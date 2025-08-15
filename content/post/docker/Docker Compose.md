---
title: Docker Compose
date: 2025-08-14
draft: false
tags:
  - docker
  - vi
---
Điều phối Ứng dụng với Docker Compose
<!--more-->

Phần 1: [Docker Principle](https://blog.nagih.io.vn/post/docker/docker/) 
Phần 2: [Docker CLI](https://blog.nagih.io.vn/post/docker/docker-cli/)

## Phần 3: Điều phối Ứng dụng với Docker Compose

Khi các ứng dụng trở nên phức tạp hơn, chúng thường bao gồm nhiều thành phần phụ thuộc lẫn nhau—một máy chủ web, một API backend, một cơ sở dữ liệu, một hàng đợi tin nhắn, v.v. Việc quản lý từng container riêng lẻ bằng các lệnh `docker run` dài dòng và phức tạp trở nên không thực tế và dễ gây ra lỗi.

Đây là lúc Docker Compose tỏa sáng. Docker Compose là một công cụ cho phép định nghĩa và chạy các ứng dụng Docker đa container một cách dễ dàng. Với Compose, bạn sử dụng một tệp YAML duy nhất (thường là

`docker-compose.yml`) để cấu hình tất cả các dịch vụ, mạng và volume của ứng dụng. Sau đó, chỉ với một lệnh duy nhất, bạn có thể khởi động hoặc gỡ bỏ toàn bộ hệ thống.

### 3.1 Cấu trúc của tệp `docker-compose.yml`

Tệp `docker-compose.yml` là trung tâm của việc quản lý ứng dụng với Compose. Nó có cấu trúc khai báo, nghĩa là bạn mô tả "trạng thái mong muốn" của hệ thống, và Compose sẽ thực hiện các bước cần thiết để đạt được trạng thái đó. Các thành phần chính bao gồm:

- **`services`**: Đây là khối chính, nơi bạn định nghĩa mỗi thành phần của ứng dụng như một "dịch vụ". Mỗi dịch vụ tương ứng với một hoặc nhiều container chạy cùng một image.
    
    - **`image: <image_name>:<tag>`**: Chỉ định image Docker sẽ được sử dụng để tạo container cho dịch vụ này. Compose sẽ tìm image này trên máy cục bộ hoặc tải về từ Docker Hub.
        
    - **`build: <path_to_context>`**: Thay vì sử dụng một image có sẵn, bạn có thể yêu cầu Compose xây dựng một image tại chỗ từ một `Dockerfile`. Giá trị này là đường dẫn đến thư mục chứa `Dockerfile` (ví dụ: `build:.`).
        
    - **`ports: - "<host_port>:<container_port>"`**: Ánh xạ cổng giữa máy chủ và container, tương tự cờ `-p` trong `docker run`.
        
    - **`volumes: - <volume_name_or_host_path>:<container_path>`**: Gắn một volume hoặc một thư mục từ máy chủ vào container. Đây là cách để lưu trữ dữ liệu bền bỉ hoặc chia sẻ tệp giữa máy chủ và container.
        
    - **`environment: - <VAR_NAME>=<value>`**: Thiết lập các biến môi trường bên trong container. Đây là cách phổ biến để truyền các thông tin cấu hình như thông tin đăng nhập cơ sở dữ liệu, khóa API, v.v..
        
    - **`networks: - <network_name>`**: Kết nối dịch vụ vào một hoặc nhiều mạng được định nghĩa. Compose tự động tạo một mạng mặc định cho tất cả các dịch vụ trong tệp, nhưng việc định nghĩa mạng tùy chỉnh mang lại sự kiểm soát tốt hơn.
        
    - **`depends_on: - <service_name>`**: Xác định sự phụ thuộc giữa các dịch vụ. Ví dụ, bạn có thể yêu cầu dịch vụ web chỉ khởi động sau khi dịch vụ cơ sở dữ liệu đã khởi động.
        
- **`volumes`** (cấp cao nhất): Nơi bạn định nghĩa các "named volumes". Việc khai báo chúng ở đây cho phép chúng được tái sử dụng và quản lý dễ dàng bởi Compose.
    
- **`networks`** (cấp cao nhất): Nơi bạn định nghĩa các mạng tùy chỉnh. Điều này cho phép bạn tạo ra các cấu trúc liên kết mạng phức tạp hơn và cô lập các nhóm dịch vụ.
    

### 3.2 Từ `docker run` đến `docker-compose.yml`

Để làm rõ mối liên hệ giữa CLI và Compose, bảng dưới đây sẽ ánh xạ các cờ phổ biến của lệnh `docker run` sang các khóa tương đương trong tệp `docker-compose.yml`. Việc hiểu rõ sự tương ứng này giúp quá trình chuyển đổi từ việc quản lý container đơn lẻ sang điều phối toàn bộ ứng dụng trở nên trực quan hơn. Nó cho thấy `docker-compose.yml` không phải là một ngôn ngữ hoàn toàn mới, mà là một cách khai báo, có cấu trúc để thể hiện những cấu hình tương tự.

|Cờ `docker run`|Khóa `docker-compose.yml`|Ví dụ|
|---|---|---|
|`-d`|(Mặc định khi dùng `up -d`)|`docker compose up -d`|
|`-p 8080:80`|`ports`|`ports: ["8080:80"]`|
|`-v my-data:/data`|`volumes`|`volumes: ["my-data:/data"]`|
|`-e VAR=value`|`environment`|`environment:`|
|`--name my-app`|`container_name`|`container_name: my-app`|
|`--network my-net`|`networks`|`networks: ["my-net"]`|
|`--restart=always`|`restart`|`restart: always`|

### 3.3 Các lệnh Docker Compose cốt lõi

Sau khi đã định nghĩa ứng dụng trong tệp `docker-compose.yml`, bạn sử dụng một vài lệnh đơn giản để quản lý toàn bộ vòng đời của nó.

- `docker compose up`: Lệnh này là trái tim của Compose. Nó đọc tệp `docker-compose.yml`, xây dựng các image cần thiết, tạo và khởi chạy tất cả các container dịch vụ, và tạo các network và volume tương ứng. Nếu không có cờ `-d`, nó sẽ chạy ở chế độ foreground và hiển thị log tổng hợp từ tất cả các container.
    
    - `docker compose up -d`: Chạy ứng dụng ở chế độ nền (detached). Đây là cách sử dụng phổ biến nhất trong môi trường phát triển và sản xuất.
        
- `docker compose down`: Lệnh này là đối nghịch của `up`. Nó sẽ dừng và xóa tất cả các container, cùng với các network được tạo bởi Compose.
    
    - `docker compose down --volumes`: Thêm cờ này để xóa cả các named volumes đã được định nghĩa trong tệp Compose. Hãy cẩn thận vì điều này sẽ xóa vĩnh viễn dữ liệu.
        
- `docker compose build`: Nếu bạn đã thay đổi `Dockerfile` của một dịch vụ, lệnh này sẽ buộc xây dựng lại image cho dịch vụ đó trước khi chạy `up`.
    
- `docker compose logs`: Hiển thị log từ các container dịch vụ.
    
    - `docker compose logs -f <service_name>`: Theo dõi log của một dịch vụ cụ thể trong thời gian thực.
        
- `docker compose exec <service_name> <command>`: Thực thi một lệnh bên trong một container của một dịch vụ đang chạy. Rất hữu ích để chạy các tác vụ quản trị hoặc mở một shell để gỡ lỗi.
    
    - Ví dụ: `docker compose exec web sh`
        


Phần 4: [Docker Practical Guide](https://blog.nagih.io.vn/post/docker/docker-practical-guide/)
Phần 5: [Docker Fullstack Example](https://blog.nagih.io.vn/post/docker/docker-fullstack-example/)
Phần 6: [Docker Best Practice for Production](https://blog.nagih.io.vn/post/docker/docker-best-practice-for-production/)