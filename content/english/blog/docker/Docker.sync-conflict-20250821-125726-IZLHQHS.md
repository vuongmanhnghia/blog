---
title: "Docker Overview"
meta_title: "Docker Overview"
description: "Tổng hợp các kiến thức cần biết về Docker"
date: 2025-08-12
image: "/images/image-placeholder.png"
categories: ["devops"]
author: "Nagih"
tags: ["docker"]
draft: false
---
Tổng hợp các kiến thức cần biết về Docker
<!--more-->
## Phần 1: Cuộc Cách Mạng Container - Thấu Hiểu Các Nguyên Tắc Cốt Lõi của Docker

### 1.1 Giới thiệu về Docker: Tại sao lại là một cuộc cách mạng?

Trong thế giới phát triển phần mềm hiện đại, Docker đã nổi lên như một công nghệ nền tảng, thay đổi cách các lập trình viên xây dựng, vận chuyển và chạy ứng dụng. Về cơ bản, Docker là một nền tảng mã nguồn mở được thiết kế để tự động hóa việc triển khai ứng dụng bên trong các môi trường biệt lập, nhẹ được gọi là container.1 Mỗi container đóng gói phần mềm cùng với tất cả những gì nó cần để hoạt động—bao gồm thư viện, công cụ hệ thống, mã nguồn và thời gian chạy (runtime)—thành một đơn vị tiêu chuẩn hóa.3

Để hiểu rõ giá trị của Docker, điều quan trọng là phải phân biệt nó với công nghệ ảo hóa truyền thống: máy ảo (Virtual Machines - VMs).

- **Máy ảo (VMs):** Một máy ảo ảo hóa toàn bộ phần cứng vật lý, cho phép nhiều hệ điều hành khách (guest OS) chạy trên một máy chủ chủ (host server) duy nhất. Mỗi VM bao gồm một bản sao đầy đủ của một hệ điều hành, các tệp nhị phân và thư viện cần thiết, và chính ứng dụng. Điều này dẫn đến sự cô lập mạnh mẽ nhưng phải trả giá bằng việc tiêu tốn tài nguyên đáng kể, kích thước lớn (hàng gigabyte) và thời gian khởi động chậm.4
    
- **Containers:** Ngược lại, container ảo hóa ở cấp độ hệ điều hành. Thay vì đóng gói cả một hệ điều hành khách, các container chia sẻ nhân (kernel) của hệ điều hành máy chủ.6 Chúng chỉ đóng gói ứng dụng và các dependencies của nó. Kết quả là các container cực kỳ nhẹ (thường chỉ vài chục megabyte), khởi động gần như tức thì và cho phép mật độ ứng dụng cao hơn nhiều trên cùng một phần cứng.5
    

Sự thay đổi mô hình này mang lại những lợi ích to lớn, định hình lại toàn bộ vòng đời phát triển phần mềm:

- **Phân phối ứng dụng nhanh chóng, nhất quán:** Docker giải quyết triệt để vấn đề kinh điển "nó chạy trên máy tôi nhưng không chạy trên production". Bằng cách đóng gói ứng dụng và môi trường của nó lại với nhau, Docker đảm bảo tính nhất quán trên các môi trường phát triển, kiểm thử và sản xuất.8
    
- **Tính di động (Portability) vượt trội:** Một container được xây dựng trên máy tính xách tay của lập trình viên có thể chạy không thay đổi trên bất kỳ hệ thống nào có cài đặt Docker, cho dù đó là máy chủ vật lý tại chỗ, máy ảo trên đám mây hay trong một môi trường lai.1
    
- **Hiệu quả và Tiết kiệm chi phí:** Vì các container nhẹ hơn nhiều so với VM, chúng cho phép chạy nhiều ứng dụng hơn trên cùng một cơ sở hạ tầng. Điều này cải thiện đáng kể việc sử dụng tài nguyên và giúp tiết kiệm chi phí phần cứng và cấp phép.3
    
- **Tăng tốc quy trình phát triển (CI/CD):** Docker tích hợp liền mạch vào các quy trình Tích hợp liên tục và Triển khai liên tục (CI/CD). Các image container có thể được xây dựng, kiểm thử và đẩy lên registry một cách tự động, giúp tăng tốc độ phát hành phần mềm một cách đáng kể.1
    

Sự phổ biến của Docker không chỉ là một thành tựu kỹ thuật; nó là chất xúc tác trực tiếp cho văn hóa DevOps. Các lợi ích kỹ thuật như môi trường chuẩn hóa 1 và tính di động 8 đã cung cấp cơ chế thực tế để thực hiện các nguyên lý cốt lõi của DevOps: phá vỡ các rào cản giữa phát triển (Dev) và vận hành (Ops), tự động hóa các quy trình, và tăng tần suất triển khai. Docker không chỉ tạo ra một công cụ mới; nó đã biến DevOps từ một triết lý thành một thực tiễn khả thi cho hàng triệu lập trình viên trên toàn thế giới.7

### 1.2 Hệ sinh thái Docker: Các Thành phần Cơ bản

Để làm việc hiệu quả với Docker, việc nắm vững các khái niệm và thành phần cốt lõi của nó là điều bắt buộc.

Kiến trúc Docker

Docker hoạt động theo kiến trúc client-server. Thành phần chính bao gồm:

- **Docker Daemon (`dockerd`):** Một dịch vụ nền chạy trên máy chủ, chịu trách nhiệm xây dựng, chạy và quản lý các đối tượng Docker như images, containers, networks và volumes.
    
- **Docker Client (`docker`):** Công cụ dòng lệnh (CLI) mà người dùng tương tác. Khi một lệnh như `docker run` được thực thi, client sẽ gửi yêu cầu đến daemon thông qua REST API qua socket UNIX hoặc giao diện mạng.1
    

Images và Containers: Bản thiết kế và Thực thể

Đây là khái niệm cơ bản và quan trọng nhất trong Docker, thường gây nhầm lẫn cho người mới bắt đầu. Một phép ẩn dụ hữu ích là xem Image như một Class trong lập trình hướng đối tượng và Container như một Instance của class đó.10

- **Image:** Một Docker image là một mẫu (template) chỉ đọc (read-only) và bất biến (immutable) chứa một tập hợp các chỉ dẫn để tạo ra một container.11 Nó giống như một bản thiết kế chi tiết, bao gồm mã nguồn ứng dụng, runtime, thư viện, biến môi trường và các tệp cấu hình. Images được xây dựng từ một
    
    `Dockerfile` và bao gồm một loạt các lớp (layers) xếp chồng lên nhau. Mỗi chỉ thị trong Dockerfile tạo ra một lớp mới. Tính bất biến này chính là nguyên nhân trực tiếp tạo ra khả năng tái tạo và tính nhất quán mà Docker cung cấp; vì image không thể thay đổi, mọi container được khởi tạo từ nó đều được đảm bảo giống hệt nhau, loại bỏ hoàn toàn sự trôi dạt môi trường.4
    
- **Container:** Một Docker container là một thực thể đang chạy (a running instance) của một image.4 Khi Docker tạo một container từ một image, nó sẽ thêm một lớp có thể ghi (writable layer) lên trên các lớp chỉ đọc của image. Bất kỳ thay đổi nào được thực hiện bên trong container—chẳng hạn như tạo tệp mới, sửa đổi cấu hình, hoặc cài đặt phần mềm—đều được ghi vào lớp này. Điều này có nghĩa là nhiều container có thể chia sẻ cùng một image cơ sở trong khi vẫn duy trì trạng thái riêng biệt của chúng.12
    

Dockerfile: Công thức để tạo Image

Dockerfile là một tệp văn bản đơn giản chứa các hướng dẫn từng bước để Docker tự động xây dựng một image.13 Mỗi lệnh (ví dụ:

`FROM`, `COPY`, `RUN`, `CMD`) trong Dockerfile tương ứng với một lớp trong image. Cấu trúc phân lớp này rất hiệu quả vì Docker sẽ lưu trữ (cache) các lớp; khi bạn xây dựng lại image, chỉ những lớp đã thay đổi kể từ lần xây dựng trước mới được tạo lại, giúp quá trình xây dựng nhanh hơn đáng kể.1

Volumes: Lưu trữ dữ liệu bền bỉ

Bản chất của container là tạm thời (ephemeral). Khi một container bị xóa, lớp ghi của nó cũng bị xóa theo, và mọi dữ liệu được tạo ra trong đó sẽ bị mất vĩnh viễn.14 Đối với các ứng dụng cần lưu trữ dữ liệu lâu dài (ứng dụng có trạng thái - stateful), chẳng hạn như cơ sở dữ liệu hoặc hệ thống quản lý nội dung, điều này là không thể chấp nhận được.

**Volumes** là giải pháp của Docker cho vấn đề này. Chúng là một cơ chế lưu trữ bền bỉ được quản lý hoàn toàn bởi Docker và tồn tại độc lập với vòng đời của bất kỳ container nào.14 Dữ liệu trong một volume có thể được chia sẻ giữa nhiều container và vẫn tồn tại ngay cả khi tất cả các container sử dụng nó đã bị xóa. Đây là phương pháp được khuyến nghị để xử lý dữ liệu cho các ứng dụng stateful.18

Networks: Giao tiếp giữa các Container

Mặc định, các container được cô lập với nhau. Để cho phép chúng giao tiếp, Docker cung cấp một hệ thống mạng ảo mạnh mẽ.19 Khi Docker khởi động, nó tạo ra một số mạng mặc định. Các loại mạng chính bao gồm:

- **`bridge`:** Đây là mạng mặc định cho các container. Các container được kết nối với cùng một mạng bridge có thể giao tiếp với nhau bằng tên container của chúng, nhờ vào hệ thống DNS tích hợp của Docker. Chúng được cô lập với các container trên các mạng bridge khác.20
    
- **`host`:** Loại bỏ sự cô lập mạng giữa container và máy chủ Docker. Container chia sẻ trực tiếp không gian mạng của máy chủ. Điều này cung cấp hiệu suất mạng tốt hơn nhưng làm mất đi lợi ích của sự cô lập.21
    
- **`overlay`:** Được sử dụng để kết nối các container chạy trên nhiều máy chủ Docker khác nhau, tạo thành một mạng ảo duy nhất. Đây là nền tảng cho các công cụ điều phối như Docker Swarm.19
    

## Phần 2: Làm Chủ Docker Command Line (CLI)

Giao diện dòng lệnh (CLI) là công cụ chính để tương tác với Docker Daemon. Thay vì chỉ liệt kê các lệnh một cách khô khan, phần này sẽ tổ chức chúng theo các quy trình làm việc (workflow) mà một lập trình viên thường gặp phải hàng ngày, giúp hiểu rõ hơn về bối cảnh và mục đích sử dụng của từng lệnh.

### 2.1 Workflow 1: Quản lý Image

Quản lý image là bước đầu tiên trong mọi quy trình làm việc với Docker. Đây là quá trình tạo, phân phối và duy trì các "bản thiết kế" cho ứng dụng của bạn.

- `docker build`: Lệnh này xây dựng một Docker image từ một `Dockerfile` và một "bối cảnh" (context). Bối cảnh là tập hợp các tệp tại đường dẫn được chỉ định. Cờ `-t` (tag) được sử dụng để đặt tên và phiên bản cho image, giúp dễ dàng nhận dạng.
    
    - Ví dụ: `docker build -t my-app:1.0.` 22
        
- `docker images` (hoặc `docker image ls`): Liệt kê tất cả các image hiện có trên máy cục bộ của bạn, hiển thị thông tin như REPOSITORY, TAG, IMAGE ID, và SIZE.13
    
- `docker pull`: Tải một image hoặc một kho lưu trữ (repository) từ một registry, mặc định là Docker Hub.
    
    - Ví dụ: `docker pull postgres:15-alpine` 25
        
- `docker push`: Tải một image từ máy cục bộ của bạn lên một registry, cho phép chia sẻ với những người khác hoặc sử dụng trong môi trường production.
    
    - Ví dụ: `docker push your-username/my-app:1.0` 25
        
- `docker rmi` (hoặc `docker image rm`): Xóa một hoặc nhiều image khỏi máy cục bộ để giải phóng dung lượng đĩa.
    
    - Ví dụ: `docker rmi my-app:1.0` 23
        
- `docker inspect <image>`: Cung cấp thông tin chi tiết, ở cấp độ thấp về một image, bao gồm các lớp của nó và siêu dữ liệu (metadata).28
    

### 2.2 Workflow 2: Vòng đời Container

Sau khi có image, bước tiếp theo là tạo và quản lý các thực thể chạy của nó—các container.

- `docker run`: Đây là lệnh trung tâm, kết hợp việc tạo và khởi chạy một container mới từ một image. Nó có nhiều cờ tùy chọn mạnh mẽ:
    
    - `-d` hoặc `--detach`: Chạy container ở chế độ nền (detached mode) và in ra ID của container.29
        
    - `-p <host_port>:<container_port>`: Ánh xạ một cổng trên máy chủ (host) tới một cổng bên trong container, cho phép truy cập ứng dụng từ bên ngoài. Ví dụ: `-p 8080:80`.30
        
    - `--name <container_name>`: Gán một tên cụ thể cho container để dễ dàng tham chiếu thay vì sử dụng ID ngẫu nhiên.23
        
    - `-v <host_path_or_volume_name>:<container_path>`: Gắn một volume hoặc một thư mục từ máy chủ vào container.29
        
    - `-e <VAR_NAME>=<value>`: Thiết lập một biến môi trường bên trong container.23
        
    - Ví dụ đầy đủ: `docker run -d -p 8080:80 --name webserver -e APP_MODE=production nginx:latest`
        
- `docker ps`: Liệt kê tất cả các container đang chạy. Sử dụng cờ `-a` để hiển thị tất cả các container, bao gồm cả những container đã dừng.6
    
- `docker stop <container_name_or_id>`: Dừng một hoặc nhiều container đang chạy một cách nhẹ nhàng (gửi tín hiệu SIGTERM).31
    
- `docker start <container_name_or_id>`: Khởi động lại một hoặc nhiều container đã bị dừng.30
    
- `docker restart <container_name_or_id>`: Dừng và sau đó khởi động lại một container.30
    
- `docker rm <container_name_or_id>`: Xóa một hoặc nhiều container đã dừng. Sử dụng cờ `-f` để buộc xóa một container đang chạy.31
    

### 2.3 Workflow 3: Tương tác và Gỡ lỗi Container

Khi container đang chạy, bạn thường cần phải "nhìn vào bên trong" để gỡ lỗi hoặc thực hiện các tác vụ quản trị.

- `docker logs <container>`: Lấy và hiển thị nhật ký (logs) được tạo ra bởi một container. Cờ `-f` (follow) rất hữu ích để theo dõi luồng log trong thời gian thực, tương tự như lệnh `tail -f` trong Linux.22
    
- `docker exec -it <container> <command>`: Thực thi một lệnh bên trong một container đang chạy. Cờ `-it` (`-i` cho interactive và `-t` cho TTY) cho phép bạn có một phiên làm việc tương tác. Đây là cách phổ biến nhất để "vào" một container.
    
    - Ví dụ: `docker exec -it webserver bash` sẽ mở một phiên shell Bash tương tác bên trong container tên là `webserver`.13
        
- `docker stats`: Hiển thị một luồng trực tiếp về việc sử dụng tài nguyên (CPU, bộ nhớ, mạng I/O) của các container đang chạy, rất hữu ích để theo dõi hiệu suất.28
    

### 2.4 Workflow 4: Dọn dẹp hệ thống

Theo thời gian, Docker có thể tích tụ nhiều đối tượng không sử dụng (container đã dừng, image cũ, volume không được gắn), chiếm dụng không gian đĩa.

- `docker system prune`: Một lệnh dọn dẹp mạnh mẽ, theo mặc định sẽ xóa tất cả các container đã dừng, các mạng không được sử dụng, các image lơ lửng (dangling images - những image không có tag và không được container nào sử dụng), và build cache.22
    
    - `docker system prune -a`: Mở rộng việc dọn dẹp để xóa tất cả các image không được sử dụng (không chỉ là dangling).
        
    - `docker system prune --volumes`: Bao gồm cả việc xóa các volume không được sử dụng.
        

### Bảng tra cứu nhanh các lệnh Docker CLI thiết yếu

Bảng dưới đây tóm tắt các lệnh Docker CLI quan trọng nhất để tham khảo nhanh.

|Lệnh|Mô tả|Ví dụ sử dụng|
|---|---|---|
|`docker build`|Xây dựng một image từ một Dockerfile.|`docker build -t my-app:latest.`|
|`docker run`|Tạo và khởi chạy một container mới từ một image.|`docker run -d -p 80:80 --name web nginx`|
|`docker ps`|Liệt kê các container đang chạy. Sử dụng `-a` để liệt kê tất cả.|`docker ps -a`|
|`docker stop`|Dừng một container đang chạy.|`docker stop web`|
|`docker rm`|Xóa một container đã dừng.|`docker rm web`|
|`docker images`|Liệt kê các image trên máy.|`docker images`|
|`docker rmi`|Xóa một image.|`docker rmi nginx`|
|`docker pull`|Tải một image từ registry.|`docker pull ubuntu:22.04`|
|`docker push`|Đẩy một image lên registry.|`docker push my-username/my-app`|
|`docker exec`|Chạy một lệnh bên trong một container đang chạy.|`docker exec -it web bash`|
|`docker logs`|Xem nhật ký của một container. Sử dụng `-f` để theo dõi.|`docker logs -f web`|
|`docker system prune`|Dọn dẹp các container, network và image không sử dụng.|`docker system prune -a --volumes`|

## Phần 3: Điều phối Ứng dụng với Docker Compose

Khi các ứng dụng trở nên phức tạp hơn, chúng thường bao gồm nhiều thành phần phụ thuộc lẫn nhau—một máy chủ web, một API backend, một cơ sở dữ liệu, một hàng đợi tin nhắn, v.v. Việc quản lý từng container riêng lẻ bằng các lệnh `docker run` dài dòng và phức tạp trở nên không thực tế và dễ gây ra lỗi.33

Đây là lúc Docker Compose tỏa sáng. Docker Compose là một công cụ cho phép định nghĩa và chạy các ứng dụng Docker đa container một cách dễ dàng.35 Với Compose, bạn sử dụng một tệp YAML duy nhất (thường là

`docker-compose.yml`) để cấu hình tất cả các dịch vụ, mạng và volume của ứng dụng. Sau đó, chỉ với một lệnh duy nhất, bạn có thể khởi động hoặc gỡ bỏ toàn bộ hệ thống.37

### 3.1 Cấu trúc của tệp `docker-compose.yml`

Tệp `docker-compose.yml` là trung tâm của việc quản lý ứng dụng với Compose. Nó có cấu trúc khai báo, nghĩa là bạn mô tả "trạng thái mong muốn" của hệ thống, và Compose sẽ thực hiện các bước cần thiết để đạt được trạng thái đó. Các thành phần chính bao gồm:

- **`services`**: Đây là khối chính, nơi bạn định nghĩa mỗi thành phần của ứng dụng như một "dịch vụ". Mỗi dịch vụ tương ứng với một hoặc nhiều container chạy cùng một image.37
    
    - **`image: <image_name>:<tag>`**: Chỉ định image Docker sẽ được sử dụng để tạo container cho dịch vụ này. Compose sẽ tìm image này trên máy cục bộ hoặc tải về từ Docker Hub.39
        
    - **`build: <path_to_context>`**: Thay vì sử dụng một image có sẵn, bạn có thể yêu cầu Compose xây dựng một image tại chỗ từ một `Dockerfile`. Giá trị này là đường dẫn đến thư mục chứa `Dockerfile` (ví dụ: `build:.`).39
        
    - **`ports: - "<host_port>:<container_port>"`**: Ánh xạ cổng giữa máy chủ và container, tương tự cờ `-p` trong `docker run`.38
        
    - **`volumes: - <volume_name_or_host_path>:<container_path>`**: Gắn một volume hoặc một thư mục từ máy chủ vào container. Đây là cách để lưu trữ dữ liệu bền bỉ hoặc chia sẻ tệp giữa máy chủ và container.40
        
    - **`environment: - <VAR_NAME>=<value>`**: Thiết lập các biến môi trường bên trong container. Đây là cách phổ biến để truyền các thông tin cấu hình như thông tin đăng nhập cơ sở dữ liệu, khóa API, v.v..38
        
    - **`networks: - <network_name>`**: Kết nối dịch vụ vào một hoặc nhiều mạng được định nghĩa. Compose tự động tạo một mạng mặc định cho tất cả các dịch vụ trong tệp, nhưng việc định nghĩa mạng tùy chỉnh mang lại sự kiểm soát tốt hơn.39
        
    - **`depends_on: - <service_name>`**: Xác định sự phụ thuộc giữa các dịch vụ. Ví dụ, bạn có thể yêu cầu dịch vụ web chỉ khởi động sau khi dịch vụ cơ sở dữ liệu đã khởi động.38
        
- **`volumes`** (cấp cao nhất): Nơi bạn định nghĩa các "named volumes". Việc khai báo chúng ở đây cho phép chúng được tái sử dụng và quản lý dễ dàng bởi Compose.39
    
- **`networks`** (cấp cao nhất): Nơi bạn định nghĩa các mạng tùy chỉnh. Điều này cho phép bạn tạo ra các cấu trúc liên kết mạng phức tạp hơn và cô lập các nhóm dịch vụ.39
    

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

- `docker compose up`: Lệnh này là trái tim của Compose. Nó đọc tệp `docker-compose.yml`, xây dựng các image cần thiết, tạo và khởi chạy tất cả các container dịch vụ, và tạo các network và volume tương ứng. Nếu không có cờ `-d`, nó sẽ chạy ở chế độ foreground và hiển thị log tổng hợp từ tất cả các container.34
    
    - `docker compose up -d`: Chạy ứng dụng ở chế độ nền (detached). Đây là cách sử dụng phổ biến nhất trong môi trường phát triển và sản xuất.
        
- `docker compose down`: Lệnh này là đối nghịch của `up`. Nó sẽ dừng và xóa tất cả các container, cùng với các network được tạo bởi Compose.
    
    - `docker compose down --volumes`: Thêm cờ này để xóa cả các named volumes đã được định nghĩa trong tệp Compose. Hãy cẩn thận vì điều này sẽ xóa vĩnh viễn dữ liệu.41
        
- `docker compose build`: Nếu bạn đã thay đổi `Dockerfile` của một dịch vụ, lệnh này sẽ buộc xây dựng lại image cho dịch vụ đó trước khi chạy `up`.37
    
- `docker compose logs`: Hiển thị log từ các container dịch vụ.
    
    - `docker compose logs -f <service_name>`: Theo dõi log của một dịch vụ cụ thể trong thời gian thực.41
        
- `docker compose exec <service_name> <command>`: Thực thi một lệnh bên trong một container của một dịch vụ đang chạy. Rất hữu ích để chạy các tác vụ quản trị hoặc mở một shell để gỡ lỗi.
    
    - Ví dụ: `docker compose exec web sh`
        

## Phần 4: Hướng dẫn Thực hành: Container hóa Ứng dụng Dịch vụ đơn

Lý thuyết là nền tảng, nhưng thực hành mới là cách tốt nhất để củng cố kiến thức. Phần này cung cấp các hướng dẫn từng bước để container hóa các ứng dụng đơn giản được viết bằng Go, Node.js và Python, ba trong số các ngôn ngữ phổ biến nhất trong phát triển web hiện đại.

### 4.1 Ví dụ 1: Máy chủ Web Go nhẹ

Go nổi tiếng với việc biên dịch ra các tệp nhị phân tĩnh, độc lập, rất phù hợp với container. Chúng ta sẽ tận dụng tính năng multi-stage build của Docker để tạo ra một image production siêu nhỏ.

1. Mã nguồn (main.go)

Tạo một tệp main.go với nội dung sau. Đây là một máy chủ web đơn giản lắng nghe trên cổng 8080.

Go

```
package main

import (
    "fmt"
    "log"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello from Go in a Docker Container!")
}

func main() {
    http.HandleFunc("/", handler)
    log.Println("Go web server starting on port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

2. Dockerfile

Tạo một tệp tên là Dockerfile (không có phần mở rộng) với nội dung sau:

Dockerfile

```
# Stage 1: Build the application
FROM golang:1.21-alpine AS builder

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code
COPY..

# Build the Go app
# CGO_ENABLED=0 is for static builds
# -o /go-app builds the executable to /go-app
RUN CGO_ENABLED=0 GOOS=linux go build -o /go-app.

# Stage 2: Create the final, lightweight image
FROM alpine:latest

# Copy the pre-built binary file from the previous stage
COPY --from=builder /go-app /go-app

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable
CMD ["/go-app"]
```

**Giải thích Dockerfile:**

- **Stage 1 (`builder`):** Chúng ta bắt đầu với image `golang:1.21-alpine`, chứa tất cả các công cụ cần thiết để biên dịch mã Go. Chúng ta sao chép mã nguồn và biên dịch nó thành một tệp nhị phân tĩnh duy nhất tại `/go-app`.36
    
- **Stage 2 (final):** Chúng ta bắt đầu lại với một image `alpine:latest` siêu nhẹ. Sau đó, chúng ta chỉ sao chép tệp nhị phân đã được biên dịch từ stage `builder` vào image cuối cùng này. Kết quả là một image production chỉ chứa ứng dụng của bạn và không có bất kỳ công cụ build nào.43
    

3. Xây dựng và Chạy

Trước tiên, khởi tạo Go module:

Bash

```
go mod init go-webapp
```

Bây giờ, xây dựng image và chạy container:

Bash

```
# Build the Docker image
docker build -t go-webapp.

# Run the container, mapping port 8080 on the host to 8080 in the container
docker run -p 8080:8080 go-webapp
```

Mở trình duyệt và truy cập `http://localhost:8080` để thấy thông điệp của bạn.

### 4.2 Ví dụ 2: API Node.js & Express năng động

Node.js là một lựa chọn phổ biến cho các API. Quy trình làm việc với Docker cho Node.js tập trung vào việc quản lý các dependencies `npm` một cách hiệu quả.

1. Mã nguồn và Dependencies

Tạo một thư mục dự án và khởi tạo một dự án Node.js:

Bash

```
mkdir node-api && cd node-api
npm init -y
npm install express
```

Tạo một tệp `app.js`:

JavaScript

```
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Node.js & Express in a Docker Container!');
});

app.listen(port, () => {
  console.log(`Node.js API listening on port ${port}`);
});
```

2. Dockerfile

Tạo một tệp Dockerfile:

Dockerfile

```
# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
# This is done separately to take advantage of Docker's layer caching.
# The npm install step will only be re-run if these files change.
COPY package*.json./

# Install app dependencies
RUN npm install

# Bundle app source
COPY..

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the app
CMD [ "node", "app.js" ]
```

**Giải thích Dockerfile:**

- Chúng ta sao chép `package*.json` và chạy `npm install` trước khi sao chép phần còn lại của mã nguồn. Đây là một kỹ thuật tối ưu hóa quan trọng. Vì các dependencies ít thay đổi hơn mã nguồn, Docker có thể tái sử dụng lớp (layer) đã được cache của `npm install`, giúp các lần build sau nhanh hơn đáng kể.44
    

**3. Xây dựng và Chạy**

Bash

```
# Build the Docker image
docker build -t node-api.

# Run the container, mapping port 3000 to 3000
docker run -p 3000:3000 node-api
```

Truy cập `http://localhost:3000` trên trình duyệt của bạn.

### 4.3 Ví dụ 3: Ứng dụng Python & FastAPI hướng dữ liệu

FastAPI là một framework Python hiện đại để xây dựng API. Tương tự như Node.js, việc quản lý dependencies là chìa khóa.

1. Mã nguồn và Dependencies

Tạo một thư mục dự án. Bên trong, tạo tệp requirements.txt:

```
fastapi
uvicorn[standard]
```

Tạo tệp `main.py`:

Python

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Python & FastAPI in a Docker Container!"}
```

2. Dockerfile

Tạo một tệp Dockerfile:

Dockerfile

```
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt.

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY..

# Expose port 8000
EXPOSE 8000

# Run uvicorn server when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Giải thích Dockerfile:**

- Quy trình này tương tự như ví dụ Node.js. Chúng ta cài đặt các dependencies từ `requirements.txt` trước, sau đó sao chép mã nguồn để tận dụng cơ chế cache của Docker.46
    
- Chúng ta sử dụng `python:3.11-slim` làm image cơ sở, đây là một biến thể nhỏ gọn hơn so với image mặc định, giúp giảm kích thước image cuối cùng.
    

**3. Xây dựng và Chạy**

Bash

```
# Build the Docker image
docker build -t python-api.

# Run the container, mapping port 8000 to 8000
docker run -p 8000:8000 python-api
```

Truy cập `http://localhost:8000` để xem kết quả.

## Phần 5: Triển khai Full-Stack: WordPress với PostgreSQL bằng Docker Compose

Đây là phần tổng hợp, nơi chúng ta sẽ áp dụng tất cả các kiến thức đã học để triển khai một ứng dụng web hoàn chỉnh và thực tế: một trang web WordPress được hỗ trợ bởi cơ sở dữ liệu PostgreSQL. Ví dụ này thể hiện sức mạnh thực sự của Docker Compose trong việc điều phối nhiều dịch vụ phụ thuộc lẫn nhau. Đáng chú ý, chúng ta sẽ sử dụng PostgreSQL theo yêu cầu cụ thể, một lựa chọn ít phổ biến hơn so với MySQL/MariaDB trong các hướng dẫn WordPress thông thường, nhưng hoàn toàn khả thi và mạnh mẽ.48

### 5.1 Kiến trúc ứng dụng

Hệ thống của chúng ta sẽ bao gồm các thành phần sau, tất cả được định nghĩa và kết nối trong một tệp `docker-compose.yml` duy nhất:

- **Dịch vụ 1 (`db`):** Một container chạy PostgreSQL, sử dụng image chính thức `postgres:15-alpine`. Đây sẽ là nơi lưu trữ tất cả nội dung của trang WordPress (bài viết, trang, người dùng, v.v.).
    
- **Dịch vụ 2 (`wordpress`):** Một container chạy WordPress, sử dụng image chính thức `wordpress:latest`. Dịch vụ này sẽ chứa máy chủ web (Apache) và PHP để chạy ứng dụng WordPress.
    
- **Volume 1 (`db_data`):** Một named volume để lưu trữ dữ liệu của PostgreSQL. Điều này đảm bảo rằng cơ sở dữ liệu của bạn sẽ tồn tại ngay cả khi container `db` bị xóa và tạo lại.
    
- **Volume 2 (`wp_content`):** Một named volume để lưu trữ các tệp của WordPress, bao gồm themes, plugins và các tệp được tải lên. Điều này cho phép bạn cập nhật phiên bản WordPress mà không làm mất các tùy chỉnh và nội dung của mình.
    
- **Network (`app_net`):** Một mạng bridge tùy chỉnh để hai dịch vụ có thể giao tiếp với nhau một cách an toàn và đáng tin cậy, tách biệt với các container khác có thể đang chạy trên cùng một máy chủ.
    

Việc sử dụng một tệp `docker-compose.yml` để định nghĩa toàn bộ kiến trúc này biến nó thành một dạng "cơ sở hạ tầng dưới dạng mã" (Infrastructure as Code). Tệp này trở thành nguồn chân lý duy nhất cho toàn bộ ứng dụng, có thể được quản lý phiên bản trong Git, chia sẻ với các thành viên trong nhóm và đảm bảo rằng mọi người đều có thể khởi tạo một môi trường giống hệt nhau chỉ bằng một lệnh duy nhất, giúp cải thiện đáng kể quá trình giới thiệu thành viên mới và tính nhất quán.37

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

Mở trình duyệt web và truy cập http://localhost:8000. Bạn sẽ thấy màn hình cài đặt WordPress quen thuộc.48 Hãy làm theo các bước để chọn ngôn ngữ, đặt tên trang web, tạo tài khoản quản trị viên. Tất cả thông tin này sẽ được lưu trữ trong cơ sở dữ liệu PostgreSQL đang chạy trong container

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

## Phần 6: Các Thực tiễn Tốt nhất cho Môi trường Production

Việc đưa các ứng dụng container hóa vào môi trường production đòi hỏi một mức độ cẩn trọng và tối ưu hóa cao hơn so với môi trường phát triển. Phần này sẽ cung cấp các thực tiễn tốt nhất, giúp bạn xây dựng các image nhỏ gọn, an toàn và các tệp Compose có khả năng bảo trì cao, sẵn sàng cho việc triển khai thực tế.

### 6.1 Tối ưu hóa Kích thước và Tốc độ: Multi-Stage Builds

Một trong những vấn đề phổ biến nhất với các Docker image là chúng trở nên cồng kềnh. Một image lớn không chỉ chiếm nhiều dung lượng lưu trữ mà còn làm tăng thời gian tải về và triển khai. Tệ hơn nữa, nó thường chứa các công cụ xây dựng (như JDK, Go toolchain, `build-essentials`) và các dependencies chỉ cần thiết cho quá trình biên dịch, không cần thiết cho việc chạy ứng dụng. Những thành phần thừa này làm tăng bề mặt tấn công của image một cách không cần thiết.51

**Multi-stage builds** là một tính năng mạnh mẽ của Docker để giải quyết vấn đề này.53 Kỹ thuật này cho phép bạn sử dụng nhiều lệnh

`FROM` trong cùng một `Dockerfile`. Mỗi lệnh `FROM` bắt đầu một "stage" (giai đoạn) xây dựng mới.

Cách hoạt động rất đơn giản và hiệu quả:

1. **Stage 1 (Build Stage):** Bạn sử dụng một image cơ sở đầy đủ (ví dụ: `golang:1.21`) có tất cả các công cụ cần thiết để biên dịch, kiểm thử và đóng gói ứng dụng của bạn. Giai đoạn này được đặt tên (ví dụ: `AS builder`).
    
2. **Stage 2 (Final Stage):** Bạn bắt đầu một giai đoạn mới với một image cơ sở tối giản (ví dụ: `alpine:latest` hoặc thậm chí `scratch`—một image trống).
    
3. **Copy Artifacts:** Bạn sử dụng lệnh `COPY --from=builder` để sao chép chỉ những tạo tác (artifacts) cần thiết—chẳng hạn như tệp nhị phân đã biên dịch hoặc các tệp đã được thu nhỏ—từ giai đoạn xây dựng vào giai đoạn cuối cùng.55
    

Ví dụ với ứng dụng Go từ Phần 4 đã minh họa hoàn hảo điều này. Image cuối cùng chỉ chứa tệp nhị phân thực thi và image Alpine cơ sở, giảm kích thước từ hàng trăm MB xuống chỉ còn vài MB.

### 6.2 Tăng cường Bảo mật

Bảo mật là yếu tố không thể bỏ qua khi triển khai. `Dockerfile` của bạn là tuyến phòng thủ đầu tiên.

- **Chạy với người dùng không phải root:** Mặc định, các container chạy với người dùng `root`, điều này tạo ra một rủi ro bảo mật nghiêm trọng. Nếu một kẻ tấn công khai thác được một lỗ hổng trong ứng dụng của bạn và thoát ra khỏi container, chúng có thể có quyền `root` trên máy chủ. Hãy luôn tạo một người dùng và nhóm không có đặc quyền bên trong `Dockerfile` và sử dụng lệnh `USER` để chuyển sang người dùng đó trước khi chạy ứng dụng.56
    
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
    
- **Chọn base image tối giản:** Nguyên tắc là "càng ít càng tốt". Một image cơ sở tối giản như `alpine`, `distroless`, hoặc `scratch` chứa ít thành phần hơn, đồng nghĩa với việc có ít lỗ hổng tiềm tàng hơn và bề mặt tấn công nhỏ hơn.53
    
- **Sử dụng `.dockerignore`:** Tương tự như `.gitignore`, tệp `.dockerignore` ngăn chặn các tệp và thư mục không cần thiết (như `.git`, `node_modules`, các tệp log cục bộ, tệp bí mật) được gửi đến Docker daemon trong quá trình xây dựng. Điều này không chỉ giúp image nhỏ hơn mà còn ngăn chặn việc vô tình rò rỉ thông tin nhạy cảm vào image.57
    

### 6.3 Quản lý các file Compose có thể bảo trì

Khi dự án phát triển, việc quản lý cấu hình cho các môi trường khác nhau (phát triển, kiểm thử, sản xuất) trở nên quan trọng.

- **Sử dụng biến môi trường và tệp `.env`:** **Không bao giờ** ghi cứng các giá trị nhạy cảm như mật khẩu, khóa API, hoặc thông tin đăng nhập cơ sở dữ liệu trực tiếp vào tệp `docker-compose.yml`. Thay vào đó, hãy tham chiếu chúng dưới dạng biến môi trường. Docker Compose sẽ tự động tải các biến từ một tệp `.env` trong cùng thư mục. Tệp `.env` này nên được thêm vào `.gitignore` để đảm bảo nó không được đưa vào hệ thống quản lý phiên bản.58
    
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
        
    
    Khi bạn chạy `docker compose up`, Compose sẽ hợp nhất hai tệp này, tạo ra một cấu hình phát triển hoàn chỉnh. Trong môi trường production, bạn chỉ cần triển khai tệp `docker-compose.yml` cơ sở.58
    

## Conclusion: Tích hợp Container hóa vào Quy trình làm việc của bạn

Hành trình qua thế giới Docker và Docker Compose đã trang bị cho các lập trình viên một bộ công cụ mạnh mẽ để hiện đại hóa quy trình phát triển và triển khai phần mềm. Chúng ta đã đi từ việc tìm hiểu các khái niệm nền tảng—sự khác biệt cốt lõi giữa image và container, tầm quan trọng của volume và network—đến việc làm chủ các lệnh CLI thiết yếu để quản lý vòng đời của chúng.

Thông qua các ví dụ thực tế với Go, Node.js và Python, chúng ta đã thấy cách áp dụng các nguyên tắc này để đóng gói các ứng dụng dịch vụ đơn một cách hiệu quả. Đỉnh cao là việc triển khai một ứng dụng web full-stack, WordPress với PostgreSQL, đã chứng minh sức mạnh của Docker Compose trong việc điều phối các hệ thống phức tạp, đa thành phần chỉ bằng một tệp cấu hình khai báo duy nhất.

Cuối cùng, việc áp dụng các thực tiễn tốt nhất—như multi-stage builds để tối ưu hóa image, các biện pháp bảo mật để làm cứng container, và các chiến lược quản lý tệp Compose để xử lý các môi trường khác nhau—nâng cao kỹ năng từ mức độ "biết dùng" lên "làm chủ".

Docker và Docker Compose là những công cụ không thể thiếu trong bộ công cụ của một lập trình viên hiện đại. Chúng là bước đệm hoàn hảo để hiểu sâu hơn về kiến trúc microservices và là nền tảng vững chắc trước khi tiến vào thế giới điều phối ở quy mô lớn hơn như Kubernetes.62 Bằng cách tích hợp container hóa vào quy trình làm việc hàng ngày, các nhóm phát triển có thể đạt được tốc độ, tính nhất quán và hiệu quả cao hơn bao giờ hết, cho phép họ tập trung vào điều quan trọng nhất: xây dựng những sản phẩm tuyệt vời.