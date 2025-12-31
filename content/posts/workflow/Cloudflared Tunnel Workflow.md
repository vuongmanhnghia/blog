---
title: Hướng dẫn setup cloudflared tunnel cơ bản
date: 2025-10-19
image:
categories:
  - workflow
  - cloudflare
tags:
  - tunnel
draft: false
---

Thiết lập Cloudflare Tunnel là một bước nâng cao cực kỳ mạnh mẽ cho server của bạn. Nó giúp bạn phơi bày (expose) các dịch vụ đang chạy trên server ra internet một cách an toàn mà không cần mở bất kỳ cổng nào trên **Firewall**.

<!--more-->

---

### **Mục tiêu:**

- Chạy một ứng dụng web trên server (ví dụ: localhost:3000).
    
- Tạo một Tunnel để kết nối server với Cloudflare.
    
- Truy cập ứng dụng web đó qua một tên miền phụ (ví dụ: app.yourdomain.com) với HTTPS mà **không cần mở cổng 80/443 trên server**.
    

### **Phase 0:** Điều Kiện Cần Có

1. **Tài khoản Cloudflare:** Hoàn toàn miễn phí.
    
2. **Tên miền đã thêm vào Cloudflare:** Bạn phải quản lý DNS của tên miền đó thông qua Cloudflare.
    
3. **Server đã cài đặt:** Một VPS hoặc máy chủ vật lý đang chạy (ví dụ: Ubuntu 22.04).
    
4. **Một dịch vụ đang chạy trên server:** Ví dụ, một ứng dụng Node.js đang lắng nghe ở cổng 3000.
    

---

### **Phase 1:** Cài Đặt cloudflared trên Server

1. **SSH vào Server**
    
2. **Cài đặt Cloudflared**
	
	- **Xác định kiến trúc CPU**
		
		```bash
		uname -a
		```
		
		Kết quả phổ biến sẽ là:

		- **x86_64 hoặc amd64**: Hầu hết các máy chủ và máy tính để bàn hiện nay.
		    
		- **aarch64 hoặc arm64**: Các máy chủ ARM, Raspberry Pi 4/5 (64-bit), máy Mac M1/M2.
		    
		- **armv7l**: Raspberry Pi cũ hơn (32-bit).
		
	- **Tải file thực thi phù hợp từ GitHub của Cloudflare**
		
		```bash
		# x86_64 / AMD64 (64-bit)
		wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
		
		# ARM64 / aarch64 (64-bit)
		wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
		
		# ARM (32-bit)
		wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm
		```
		
	- **Cài đặt file vừa tải**
		
		```bash
		# Đổi tên file cho gọn (thay amd64 bằng arm64 hoặc arm nếu cần)
		# Lưu ý: Tên file cùng với file vừa tải ở trên
		mv cloudflared-linux-amd64 cloudflared
		
		# Cấp quyền thực thi
		chmod +x cloudflared
		
		# Di chuyển vào thư mục bin của hệ thống
		sudo mv cloudflared /usr/local/bin/
		```
		
	- **Kiểm tra cài đặt**
		
		```bash
		cloudflared --version
		```
	
### **Phase 2:** Xác Thực cloudflared với Tài Khoản Cloudflare

Bước này sẽ liên kết daemon cloudflared trên server của bạn với tài khoản Cloudflare.

1. **Chạy lệnh đăng nhập:**
	
	```bash
	cloudflared tunnel login
	```  
    
2. **Thực hiện xác thực:**
    
    - Lệnh trên sẽ in ra một đường link URL trong terminal.
        
    - **Copy** và **Paste** vào trình duyệt trên máy tính cá nhân của bạn.
        
    - Đăng nhập vào tài khoản Cloudflare của bạn.
        
    - Chọn tên miền bạn muốn sử dụng cho Tunnel.
        
    - Nhấn **Authorize**.
        
3. **Xác nhận thành công:**
    
    - Sau khi xác thực thành công trên trình duyệt, cloudflared trên server của bạn sẽ tự động tải về một file chứng chỉ (cert.pem) và lưu nó vào thư mục `~/.cloudflared/`. File này chính là **Key** để server của bạn giao tiếp với Cloudflare.
        

### **Phase 3:** Cấu Hình Tunnel

Giờ là bước quan trọng nhất: tạo một Tunnel có tên và định nghĩa cách nó sẽ định tuyến lưu lượng truy cập.

1. **Tạo một Tunnel có tên:**
    
    - Hãy chọn một cái tên dễ nhớ cho tunnel của bạn (ví dụ: `main-tunnel`).
        
        ```bash
        cloudflared tunnel create main-tunnel
        ```  
        
    - Lệnh này sẽ đăng ký tunnel với Cloudflare và trả về một **UUID** (một chuỗi ID duy nhất) cho tunnel đó. Nó cũng sẽ tạo một file credentials (`<UUID>.json`) trong thư mục `~/.cloudflared/`. **Hãy lưu lại UUID này.**
        
2. **Tạo file cấu hình:**
    
    - cloudflared sử dụng một file `config.yml` để biết cách định tuyến các yêu cầu.
        
        ```bash
        vi ~/.cloudflared/config.yml
        ```  
        
    - Dán nội dung sau vào file. **Hãy thay thế UUID bằng UUID bạn nhận được ở bước trên.**
        
        ```yml
        # UUID của tunnel bạn vừa tạo 
        tunnel: 8e34e9a6-0935-4563-87c1-652a5d7a825a  
        # Đường dẫn đến file credentials 
        credentials-file: /home/your_username/.cloudflared/8e34e9a6-0935-4563-87c1-652a5d7a825a.json 
        # Cấu hình định tuyến (ingress rules) 
        ingress:   
        # Quy tắc 1: Gửi traffic từ app.yourdomain.com đến dịch vụ ở localhost:3000   
	        - hostname: app.yourdomain.com
		       service: http://localhost:3000 
	           
	    # Quy tắc cuối cùng: Bắt buộc phải có. 
	    # Nó sẽ trả về lỗi 404 cho bất kỳ request nào không khớp với các quy tắc trên.
		    - service: http_status:404
        ```
        
        - Thay `your_username` bằng tên người dùng của bạn trên server.
            
        - Thay `app.yourdomain.com` bằng tên miền phụ bạn muốn sử dụng.
            
        - Thay `http://localhost:3000` bằng địa chỉ và cổng của dịch vụ bạn muốn phơi bày.
    
### **Phase 4:** Định Tuyến DNS

1. **Chạy lệnh định tuyến DNS:**
    
    ```bash
    cloudflared tunnel route dns my-web-app app.yourdomain.com
    ```  
    
2. Lệnh này sẽ tự động tạo một bản ghi **CNAME** trong phần quản lý DNS của bạn trên Cloudflare, trỏ tên miền phụ của bạn vào tunnel.
    
### **Phase 5:** Chạy Tunnel như một Dịch Vụ (Service)

Để tunnel luôn chạy kể cả khi bạn đóng cửa sổ SSH hoặc khởi động lại server, bạn cần cài đặt nó như một dịch vụ hệ thống (systemd).

1. **Di chuyển file cấu hình và credentials đến vị trí hệ thống:**
    
    - Dịch vụ systemd sẽ tìm file cấu hình ở /etc/cloudflared/, không phải trong thư mục home của bạn.
        
        ```bash
        # Tạo thư mục cấu hình
        sudo mkdir /etc/cloudflared
        
        # Sao chép file config và đổi tên thành config.yml
        sudo cp ~/.cloudflared/config.yml /etc/cloudflared/config.yml
        
        # Sao chép file credentials
        sudo cp ~/.cloudflared/<UUID>.json /etc/cloudflared/
        ```  
        
    - **Lưu ý:** Bạn cần sửa lại đường dẫn credentials-file trong `/etc/cloudflared/config.yml để trỏ đến vị trí mới: /etc/cloudflared/<UUID>.json.`
        
        ```bash
        sudo nano /etc/cloudflared/config.yml 
        # Sửa dòng credentials-file thành: credentials-file: /etc/cloudflared/8e34e9a6-0935-4563-87c1-652a5d7a825a.json
        ```  
        
2. **Cài đặt và khởi chạy dịch vụ:**
    
    ```bash
    # Cài đặt dịch vụ systemd
    sudo cloudflared service install
    
    # Khởi động dịch vụ
    sudo systemctl start cloudflared  
    
    # (Tùy chọn) Kiểm tra trạng thái dịch vụ
    sudo systemctl status cloudflared
    ```  

	- Nếu bước này xảy ra lỗi, bạn cần kiểm tra xem có tồn tại user `cloudflared` hay không, nếu có hãy cấp quyền cho `cloudflared`. Nếu không có hãy tạo mới user `cloudflared` và cấp quyền.
	
		```bash
		# Kiểm tra có tồn tại user cloudflared không
		id cloudflared
		
		# Nếu không có user cloudflared
		sudo useradd -r -M -s /usr/sbin/nologin cloudflared
		
		# Phân quyền sở hữu
		sudo chown -R cloudflared:cloudflared /etc/cloudflared
		sudo chmod 640 /etc/cloudflared/*
		
		# Hãy quay lại Bước 2: Cài đặt và khởi tạo dịch vụ
		```
		
**Xong!** Bây giờ, hãy thử truy cập` https://app.yourdomain.com` trên trình duyệt. Bạn sẽ thấy ứng dụng của mình đang chạy, được bảo vệ bởi Cloudflare với HTTPS, trong khi server của bạn không hề mở bất kỳ cổng nào ra ngoài internet.

---

### Tích Hợp với Docker và Docker Compose

Nếu bạn đang dùng Docker, việc chạy cloudflared trong một container riêng là cách làm khá Ok.

- Bạn có thể thêm một service cloudflared vào `file docker-compose.yml`
	
	```yml
	services:
		web-app:
			build: .     
			# ... các cấu hình khác của bạn
		networks:
			- app-network
			  
	cloudflared:
		image: cloudflare/cloudflared:latest
		restart: unless-stopped
		command: tunnel --no-autoupdate run --token <YOUR_TUNNEL_TOKEN>
		depends_on:
			- web-app     
		networks:
			- app-network
	networks:
		app-network:
			driver: bridge
	```
	
- Trong trường hợp này, bạn sẽ lấy **Token** của Tunnel từ trang quản trị Cloudflare Zero Trust thay vì dùng file `cert.pem` và `credentials.json`.
    
- Trong trang quản trị Cloudflare, bạn sẽ cấu hình Public Hostname (`app.yourdomain.com`) để trỏ đến service bên trong mạng Docker (ví dụ: `http://web-app:3000`).
    

*ps: Cách làm này phù hợp với quy trình tự động hóa và IaC (Infrastructure as Code)*

---