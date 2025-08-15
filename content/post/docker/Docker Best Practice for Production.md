---
title: Docker Best Practice for Production
date: 2025-08-15
draft: false
tags:
  - docker
  - vi
---
Các Thực tiễn Tốt nhất cho Môi trường Production
<!--more-->

Phần 1: [Docker Principle](https://blog.nagih.io.vn/post/docker/docker/) 
Phần 2: [Docker CLI](https://blog.nagih.io.vn/post/docker/docker-cli/)
Phần 3: [Docker Compose](https://blog.nagih.io.vn/post/docker/docker-compose/)
Phần 4: [Docker Practical Guide](https://blog.nagih.io.vn/post/docker/docker-practical-guide/)
Phần 5: [Docker Fullstack Example](https://blog.nagih.io.vn/post/docker/docker-fullstack-example/)

## Phần 6: Các Thực tiễn Tốt nhất cho Môi trường Production

Việc đưa các ứng dụng container hóa vào môi trường production đòi hỏi một mức độ cẩn trọng và tối ưu hóa cao hơn so với môi trường phát triển. Phần này sẽ cung cấp các thực tiễn tốt nhất, giúp bạn xây dựng các image nhỏ gọn, an toàn và các tệp Compose có khả năng bảo trì cao, sẵn sàng cho việc triển khai thực tế.

### 6.1 Tối ưu hóa Kích thước và Tốc độ: Multi-Stage Builds

Một trong những vấn đề phổ biến nhất với các Docker image là chúng trở nên cồng kềnh. Một image lớn không chỉ chiếm nhiều dung lượng lưu trữ mà còn làm tăng thời gian tải về và triển khai. Tệ hơn nữa, nó thường chứa các công cụ xây dựng (như JDK, Go toolchain, `build-essentials`) và các dependencies chỉ cần thiết cho quá trình biên dịch, không cần thiết cho việc chạy ứng dụng. Những thành phần thừa này làm tăng bề mặt tấn công của image một cách không cần thiết.

**Multi-stage builds** là một tính năng mạnh mẽ của Docker để giải quyết vấn đề này. Kỹ thuật này cho phép bạn sử dụng nhiều lệnh

`FROM` trong cùng một `Dockerfile`. Mỗi lệnh `FROM` bắt đầu một "stage" (giai đoạn) xây dựng mới.

Cách hoạt động rất đơn giản và hiệu quả:

1. **Stage 1 (Build Stage):** Bạn sử dụng một image cơ sở đầy đủ (ví dụ: `golang:1.21`) có tất cả các công cụ cần thiết để biên dịch, kiểm thử và đóng gói ứng dụng của bạn. Giai đoạn này được đặt tên (ví dụ: `AS builder`).
    
2. **Stage 2 (Final Stage):** Bạn bắt đầu một giai đoạn mới với một image cơ sở tối giản (ví dụ: `alpine:latest` hoặc thậm chí `scratch`—một image trống).
    
3. **Copy Artifacts:** Bạn sử dụng lệnh `COPY --from=builder` để sao chép chỉ những tạo tác (artifacts) cần thiết—chẳng hạn như tệp nhị phân đã biên dịch hoặc các tệp đã được thu nhỏ—từ giai đoạn xây dựng vào giai đoạn cuối cùng.
    

Ví dụ với ứng dụng Go từ Phần 4 đã minh họa hoàn hảo điều này. Image cuối cùng chỉ chứa tệp nhị phân thực thi và image Alpine cơ sở, giảm kích thước từ hàng trăm MB xuống chỉ còn vài MB.

### 6.2 Tăng cường Bảo mật

Bảo mật là yếu tố không thể bỏ qua khi triển khai. `Dockerfile` của bạn là tuyến phòng thủ đầu tiên.

- **Chạy với người dùng không phải root:** Mặc định, các container chạy với người dùng `root`, điều này tạo ra một rủi ro bảo mật nghiêm trọng. Nếu một kẻ tấn công khai thác được một lỗ hổng trong ứng dụng của bạn và thoát ra khỏi container, chúng có thể có quyền `root` trên máy chủ. Hãy luôn tạo một người dùng và nhóm không có đặc quyền bên trong `Dockerfile` và sử dụng lệnh `USER` để chuyển sang người dùng đó trước khi chạy ứng dụng.
    
    Dockerfile
    
    ```
    # Create a non-root user
    RUN addgroup -S appgroup && adduser -S appuser -G appgroup
    
    #... copy files and set permissions...
    RUN chown -R appuser:appgroup /app
    
    # Switch to the non-root user
    USER appuser
    
    CMD ["/app/my-binary"]
    ```
    
- **Chọn base image tối giản:** Nguyên tắc là "càng ít càng tốt". Một image cơ sở tối giản như `alpine`, `distroless`, hoặc `scratch` chứa ít thành phần hơn, đồng nghĩa với việc có ít lỗ hổng tiềm tàng hơn và bề mặt tấn công nhỏ hơn.
    
- **Sử dụng `.dockerignore`:** Tương tự như `.gitignore`, tệp `.dockerignore` ngăn chặn các tệp và thư mục không cần thiết (như `.git`, `node_modules`, các tệp log cục bộ, tệp bí mật) được gửi đến Docker daemon trong quá trình xây dựng. Điều này không chỉ giúp image nhỏ hơn mà còn ngăn chặn việc vô tình rò rỉ thông tin nhạy cảm vào image.
    

### 6.3 Quản lý các file Compose có thể bảo trì

Khi dự án phát triển, việc quản lý cấu hình cho các môi trường khác nhau (phát triển, kiểm thử, sản xuất) trở nên quan trọng.

- **Sử dụng biến môi trường và tệp `.env`:** **Không bao giờ** ghi cứng các giá trị nhạy cảm như mật khẩu, khóa API, hoặc thông tin đăng nhập cơ sở dữ liệu trực tiếp vào tệp `docker-compose.yml`. Thay vào đó, hãy tham chiếu chúng dưới dạng biến môi trường. Docker Compose sẽ tự động tải các biến từ một tệp `.env` trong cùng thư mục. Tệp `.env` này nên được thêm vào `.gitignore` để đảm bảo nó không được đưa vào hệ thống quản lý phiên bản.
    
    - Trong `docker-compose.yml`:
        
        YAML
        
        ```
        environment:
          - DB_PASSWORD=${POSTGRES_PASSWORD}
        ```
        
    - Trong tệp `.env`:
        
        Code snippet
        
        ```
        POSTGRES_PASSWORD=supersecret
        ```
        
- **Quản lý các môi trường khác nhau (Dev vs. Prod):** Thay vì duy trì nhiều tệp Compose gần như giống hệt nhau, hãy sử dụng một tệp `docker-compose.yml` cơ sở cho các cấu hình chung và một tệp `docker-compose.override.yml` cho các cấu hình dành riêng cho môi trường phát triển. Docker Compose tự động đọc và hợp nhất cả hai tệp này.
    
    - **`docker-compose.yml` (cơ sở, cho production):**
        
        YAML
        
        ```
        services:
          web:
            image: my-app:latest
            ports: ["80:8000"]
        ```
        
    - **`docker-compose.override.yml` (cho development, không commit vào Git):**
        
        YAML
        
        ```
        services:
          web:
            build:.
            volumes:
              -.:/app  # Mount source code for live reload
            ports:
              - "8000:8000"
            command: npm run dev
        ```
        
    
    Khi bạn chạy `docker compose up`, Compose sẽ hợp nhất hai tệp này, tạo ra một cấu hình phát triển hoàn chỉnh. Trong môi trường production, bạn chỉ cần triển khai tệp `docker-compose.yml` cơ sở.