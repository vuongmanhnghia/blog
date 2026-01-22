---
title: Hướng dẫn cấu hình Nginx làm Reverse Proxy kết hợp Certbot thông qua Docker
date: 2025-11-21
image:
categories:
  - proxy
tags:
  - docker
  - nginx
draft: false
---
Hướng dẫn xây dựng mô hình **Nginx làm Reverse Proxy** kết hợp với **Certbot** theo mô hình **Sidecar** (hoặc chạy định kỳ) để quản lý SSL.

<!--more-->

---

Dưới đây là hướng dẫn triển khai theo chuẩn **Infrastructure as Code (IaC)**. Toàn bộ cấu hình nằm trong file, có thể đẩy lên Git.

---
## Kiến trúc

Chúng ta sẽ có 1 file `docker-compose.yml` quản lý **Gateway**, bao gồm:
	
1.  **Service Nginx:** Chịu trách nhiệm routing và hứng traffic (Port 80/443).
	
2.  **Service Certbot:** Chịu trách nhiệm xin và gia hạn SSL.
	
3.  **Shared Volumes:** Để Nginx và Certbot cùng đọc/ghi được file chứng chỉ.

---

## Các bước cấu hình

### Bước 1: Chuẩn bị cấu trúc thư mục

Tạo một thư mục quản lý Gateway riêng biệt (để tách biệt với code ứng dụng).

```bash
mkdir -p ~/nginx-gateway/{conf.d,certbot/conf,certbot/www}
cd ~/nginx-gateway
```
	
*   `conf.d`: Chứa file config của các domain (Virtual Hosts).
	
*   `certbot/conf`: Nơi lưu chứng chỉ SSL thật.
	
*   `certbot/www`: Nơi lưu file xác thực (ACME Challenge) để Let's Encrypt kiểm tra.

> Các folders và file này là để ánh xạ vào volumes của nginx container

---
### Bước 2: Tạo file Docker Compose

Tạo file `compose.yml`:

```yaml
services:
  nginx:
    image: nginx:alpine
    container_name: nginx-gateway
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./conf.d:/etc/nginx/conf.d
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    command: "/bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g \"daemon off;\"'"

  certbot:
    image: certbot/certbot
    container_name: certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

networks:
  default:
	name: nginx-network
    external: true
```
	
*   **Nginx Command:** Đoạn script nhỏ giúp Nginx tự động reload config mỗi 6 tiếng để cập nhật SSL mới (nếu có) mà không cần restart container (Zero Downtime).
	
*   **Certbot Entrypoint:** Chạy vòng lặp kiểm tra gia hạn SSL mỗi 12 tiếng.
	
*   **Network:** Sử dụng `nginx-network` để kết nối với các container ứng dụng khác.

---

### Bước 3: Config Nginx (Vấn đề "Con gà - Quả trứng")

Đây là điểm khó chịu nhất khi làm thủ công: **Nginx cần file SSL để khởi động, nhưng chưa có SSL thì Nginx không chạy để Certbot xin SSL được.**

**Giải pháp:** Chúng ta config 2 giai đoạn.

- Giai đoạn 1: Config HTTP để xin SSL
	
	Tạo file config cho domain của bạn: `nano conf.d/domain.com.conf`
	
	```nginx
	server {
	    listen 80;
	    server_name domain.com www.domain.com;
	
	    # Cho phép Certbot truy cập thư mục này để xác thực
	    location /.well-known/acme-challenge/ {
	        root /var/www/certbot;
	    }
	
	    location / {
	        return 301 https://$host$request_uri; # Redirect tạm, nhưng chưa có HTTPS thì cứ để đó
	    }
	}
	```
	
	Run Nginx:
	
	```bash
	docker compose up -d nginx
	```

- Giai đoạn 2: Xin SSL bằng Certbot
	
	Chạy lệnh này một lần duy nhất để lấy chứng chỉ:
	
	```bash
	docker compose run --rm --entrypoint certbot certonly --webroot --webroot-path /var/www/certbot -d domain.com -d www.domain.com
	```
	
	*Nếu thành công, nó sẽ báo "Successfully received certificate".*

- Giai đoạn 3: Config HTTPS hoàn chỉnh (Production)
	
	Bây giờ đã có file SSL trong thư mục `./certbot/conf`, bạn sửa lại file `conf.d/domain.com.conf` để cấu hình đầy đủ:
	
	```nginx
	server {
	    listen 80;
	    server_name domain.com www.domain.com;
	
	    location /.well-known/acme-challenge/ {
	        root /var/www/certbot;
	    }
	
	    location / {
	        return 301 https://$host$request_uri;
	    }
	}
	
	server {
	    listen 443 ssl;
	    server_name domain.com www.domain.com;
	
	    # Đường dẫn này được map từ volume docker
	    ssl_certificate /etc/letsencrypt/live/domain.com/fullchain.pem;
	    ssl_certificate_key /etc/letsencrypt/live/domain.com/privkey.pem;
	
	    # Best Practice SSL Params (Optional but recommended)
	    ssl_protocols TLSv1.2 TLSv1.3;
	    ssl_ciphers HIGH:!aNULL:!MD5;
	
	    location / {
	        # Proxy pass vào tên container của App (trong cùng network)
	        proxy_pass http://my-website-container:80; 
	        
	        proxy_set_header Host $host;
	        proxy_set_header X-Real-IP $remote_addr;
	        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	        proxy_set_header X-Forwarded-Proto $scheme;
	    }
	}
	```
	
	Cuối cùng, reload Nginx để nhận config mới:
	```bash
	docker compose exec nginx nginx -s reload
	```

---

### Bước 4: Quy trình vận hành (Workflow)

Từ giờ, khi bạn muốn thêm một domain mới (ví dụ: `api.domain.com`), quy trình là:
	
1.  **Tạo file config:** Tạo `conf.d/api.domain.com.conf` (chỉ có block port 80).
	
2.  **Reload Nginx:** `docker compose exec nginx nginx -s reload`.
	
3.  **Xin SSL:** Chạy lệnh `docker compose run --rm certbot ...`.
	
4.  **Update config:** Thêm block port 443 vào file config.
	
5.  **Reload Nginx:** Lần cuối.

---
## Lưu ý

```bash
docker compose run --rm --entrypoint certbot certonly --webroot --webroot-path /var/www/certbot -d domain.com -d www.domain.com
```

Sau khi run command Xin SSL bằng Certbot, hãy lưu ý các điều này để tránh xảy ra các lỗi thường gặp

1. Tắt **Cloudflare Proxy** (Đám mây màu cam) nếu đang sử dụng **Cloudflare** để trỏ tên miền tới server
	
2. Kiểm tra **Tường lửa (Firewall)**
	
	- Kiểm tra ufw đã mở `port 80/tcp` và `443/tcp` chưa
	
		```bash
		sudo ufw status
		```
	
	- Nếu chưa, chạy command sau để mở port:
	
		```bash
		sudo ufw allow 80/tcp 
		sudo ufw allow 443/tcp 
		sudo ufw reload
		```
	
3. Kiểm tra tình trạng của Nginx Container
	
4. Chú ý cú pháp các file trong `./conf.d`

---