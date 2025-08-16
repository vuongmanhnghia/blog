---
title: Docker CLI
date: 2025-08-13
draft: false
tags:
  - docker
  - vi
---
Làm chủ Docker Command Line (CLI)
<!--more-->

*Phần 1: [Docker Principle](https://blog.nagih.io.vn/post/docker/docker/) *
## Phần 2: Làm Chủ Docker Command Line (CLI)

Giao diện dòng lệnh (CLI) là công cụ chính để tương tác với Docker Daemon. Thay vì chỉ liệt kê các lệnh một cách khô khan, phần này sẽ tổ chức chúng theo các quy trình làm việc (workflow) mà một lập trình viên thường gặp phải hàng ngày, giúp hiểu rõ hơn về bối cảnh và mục đích sử dụng của từng lệnh.

### 2.1 Quản lý Image

Quản lý image là bước đầu tiên trong mọi quy trình làm việc với Docker. Đây là quá trình tạo, phân phối và duy trì các "bản thiết kế" cho ứng dụng của bạn.

- `docker build`: Lệnh này xây dựng một Docker image từ một `Dockerfile` và một "bối cảnh" (context). Bối cảnh là tập hợp các tệp tại đường dẫn được chỉ định. Cờ `-t` (tag) được sử dụng để đặt tên và phiên bản cho image, giúp dễ dàng nhận dạng.
    
    - Ví dụ: `docker build -t my-app:1.0.` 
        
- `docker images` (hoặc `docker image ls`): Liệt kê tất cả các image hiện có trên máy cục bộ của bạn, hiển thị thông tin như REPOSITORY, TAG, IMAGE ID, và SIZE.
    
- `docker pull`: Tải một image hoặc một kho lưu trữ (repository) từ một registry, mặc định là Docker Hub.
    
    - Ví dụ: `docker pull postgres:15-alpine` 
        
- `docker push`: Tải một image từ máy cục bộ của bạn lên một registry, cho phép chia sẻ với những người khác hoặc sử dụng trong môi trường production.
    
    - Ví dụ: `docker push your-username/my-app:1.0` 
        
- `docker rmi` (hoặc `docker image rm`): Xóa một hoặc nhiều image khỏi máy cục bộ để giải phóng dung lượng đĩa.
    
    - Ví dụ: `docker rmi my-app:1.0` 
        
- `docker inspect <image>`: Cung cấp thông tin chi tiết, ở cấp độ thấp về một image, bao gồm các lớp của nó và siêu dữ liệu (metadata).
    

### 2.2 Vòng đời Container

Sau khi có image, bước tiếp theo là tạo và quản lý các thực thể chạy của nó - các container.

- `docker run`: Đây là lệnh trung tâm, kết hợp việc tạo và khởi chạy một container mới từ một image. Nó có nhiều cờ tùy chọn mạnh mẽ:
    
    - `-d` hoặc `--detach`: Chạy container ở chế độ nền (detached mode) và in ra ID của container.
        
    - `-p <host_port>:<container_port>`: Ánh xạ một cổng trên máy chủ (host) tới một cổng bên trong container, cho phép truy cập ứng dụng từ bên ngoài. Ví dụ: `-p 8080:80`.
        
    - `--name <container_name>`: Gán một tên cụ thể cho container để dễ dàng tham chiếu thay vì sử dụng ID ngẫu nhiên.
        
    - `-v <host_path_or_volume_name>:<container_path>`: Gắn một volume hoặc một thư mục từ máy chủ vào container.
        
    - `-e <VAR_NAME>=<value>`: Thiết lập một biến môi trường bên trong container.
        
    - Ví dụ đầy đủ: `docker run -d -p 8080:80 --name webserver -e APP_MODE=production nginx:latest`
        
- `docker ps`: Liệt kê tất cả các container đang chạy. Sử dụng cờ `-a` để hiển thị tất cả các container, bao gồm cả những container đã dừng.
    
- `docker stop <container_name_or_id>`: Dừng một hoặc nhiều container đang chạy một cách nhẹ nhàng (gửi tín hiệu SIGTERM).
    
- `docker start <container_name_or_id>`: Khởi động lại một hoặc nhiều container đã bị dừng.
    
- `docker restart <container_name_or_id>`: Dừng và sau đó khởi động lại một container.
    
- `docker rm <container_name_or_id>`: Xóa một hoặc nhiều container đã dừng. Sử dụng cờ `-f` để buộc xóa một container đang chạy.
    

### 2.3 Tương tác và Gỡ lỗi Container

Khi container đang chạy, bạn thường cần phải "nhìn vào bên trong" để gỡ lỗi hoặc thực hiện các tác vụ quản trị.

- `docker logs <container>`: Lấy và hiển thị nhật ký (logs) được tạo ra bởi một container. Cờ `-f` (follow) rất hữu ích để theo dõi luồng log trong thời gian thực, tương tự như lệnh `tail -f` trong Linux.
    
- `docker exec -it <container> <command>`: Thực thi một lệnh bên trong một container đang chạy. Cờ `-it` (`-i` cho interactive và `-t` cho TTY) cho phép bạn có một phiên làm việc tương tác. Đây là cách phổ biến nhất để "vào" một container.
    
    - Ví dụ: `docker exec -it webserver bash` sẽ mở một phiên shell Bash tương tác bên trong container tên là `webserver`.
        
- `docker stats`: Hiển thị một luồng trực tiếp về việc sử dụng tài nguyên (CPU, bộ nhớ, mạng I/O) của các container đang chạy, rất hữu ích để theo dõi hiệu suất.
    

### 2.4 Dọn dẹp hệ thống

Theo thời gian, Docker có thể tích tụ nhiều đối tượng không sử dụng (container đã dừng, image cũ, volume không được gắn), chiếm dụng không gian đĩa.

- `docker system prune`: Một lệnh dọn dẹp mạnh mẽ, theo mặc định sẽ xóa tất cả các container đã dừng, các mạng không được sử dụng, các image lơ lửng (dangling images - những image không có tag và không được container nào sử dụng), và build cache.
    
    - `docker system prune -a`: Mở rộng việc dọn dẹp để xóa tất cả các image không được sử dụng (không chỉ là dangling).
        
    - `docker system prune --volumes`: Bao gồm cả việc xóa các volume không được sử dụng.
        

### Bảng tra cứu nhanh các lệnh Docker CLI thiết yếu

Bảng dưới đây tóm tắt các lệnh Docker CLI quan trọng nhất để tham khảo nhanh.

| Lệnh                  | Mô tả                                                            | Ví dụ sử dụng                             |
| --------------------- | ---------------------------------------------------------------- | ----------------------------------------- |
| `docker build`        | Xây dựng một image từ một Dockerfile.                            | `docker build -t my-app:latest.`          |
| `docker run`          | Tạo và khởi chạy một container mới từ một image.                 | `docker run -d -p 80:80 --name web nginx` |
| `docker ps`           | Liệt kê các container đang chạy. Sử dụng `-a` để liệt kê tất cả. | `docker ps -a`                            |
| `docker stop`         | Dừng một container đang chạy.                                    | `docker stop web`                         |
| `docker rm`           | Xóa một container đã dừng.                                       | `docker rm web`                           |
| `docker images`       | Liệt kê các image trên máy.                                      | `docker images`                           |
| `docker rmi`          | Xóa một image.                                                   | `docker rmi nginx`                        |
| `docker pull`         | Tải một image từ registry.                                       | `docker pull ubuntu:22.04`                |
| `docker push`         | Đẩy một image lên registry.                                      | `docker push my-username/my-app`          |
| `docker exec`         | Chạy một lệnh bên trong một container đang chạy.                 | `docker exec -it web bash`                |
| `docker logs`         | Xem nhật ký của một container. Sử dụng `-f` để theo dõi.         | `docker logs -f web`                      |
| `docker system prune` | Dọn dẹp các container, network và image không sử dụng.           | `docker system prune -a --volumes`        |

*Phần 3: [Docker Compose](https://blog.nagih.io.vn/post/docker/docker-compose/)*

*Phần 4: [Docker Practical Guide](https://blog.nagih.io.vn/post/docker/docker-practical-guide/)*

*Phần 5: [Docker Fullstack Example](https://blog.nagih.io.vn/post/docker/docker-fullstack-example/)*

*Phần 6: [Docker Best Practice for Production](https://blog.nagih.io.vn/post/docker/docker-best-practice-for-production/)*