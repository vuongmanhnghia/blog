---
title: Docker Fullstack Example
date: 2025-08-15
draft: false
tags:
  - docker
  - vi
---
Triển khai Full-Stack: WordPress với PostgreSQL bằng Docker Compose
<!--more-->

Phần 1: [Docker Principle](https://blog.nagih.io.vn/post/docker/docker/) 
Phần 2: [Docker CLI](https://blog.nagih.io.vn/post/docker/docker-cli/)
Phần 3: [Docker Compose](https://blog.nagih.io.vn/post/docker/docker-compose/)
Phần 4: [Docker Practical Guide](https://blog.nagih.io.vn/post/docker/docker-practical-guide/)

## Phần 5: Triển khai Full-Stack: WordPress với PostgreSQL bằng Docker Compose

Đây là phần tổng hợp, nơi chúng ta sẽ áp dụng tất cả các kiến thức đã học để triển khai một ứng dụng web hoàn chỉnh và thực tế: một trang web WordPress được hỗ trợ bởi cơ sở dữ liệu PostgreSQL. Ví dụ này thể hiện sức mạnh thực sự của Docker Compose trong việc điều phối nhiều dịch vụ phụ thuộc lẫn nhau. Đáng chú ý, chúng ta sẽ sử dụng PostgreSQL theo yêu cầu cụ thể, một lựa chọn ít phổ biến hơn so với MySQL/MariaDB trong các hướng dẫn WordPress thông thường, nhưng hoàn toàn khả thi và mạnh mẽ.

### 5.1 Kiến trúc ứng dụng

Hệ thống của chúng ta sẽ bao gồm các thành phần sau, tất cả được định nghĩa và kết nối trong một tệp `docker-compose.yml` duy nhất:

- **Dịch vụ 1 (`db`):** Một container chạy PostgreSQL, sử dụng image chính thức `postgres:15-alpine`. Đây sẽ là nơi lưu trữ tất cả nội dung của trang WordPress (bài viết, trang, người dùng, v.v.).
    
- **Dịch vụ 2 (`wordpress`):** Một container chạy WordPress, sử dụng image chính thức `wordpress:latest`. Dịch vụ này sẽ chứa máy chủ web (Apache) và PHP để chạy ứng dụng WordPress.
    
- **Volume 1 (`db_data`):** Một named volume để lưu trữ dữ liệu của PostgreSQL. Điều này đảm bảo rằng cơ sở dữ liệu của bạn sẽ tồn tại ngay cả khi container `db` bị xóa và tạo lại.
    
- **Volume 2 (`wp_content`):** Một named volume để lưu trữ các tệp của WordPress, bao gồm themes, plugins và các tệp được tải lên. Điều này cho phép bạn cập nhật phiên bản WordPress mà không làm mất các tùy chỉnh và nội dung của mình.
    
- **Network (`app_net`):** Một mạng bridge tùy chỉnh để hai dịch vụ có thể giao tiếp với nhau một cách an toàn và đáng tin cậy, tách biệt với các container khác có thể đang chạy trên cùng một máy chủ.
    

Việc sử dụng một tệp `docker-compose.yml` để định nghĩa toàn bộ kiến trúc này biến nó thành một dạng "cơ sở hạ tầng dưới dạng mã" (Infrastructure as Code). Tệp này trở thành nguồn chân lý duy nhất cho toàn bộ ứng dụng, có thể được quản lý phiên bản trong Git, chia sẻ với các thành viên trong nhóm và đảm bảo rằng mọi người đều có thể khởi tạo một môi trường giống hệt nhau chỉ bằng một lệnh duy nhất, giúp cải thiện đáng kể quá trình giới thiệu thành viên mới và tính nhất quán.

### 5.2 Phân tích chi tiết `docker-compose.yml`

Tạo một thư mục cho dự án của bạn, ví dụ `my-wordpress-site`. Bên trong thư mục đó, tạo một tệp có tên `docker-compose.yml` với nội dung sau:

YAML

```
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    container_name: wordpress_db
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    restart: always
    networks:
      - app_net

  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    container_name: wordpress_app
    ports:
      - "8000:80"
    volumes:
      - wp_content:/var/www/html
    environment:
      WORDPRESS_DB_HOST: db:5432
      WORDPRESS_DB_USER: ${POSTGRES_USER}
      WORDPRESS_DB_PASSWORD: ${POSTGRES_PASSWORD}
      WORDPRESS_DB_NAME: ${POSTGRES_DB}
    restart: always
    networks:
      - app_net

volumes:
  db_data:
  wp_content:

networks:
  app_net:
    driver: bridge
```

**Giải thích chi tiết:**

- **`services:`**: Định nghĩa hai dịch vụ của chúng ta là `db` và `wordpress`.
    
- **`db` service:**
    
    - `image: postgres:15-alpine`: Sử dụng phiên bản 15 của PostgreSQL trên nền Alpine Linux để có kích thước nhỏ.
        
    - `volumes: - db_data:/var/lib/postgresql/data`: Ánh xạ named volume `db_data` vào thư mục dữ liệu mặc định của PostgreSQL bên trong container.
        
    - `environment:`: Cấu hình cơ sở dữ liệu. Các giá trị `${...}` sẽ được Docker Compose thay thế bằng các biến môi trường từ một tệp `.env` hoặc từ shell, một thực tiễn tốt để giữ bí mật an toàn.
        
    - `restart: always`: Tự động khởi động lại container này nếu nó bị dừng.
        
    - `networks: - app_net`: Kết nối dịch vụ này vào mạng `app_net`.
        
- **`wordpress` service:**
    
    - `depends_on: - db`: Yêu cầu Compose khởi động dịch vụ `db` trước dịch vụ `wordpress`.
        
    - `ports: - "8000:80"`: Ánh xạ cổng 8000 trên máy chủ của bạn tới cổng 80 (cổng web mặc định) bên trong container WordPress.
        
    - `volumes: - wp_content:/var/www/html`: Ánh xạ named volume `wp_content` vào thư mục gốc của WordPress.
        
    - `environment:`: Cung cấp cho WordPress thông tin cần thiết để kết nối với cơ sở dữ liệu. Lưu ý `WORDPRESS_DB_HOST: db:5432`. Ở đây, `db` là tên của dịch vụ cơ sở dữ liệu, và Docker Compose sẽ đảm bảo rằng tên này được phân giải thành địa chỉ IP nội bộ của container `db` trên mạng `app_net`.
        
- **`volumes:`** (cấp cao nhất): Khai báo hai named volumes `db_data` và `wp_content` để Docker quản lý.
    
- **`networks:`** (cấp cao nhất): Khai báo mạng tùy chỉnh `app_net` sử dụng driver `bridge` mặc định.
    

### 5.3 Triển khai và Quản lý

1. Tạo tệp Biến môi trường (.env)

Trong cùng thư mục với docker-compose.yml, tạo một tệp tên là .env. Tệp này sẽ chứa các thông tin nhạy cảm. Docker Compose sẽ tự động đọc tệp này.

Lưu ý: Hãy thêm .env vào tệp .gitignore của bạn để không vô tình đưa thông tin đăng nhập vào kho mã nguồn.

Code snippet

```
#.env file
# PostgreSQL Credentials
POSTGRES_DB=wordpress
POSTGRES_USER=wp_user
POSTGRES_PASSWORD=your_strong_password
```

Thay `your_strong_password` bằng một mật khẩu mạnh và an toàn.

2. Khởi động hệ thống

Mở terminal trong thư mục dự án và chạy lệnh sau:

Bash

```
docker compose up -d
```

Docker Compose sẽ:

1. Tải về các image `postgres:15-alpine` và `wordpress:latest` nếu chúng chưa có trên máy.
    
2. Tạo mạng `app_net`.
    
3. Tạo các volume `db_data` và `wp_content`.
    
4. Khởi động container `db` trước.
    
5. Sau đó, khởi động container `wordpress`.
    
6. Tất cả sẽ chạy ở chế độ nền (`-d`).
    

Bạn có thể kiểm tra trạng thái của các container bằng lệnh `docker compose ps`.

3. Hoàn tất cài đặt WordPress

Mở trình duyệt web và truy cập http://localhost:8000. Bạn sẽ thấy màn hình cài đặt WordPress quen thuộc. Hãy làm theo các bước để chọn ngôn ngữ, đặt tên trang web, tạo tài khoản quản trị viên. Tất cả thông tin này sẽ được lưu trữ trong cơ sở dữ liệu PostgreSQL đang chạy trong container

`db`.

4. Dừng và Dọn dẹp

Khi bạn muốn dừng ứng dụng, hãy chạy:

Bash

```
docker compose down
```

Lệnh này sẽ dừng và xóa các container và mạng. Tuy nhiên, các volume (`db_data` và `wp_content`) sẽ vẫn còn. Điều này có nghĩa là nếu bạn chạy lại `docker compose up -d`, trang web của bạn sẽ trở lại với tất cả dữ liệu và tệp tin còn nguyên vẹn.

Để xóa mọi thứ, bao gồm cả dữ liệu, hãy chạy:

Bash

```
docker compose down --volumes
```


Phần 6: [Docker Best Practice for Production](https://blog.nagih.io.vn/post/docker/docker-best-practice-for-production/)