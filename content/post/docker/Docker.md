---
title: Docker
date: 2025-08-13
draft: false
tags:
  - docker
  - vi
---
Sự Ra Đời và Các Nguyên Tắc Cốt Lõi của Docker
<!--more-->

## Phần 1: Cuộc Cách Mạng Container

### 1.1 Giới thiệu về Docker: Tại sao lại là một cuộc cách mạng?

Trong thế giới phát triển phần mềm hiện đại, Docker đã nổi lên như một công nghệ nền tảng, thay đổi cách các lập trình viên xây dựng, vận chuyển và chạy ứng dụng. Về cơ bản, Docker là một nền tảng mã nguồn mở được thiết kế để tự động hóa việc triển khai ứng dụng bên trong các môi trường biệt lập, nhẹ được gọi là container. Mỗi container đóng gói phần mềm cùng với tất cả những gì nó cần để hoạt động—bao gồm thư viện, công cụ hệ thống, mã nguồn và thời gian chạy (runtime)—thành một đơn vị tiêu chuẩn hóa.

Để hiểu rõ giá trị của Docker, điều quan trọng là phải phân biệt nó với công nghệ ảo hóa truyền thống: máy ảo (Virtual Machines - VMs).

- **Máy ảo (VMs):** Một máy ảo ảo hóa toàn bộ phần cứng vật lý, cho phép nhiều hệ điều hành khách (guest OS) chạy trên một máy chủ chủ (host server) duy nhất. Mỗi VM bao gồm một bản sao đầy đủ của một hệ điều hành, các tệp nhị phân và thư viện cần thiết, và chính ứng dụng. Điều này dẫn đến sự cô lập mạnh mẽ nhưng phải trả giá bằng việc tiêu tốn tài nguyên đáng kể, kích thước lớn (hàng gigabyte) và thời gian khởi động chậm.
    
- **Containers:** Ngược lại, container ảo hóa ở cấp độ hệ điều hành. Thay vì đóng gói cả một hệ điều hành khách, các container chia sẻ nhân (kernel) của hệ điều hành máy chủ. Chúng chỉ đóng gói ứng dụng và các dependencies của nó. Kết quả là các container cực kỳ nhẹ (thường chỉ vài chục megabyte), khởi động gần như tức thì và cho phép mật độ ứng dụng cao hơn nhiều trên cùng một phần cứng.
    

Sự thay đổi mô hình này mang lại những lợi ích to lớn, định hình lại toàn bộ vòng đời phát triển phần mềm:

- **Phân phối ứng dụng nhanh chóng, nhất quán:** Docker giải quyết triệt để vấn đề kinh điển "nó chạy trên máy tôi nhưng không chạy trên production". Bằng cách đóng gói ứng dụng và môi trường của nó lại với nhau, Docker đảm bảo tính nhất quán trên các môi trường phát triển, kiểm thử và sản xuất.
    
- **Tính di động (Portability) vượt trội:** Một container được xây dựng trên máy tính xách tay của lập trình viên có thể chạy không thay đổi trên bất kỳ hệ thống nào có cài đặt Docker, cho dù đó là máy chủ vật lý tại chỗ, máy ảo trên đám mây hay trong một môi trường lai.
    
- **Hiệu quả và Tiết kiệm chi phí:** Vì các container nhẹ hơn nhiều so với VM, chúng cho phép chạy nhiều ứng dụng hơn trên cùng một cơ sở hạ tầng. Điều này cải thiện đáng kể việc sử dụng tài nguyên và giúp tiết kiệm chi phí phần cứng và cấp phép.
    
- **Tăng tốc quy trình phát triển (CI/CD):** Docker tích hợp liền mạch vào các quy trình Tích hợp liên tục và Triển khai liên tục (CI/CD). Các image container có thể được xây dựng, kiểm thử và đẩy lên registry một cách tự động, giúp tăng tốc độ phát hành phần mềm một cách đáng kể.
    

Sự phổ biến của Docker không chỉ là một thành tựu kỹ thuật; nó là chất xúc tác trực tiếp cho văn hóa DevOps. Các lợi ích kỹ thuật như môi trường chuẩn hóa 1 và tính di động đã cung cấp cơ chế thực tế để thực hiện các nguyên lý cốt lõi của DevOps: phá vỡ các rào cản giữa phát triển (Dev) và vận hành (Ops), tự động hóa các quy trình, và tăng tần suất triển khai. Docker không chỉ tạo ra một công cụ mới; nó đã biến DevOps từ một triết lý thành một thực tiễn khả thi cho hàng triệu lập trình viên trên toàn thế giới.

### 1.2 Hệ sinh thái Docker: Các Thành phần Cơ bản

Để làm việc hiệu quả với Docker, việc nắm vững các khái niệm và thành phần cốt lõi của nó là điều bắt buộc.

Kiến trúc Docker

Docker hoạt động theo kiến trúc client-server. Thành phần chính bao gồm:

- **Docker Daemon (`dockerd`):** Một dịch vụ nền chạy trên máy chủ, chịu trách nhiệm xây dựng, chạy và quản lý các đối tượng Docker như images, containers, networks và volumes.
    
- **Docker Client (`docker`):** Công cụ dòng lệnh (CLI) mà người dùng tương tác. Khi một lệnh như `docker run` được thực thi, client sẽ gửi yêu cầu đến daemon thông qua REST API qua socket UNIX hoặc giao diện mạng.
    

Images và Containers: Bản thiết kế và Thực thể

Đây là khái niệm cơ bản và quan trọng nhất trong Docker, thường gây nhầm lẫn cho người mới bắt đầu. Một phép ẩn dụ hữu ích là xem Image như một Class trong lập trình hướng đối tượng và Container như một Instance của class đó.

- **Image:** Một Docker image là một mẫu (template) chỉ đọc (read-only) và bất biến (immutable) chứa một tập hợp các chỉ dẫn để tạo ra một container. Nó giống như một bản thiết kế chi tiết, bao gồm mã nguồn ứng dụng, runtime, thư viện, biến môi trường và các tệp cấu hình. Images được xây dựng từ một
    
    `Dockerfile` và bao gồm một loạt các lớp (layers) xếp chồng lên nhau. Mỗi chỉ thị trong Dockerfile tạo ra một lớp mới. Tính bất biến này chính là nguyên nhân trực tiếp tạo ra khả năng tái tạo và tính nhất quán mà Docker cung cấp; vì image không thể thay đổi, mọi container được khởi tạo từ nó đều được đảm bảo giống hệt nhau, loại bỏ hoàn toàn sự trôi dạt môi trường.
    
- **Container:** Một Docker container là một thực thể đang chạy (a running instance) của một image. Khi Docker tạo một container từ một image, nó sẽ thêm một lớp có thể ghi (writable layer) lên trên các lớp chỉ đọc của image. Bất kỳ thay đổi nào được thực hiện bên trong container—chẳng hạn như tạo tệp mới, sửa đổi cấu hình, hoặc cài đặt phần mềm—đều được ghi vào lớp này. Điều này có nghĩa là nhiều container có thể chia sẻ cùng một image cơ sở trong khi vẫn duy trì trạng thái riêng biệt của chúng.
    

Dockerfile: Công thức để tạo Image

Dockerfile là một tệp văn bản đơn giản chứa các hướng dẫn từng bước để Docker tự động xây dựng một image. Mỗi lệnh (ví dụ:

`FROM`, `COPY`, `RUN`, `CMD`) trong Dockerfile tương ứng với một lớp trong image. Cấu trúc phân lớp này rất hiệu quả vì Docker sẽ lưu trữ (cache) các lớp; khi bạn xây dựng lại image, chỉ những lớp đã thay đổi kể từ lần xây dựng trước mới được tạo lại, giúp quá trình xây dựng nhanh hơn đáng kể.

Volumes: Lưu trữ dữ liệu bền bỉ

Bản chất của container là tạm thời (ephemeral). Khi một container bị xóa, lớp ghi của nó cũng bị xóa theo, và mọi dữ liệu được tạo ra trong đó sẽ bị mất vĩnh viễn. Đối với các ứng dụng cần lưu trữ dữ liệu lâu dài (ứng dụng có trạng thái - stateful), chẳng hạn như cơ sở dữ liệu hoặc hệ thống quản lý nội dung, điều này là không thể chấp nhận được.

**Volumes** là giải pháp của Docker cho vấn đề này. Chúng là một cơ chế lưu trữ bền bỉ được quản lý hoàn toàn bởi Docker và tồn tại độc lập với vòng đời của bất kỳ container nào. Dữ liệu trong một volume có thể được chia sẻ giữa nhiều container và vẫn tồn tại ngay cả khi tất cả các container sử dụng nó đã bị xóa. Đây là phương pháp được khuyến nghị để xử lý dữ liệu cho các ứng dụng stateful.

Networks: Giao tiếp giữa các Container

Mặc định, các container được cô lập với nhau. Để cho phép chúng giao tiếp, Docker cung cấp một hệ thống mạng ảo mạnh mẽ. Khi Docker khởi động, nó tạo ra một số mạng mặc định. Các loại mạng chính bao gồm:

- **`bridge`:** Đây là mạng mặc định cho các container. Các container được kết nối với cùng một mạng bridge có thể giao tiếp với nhau bằng tên container của chúng, nhờ vào hệ thống DNS tích hợp của Docker. Chúng được cô lập với các container trên các mạng bridge khác.
    
- **`host`:** Loại bỏ sự cô lập mạng giữa container và máy chủ Docker. Container chia sẻ trực tiếp không gian mạng của máy chủ. Điều này cung cấp hiệu suất mạng tốt hơn nhưng làm mất đi lợi ích của sự cô lập.
    
- **`overlay`:** Được sử dụng để kết nối các container chạy trên nhiều máy chủ Docker khác nhau, tạo thành một mạng ảo duy nhất. Đây là nền tảng cho các công cụ điều phối như Docker Swarm.
    

*Phần 2: [Docker CLI](https://blog.nagih.io.vn/post/docker/docker-cli/)

*Phần 3: [Docker Compose](https://blog.nagih.io.vn/post/docker/docker-compose/)

*Phần 4: [Docker Practical Guide](https://blog.nagih.io.vn/post/docker/docker-practical-guide/)

*Phần 5: [Docker Fullstack Example](https://blog.nagih.io.vn/post/docker/docker-fullstack-example/)

*Phần 6: [Docker Best Practice for Production](https://blog.nagih.io.vn/post/docker/docker-best-practice-for-production/)

## Kết luận

Hành trình qua thế giới Docker và Docker Compose đã trang bị cho các lập trình viên một bộ công cụ mạnh mẽ để hiện đại hóa quy trình phát triển và triển khai phần mềm. Chúng ta đã đi từ việc tìm hiểu các khái niệm nền tảng—sự khác biệt cốt lõi giữa image và container, tầm quan trọng của volume và network—đến việc làm chủ các lệnh CLI thiết yếu để quản lý vòng đời của chúng.

Thông qua các ví dụ thực tế với Go, Node.js và Python, chúng ta đã thấy cách áp dụng các nguyên tắc này để đóng gói các ứng dụng dịch vụ đơn một cách hiệu quả. Đỉnh cao là việc triển khai một ứng dụng web full-stack, WordPress với PostgreSQL, đã chứng minh sức mạnh của Docker Compose trong việc điều phối các hệ thống phức tạp, đa thành phần chỉ bằng một tệp cấu hình khai báo duy nhất.

Cuối cùng, việc áp dụng các thực tiễn tốt nhất—như multi-stage builds để tối ưu hóa image, các biện pháp bảo mật để làm cứng container, và các chiến lược quản lý tệp Compose để xử lý các môi trường khác nhau—nâng cao kỹ năng từ mức độ "biết dùng" lên "làm chủ".

Docker và Docker Compose là những công cụ không thể thiếu trong bộ công cụ của một lập trình viên hiện đại. Chúng là bước đệm hoàn hảo để hiểu sâu hơn về kiến trúc microservices và là nền tảng vững chắc trước khi tiến vào thế giới điều phối ở quy mô lớn hơn như Kubernetes. Bằng cách tích hợp container hóa vào quy trình làm việc hàng ngày, các nhóm phát triển có thể đạt được tốc độ, tính nhất quán và hiệu quả cao hơn bao giờ hết, cho phép họ tập trung vào điều quan trọng nhất: xây dựng những sản phẩm tuyệt vời.

*Nếu thấy hay, hãy để lại cho mình xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*