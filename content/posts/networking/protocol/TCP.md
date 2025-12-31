---
title: Tổng quan về TCP
date: 2025-10-13
image:
categories:
  - network
  - protocol
tags:
  - TCP
draft: false
---
**Transmission Control Protocol** (Giao thức điều khiển truyền vận), là một giao thức cốt lõi trong bộ giao thức Internet (TCP/IP)

<!--more-->

---
## TCP là gì?

TCP hoạt động ở tầng Giao vận (Transport Layer - Tầng 4 trong mô hình OSI. Nhiệm vụ chính của TCP là đảm bảo dữ liệu được truyền đi một cách **đáng tin cậy** và **đúng thứ tự** giữa các ứng dụng trên các thiết bị mạng khác nhau.

Hãy tưởng tượng bạn gửi một bức thư dài qua đường bưu điện. Thay vì gửi cả tập giấy dày, bạn chia nhỏ nó thành nhiều trang, đánh số thứ tự mỗi trang và gửi từng trang riêng lẻ. TCP cũng làm điều tương tự với dữ liệu của bạn. Nó chia dòng dữ liệu lớn thành các gói tin nhỏ hơn gọi là **segment** (phân đoạn).

TCP thường hoạt động cùng với Giao thức IP. Trong khi IP chịu trách nhiệm tìm đường và gửi các gói tin đến đúng địa chỉ đích, TCP đảm bảo rằng tất cả các gói tin này đến nơi an toàn, không lỗi và được lắp ráp lại theo đúng thứ tự ban đầu. Sự kết hợp này được gọi là **TCP/IP**, là nền tảng cho hầu hết các hoạt động trên Internet ngày nay.

---
## Các đặc điểm chính của TCP

TCP được biết đến là một giao thức "hướng kết nối" (connection-oriented) và đáng tin cậy. Điều này có nghĩa là trước khi bất kỳ dữ liệu nào được gửi đi, một kết nối ảo phải được thiết lập giữa máy gửi và máy nhận. Các đặc điểm nổi bật của TCP bao gồm:
	
*   **Độ tin cậy cao:** TCP đảm bảo dữ liệu đến đích một cách toàn vẹn. Nó sử dụng cơ chế kiểm tra lỗi (checksum), gửi lại các gói tin bị mất và loại bỏ các gói tin trùng lặp.
	
*   **Đảm bảo đúng thứ tự:** Mỗi segment được gán một "số thứ tự" (sequence number). Bên nhận sẽ dựa vào số này để sắp xếp lại các segment theo đúng thứ tự ban đầu, đảm bảo dữ liệu không bị xáo trộn.
	
*   **Kiểm soát luồng (Flow Control):** TCP sử dụng một cơ chế gọi là "cửa sổ trượt" (sliding window) để điều chỉnh tốc độ truyền dữ liệu. Điều này giúp bên gửi không làm quá tải bên nhận bằng cách gửi dữ liệu nhanh hơn khả năng xử lý của nó.
	
*   **Kiểm soát tắc nghẽn (Congestion Control):** TCP có khả năng phát hiện tình trạng tắc nghẽn mạng và tự động giảm tốc độ truyền để tránh làm tình hình tệ hơn.
	
---
## TCP hoạt động như thế nào? Quy trình "Bắt tay ba bước"

Hoạt động của TCP có thể được chia thành ba giai đoạn chính: thiết lập kết nối, truyền dữ liệu và kết thúc kết nối.

### 1. Thiết lập kết nối: Bắt tay ba bước (Three-Way Handshake)

Đây là quy trình bắt buộc để thiết lập một kết nối TCP đáng tin cậy. Quá trình này diễn ra như sau:

*   **Bước 1 (SYN):** Máy khách (Client) muốn bắt đầu kết nối sẽ gửi một gói tin có cờ **SYN** (Synchronize) đến máy chủ (Server). Gói tin này về cơ bản là một lời chào: "Chào Server, tôi muốn kết nối. Số thứ tự bắt đầu của tôi là X."
	
*   **Bước 2 (SYN-ACK):** Server nhận được gói SYN, nếu đồng ý kết nối, nó sẽ gửi lại một gói tin có cả cờ **SYN** và **ACK** (Acknowledgement). Gói tin này có ý nghĩa: "Chào Client, tôi đã nhận được yêu cầu của bạn (ACK X+1). Tôi cũng sẵn sàng kết nối. Số thứ tự bắt đầu của tôi là Y."
	
*   **Bước 3 (ACK):** Client nhận được gói SYN-ACK từ Server. Để hoàn tất quá trình, Client gửi lại một gói tin chỉ có cờ **ACK**. Gói tin này xác nhận: "Tôi đã nhận được gói tin của Server (ACK Y+1). Kết nối đã được thiết lập!"

Sau khi hoàn thành 3 bước này, một kết nối ổn định được tạo ra và quá trình truyền dữ liệu có thể bắt đầu.

### 2. Truyền dữ liệu

Khi kết nối đã được thiết lập, dữ liệu sẽ được chia thành các segment và gửi đi.

*   Bên gửi sẽ gửi một lượng dữ liệu (trong giới hạn của cửa sổ trượt).
	
*   Bên nhận sau khi nhận được dữ liệu sẽ gửi lại một gói tin ACK để xác nhận.
	
*   Nếu bên gửi không nhận được ACK trong một khoảng thời gian nhất định, nó sẽ tự động gửi lại segment đó.

### 3. Kết thúc kết nối: Bắt tay bốn bước (Four-Way Handshake)

Khi quá trình truyền dữ liệu hoàn tất, kết nối sẽ được đóng lại thông qua một quy trình "bắt tay bốn bước" để đảm bảo cả hai bên đều đồng ý chấm dứt.

*   Một bên (ví dụ: Client) gửi một gói tin **FIN** (Finish) để thông báo muốn kết thúc.
	
*   Bên kia (Server) gửi lại một gói **ACK** để xác nhận đã nhận được yêu cầu.
	
*   Sau đó, Server cũng gửi một gói **FIN** của riêng mình.
	
*   Cuối cùng, Client gửi lại một gói **ACK** để xác nhận, và kết nối được đóng hoàn toàn.

## So sánh TCP và UDP

Trong tầng Giao vận, ngoài TCP còn có một giao thức quan trọng khác là **UDP (User Datagram Protocol)**. Dưới đây là bảng so sánh nhanh giữa hai giao thức này:

| Đặc điểm              | TCP (Transmission Control Protocol)                              | UDP (User Datagram Protocol)                                                           |
| :-------------------- | :--------------------------------------------------------------- | :------------------------------------------------------------------------------------- |
| **Kiểu kết nối**      | Hướng kết nối (Connection-oriented)                              | Không kết nối (Connectionless)                                                         |
| **Độ tin cậy**        | Rất cao. Đảm bảo dữ liệu đến nơi, đúng thứ tự, không lỗi.        | Không đáng tin cậy. Không đảm bảo dữ liệu có đến đích hay không, không sắp xếp thứ tự. |
| **Tốc độ**            | Chậm hơn do các cơ chế kiểm tra, xác nhận và thiết lập kết nối.  | Rất nhanh do không có các quy trình phức tạp.                                          |
| **Kiểm soát luồng**   | Có                                                               | Không                                                                                  |
| **Header**            | Lớn hơn (tối thiểu 20 bytes) do chứa nhiều thông tin điều khiển. | Nhỏ hơn (8 bytes), giúp giảm thiểu dữ liệu thừa.                                       |
| **Ứng dụng phổ biến** | Truy cập web (HTTP/HTTPS), gửi email (SMTP), truyền file (FTP).  | Streaming video/audio, game online, gọi VoIP, DNS.                                     |

### Khi nào nên sử dụng TCP?

TCP là lựa chọn lý tưởng cho các ứng dụng đòi hỏi **tính toàn vẹn và độ chính xác của dữ liệu là ưu tiên hàng đầu**. Nếu việc mất một vài gói tin có thể gây ra lỗi nghiêm trọng (ví dụ như tải một tệp tin bị hỏng, email bị mất nội dung), thì TCP là giao thức bắt buộc phải sử dụng.

---
