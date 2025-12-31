---
title: REST và gRPC
date: 2025-08-28
image: /image-placeholder.png
categories:
  - network
  - protocol
tags:
  - rest
  - grpc
draft: false
---

Phân Tích về Kiến Trúc API Hiện Đại | Rest & gRPC

<!--more-->

## Giới thiệu

REST, với tư cách là một kiểu kiến trúc, đã định hình nên các API web trong hơn hai thập kỷ, trở thành tiêu chuẩn de facto nhờ tính linh hoạt và khả năng tiếp cận phổ quát. Mặt khác, gRPC, một framework mã nguồn mở hiệu suất cao do Google phát triển, nổi lên như một giải pháp được thiết kế đặc biệt cho kỷ nguyên microservice, nơi hiệu suất, độ trễ thấp và các hợp đồng dịch vụ nghiêm ngặt là tối quan trọng.
## REST

REST không phải là một giao thức hay một tiêu chuẩn, mà là một _kiểu kiến trúc_ (architectural style) được định nghĩa bởi Roy Fielding vào năm 2000. Một hệ thống được coi là "RESTful" khi nó tuân thủ một tập hợp các ràng buộc kiến trúc được thiết kế để tối ưu hóa cho một hệ thống phân tán quy mô lớn như World Wide Web.

### Kiến trúc cốt lõi của REST

Sức mạnh và sự phổ biến của REST bắt nguồn từ sáu ràng buộc sau:

-   **Tách Biệt Client-Server (Client-Server Decoupling):** Server và client chỉ tương tác thông qua một giao diện chuẩn hóa. Sự tách biệt này cho phép chúng phát triển độc lập - client không cần biết về logic nghiệp vụ của server, và server không cần biết về giao diện của client miễn là hợp đồng giao diện không thay đổi.
	
-   **Vô Trạng Thái (Statelessness):** Trong kiến trúc REST, mỗi yêu cầu từ client đến server phải chứa tất cả thông tin cần thiết để server hiểu và xử lý nó. Server không lưu trữ bất kỳ trạng thái phiên nào của client giữa các yêu cầu. 
	
-   **Giao Diện Đồng Nhất (Uniform Interface):** Được thiết kế để đơn giản hóa và tách rời kiến trúc. Nó bao gồm 4 ràng buộc con:Đ
	
    -   **Identification of resources:** Mọi tài nguyên đều được định danh duy nhất thông qua một URI (Uniform Resource Identifier). 
	    
	    - Ví dụ: `https://.../osers/123` thì 123 là ID duy nhất của order đó.
		
    -   **Manipulation of resources through representations:** Client tương tác với tài nguyên thông qua các biểu diễn của chúng (ví dụ: một tài liệu JSON hoặc XML). Biểu diễn này chứa đủ thông tin để client có thể sửa đổi hoặc xóa tài nguyên trên server.
		
    -   **Self-descriptive:** Mỗi thông điệp chứa đủ thông tin để mô tả cách xử lý nó. Ví dụ, một header `Content-Type` cho biết định dạng media của thông điệp.
		
    -   **HATEOAS:** Client chỉ cần biết URI khởi đầu. Sau đó, tất cả các hành động và tài nguyên trong tương lai mà client có thể truy cập đều được khám phá thông qua các siêu liên kết có trong các phản hồi từ server.
	
-   **Cacheability:** Cho phép client hoặc các máy chủ trung gian lưu trữ các phản hồi, giúp giảm độ trễ và tải cho server.
	
-   **Layered System:** Client không thể biết liệu nó đang kết nối trực tiếp đến server cuối cùng hay một máy chủ trung gian _(microservices)_.
	
-   **Code on Demand:** Đây là ràng buộc duy nhất không bắt buộc. Nó cho phép server tạm thời mở rộng hoặc tùy chỉnh chức năng của client bằng cách truyền mã thực thi (ví dụ: JavaScript).
### Triển khai đển hình

Thông thường, REST được triển khai trên HTTP/1.1. Các tài nguyên được thao tác bằng HTTP tiêu chuẩn (GET, POST, PUT, DELETE), và dữ liệu thường được trao đổi bằng định dạng JSON.

## Framework gRPC - Hiệu Suất và Gọi Thủ Tục Từ Xa

gRPC (gRPC Remote Procedure Call) là một framework RPC hiện đại, được xây dựng trên nền tảng các công nghệ hiệu suất cao. Thay vì tập trung vào tài nguyên, gRPC tập trung vào các dịch vụ và các thủ tục (hàm) mà client có thể gọi từ xa. Kiến trúc của nó được xây dựng trên ba trụ cột chính: Protocol Buffers, HTTP/2, và các mô hình streaming tiên tiến.

### Mô Hình RPC

Cốt lõi của gRPC là mô hình Gọi Thủ Tục Từ Xa (Remote Procedure Call). Ý tưởng là cho phép một client gọi một hàm trên một server từ xa một cách minh bạch, như thể nó là một lời gọi hàm cục bộ. Framework sẽ trừu tượng hóa toàn bộ quá trình giao tiếp mạng phức tạp, bao gồm tuần tự hóa dữ liệu, kết nối và xử lý lỗi.

### 1. Protocol Buffers (Protobuf)

Protobuf là Ngôn ngữ Định nghĩa Giao diện (Interface Definition Language - IDL) mặc định của gRPC. Nó đóng vai trò là bản thiết kế cho cả dịch vụ và cấu trúc dữ liệu.

-   **Design-first:** Với gRPC, bắt đầu bằng cách định nghĩa các dịch vụ cấu trúc dữ liệu trong một tệp `.proto`. Tệp này hoạt động như một hợp đồng chính thức giữa client và server.
	
-   **Tạo mã tự động:** Trình biên dịch `protoc` của Protobuf sau đó sẽ đọc tệp `.proto` này và tự động tạo ra các client stub (phía client) và server skeleton (phía server) với kiểu dữ liệu mạnh (strongly-typed).

### 2. Giao thức HTTP/2

gRPC được xây dựng nguyên bản trên HTTP/2, một bản nâng cấp lớn so với HTTP/1.1, và tận dụng triệt để các tính năng của nó để đạt được hiệu suất vượt trội.

-   **Binary Framing:** HTTP/2 truyền dữ liệu dưới dạng các khung nhị phân, hiệu quả hơn so với định dạng văn bản của HTTP/1.1.
	
-   **Full Multiplexing:** Đây là tính năng đột phá nhất. HTTP/2 cho phép gửi và nhận nhiều yêu cầu và phản hồi đồng thời trên một kết nối TCP duy nhất, loại bỏ hoàn toàn vấn đề "chặn đầu hàng" (head-of-line blocking) của HTTP/1.1.
	
-   **Header Compression:** Sử dụng thuật toán HPACK, HTTP/2 nén các header của yêu cầu và phản hồi, giảm đáng kể dữ liệu dư thừa và chi phí mạng.
	
-   **Hỗ trợ streaming nguyên bản:** HTTP/2 được thiết kế để hỗ trợ streaming dữ liệu, một nền tảng cơ bản cho các mô hình giao tiếp tiên tiến của gRPC.

### 3. Các mô hình Streaming tiên tiến

Nhờ vào nền tảng HTTP/2, gRPC hỗ trợ bốn mô hình giao tiếp, mang lại sự linh hoạt vượt trội so với mô hình yêu cầu-phản hồi đơn lẻ của REST:

-   **Unary RPC:** Mô hình yêu cầu-phản hồi cổ điển, tương tự như một lời gọi REST. Client gửi một yêu cầu duy nhất và nhận lại một phản hồi duy nhất.
	
-   **Server Streaming RPC:** Client gửi một yêu cầu và nhận lại một luồng (stream) các phản hồi từ server. Rất hữu ích cho các trường hợp như đăng ký nhận thông báo hoặc cập nhật dữ liệu trực tiếp.
	
-   **Client Streaming RPC:** Client gửi một luồng các thông điệp đến server, và server sẽ phản hồi bằng một thông điệp duy nhất sau khi đã nhận tất cả. Thích hợp cho việc tải lên các tệp lớn hoặc gửi dữ liệu đo lường từ xa.
	
-   **Bidirectional Streaming RPC:** Cả client và server đều có thể gửi các luồng thông điệp cho nhau một cách độc lập trên cùng một kết nối. Mô hình này lý tưởng cho các ứng dụng tương tác thời gian thực như chat hoặc game nhiều người chơi.

## Bảng So Sánh Tổng Quan

| Tiêu Chí                       | REST                                                          | gRPC                                                               |
| ------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Mô hình**                    | Dựa trên tài nguyên (Resource-based)                          | Gọi thủ tục từ xa (RPC)                                            |
| **Tiêu chuẩn hóa**             | Không có tiêu chuẩn chính thức, là một tập hợp các nguyên tắc | Được định nghĩa rõ ràng và chi tiết                                |
| **Giao thức vận chuyển**       | Thường là HTTP/1.1 (có thể dùng HTTP/2)                       | HTTP/2                                                             |
| **Định dạng dữ liệu mặc định** | JSON (cũng hỗ trợ XML, text, v.v.)                            | Protocol Buffers (Protobuf)                                        |
| **Các chế độ dịch vụ**         | Chỉ Unary (yêu cầu-phản hồi đơn lẻ)                           | Unary, Client streaming, Server streaming, Bidirectional streaming |
| **Thiết kế API**               | Thường là Code-first (mã trước)                               | Design-first (thiết kế trước)                                      |
| **Mức độ ghép nối**            | Ghép nối lỏng (Loosely coupled)                               | Ghép nối chặt (Tightly coupled)                                    |
| **Tạo mã**                     | Yêu cầu công cụ bên thứ ba (ví dụ: OpenAPI Generator)         | Tích hợp sẵn (thông qua trình biên dịch `protoc`)                  |
| **Hỗ trợ trình duyệt**         | Hỗ trợ nguyên bản và phổ quát                                 | Yêu cầu lớp proxy (gRPC-Web)                                       |
| **Lưu cache**                  | Hỗ trợ tốt thông qua các cơ chế HTTP tiêu chuẩn               | Không hỗ trợ mặc định, cần tự triển khai                           |

## Triết Lý và Thiết Kế

Sự khác biệt cơ bản nhất giữa REST và gRPC nằm ở triết lý thiết kế của chúng: "cái gì" so với "làm gì".
	
-   **REST:** Tập trung vào việc phơi bày các _thực thể_ hoặc _tài nguyên_ (danh từ). Client tương tác với các tài nguyên này bằng CRUD (Create, Read, Update, Delete) và các nguyên tắc lập trình hướng đối tượng.
	
-   **gRPC:** Tập trung vào việc phơi bày các _hành động_ hoặc _thủ tục_ (động từ). Client gọi các hàm cụ thể trên server, ví dụ `CreateUser(user_details)`. Đây là một thiết kế hướng dịch vụ, ánh xạ trực tiếp đến logic ứng dụng.
	

> Có một mối quan hệ nghịch đảo giữa sự dễ dàng trong thiết lập/gỡ lỗi ban đầu và khả năng bảo trì lâu dài trong các hệ thống đa ngôn ngữ. REST rất dễ bắt đầu, nhưng có thể dẫn đến các vấn đề tích hợp sau này do thiếu một hợp đồng chính thức. gRPC đòi hỏi nhiều công sức thiết lập hơn (định nghĩa tệp `.proto`, tạo mã), nhưng nó cung cấp một nền tảng vững chắc, an toàn về kiểu dữ liệu giúp ngăn ngừa các lỗi tích hợp, đặc biệt là trong kiến trúc microservices với nhiều nhóm và ngôn ngữ khác nhau.