---
title: Tổng quan về mô hình OSI
date: 2025-10-12
image:
categories:
  - network
tags:
  - OSI
draft: false
---

Open Systems Interconnection - OSI là một khung khái niệm chia các chức năng truyền thông mạng thành 7 lớp hay 7 tầng riêng biệt. Được phát triển bởi Tổ chức Tiêu chuẩn hóa Quốc tế (ISO)

<!--more-->

---
## Cấu trúc 7 tầng của mô hình OSI

Quá trình truyền dữ liệu trong mô hình OSI diễn ra theo thứ tự từ tầng ứng dụng (tầng 7) đi xuống tầng vật lý (tầng 1) ở máy gửi, và ngược lại ở máy nhận. Mỗi tầng có những chức năng cụ thể và có thêm thêm header (thông tin điều khiển) của riêng mình vào dữ liệu trước khi chuyển xuống tầng tiếp theo. Quá trình này gọi là "đóng gói dữ liệu".

---

### Tầng 7: Application Layer

Đây là tầng gần gũi nhất với người dùng. Nó cung cấp giao diện để các ứng dụng phần mềm có thể truy cập và sử dụng các dịch vụ mạng.

*   **Chức năng chính:**
	
    *   Cung cấp các dịch vụ mạng cho ứng dụng của người dùng như truy cập web, gửi/nhận email, truyền file.
		
    *   Xác định các giao thức mà ứng dụng sử dụng để trao đổi dữ liệu.
	
*   **Ví dụ thực tế:** Khi bạn sử dụng trình duyệt web, email hoặc một phần mềm chat, bạn đang tương tác với tầng ứng dụng. Các giao thức phổ biến ở tầng này bao gồm HTTP/HTTPS (truy cập web), FTP (truyền tệp), SMTP (gửi email), và DNS (hệ thống phân giải tên miền).

---

### Tầng 6: Presentation Layer

Tầng này hoạt động như một "người phiên dịch" của mạng, đảm bảo rằng dữ liệu được gửi từ tầng ứng dụng của một hệ thống có thể được đọc và hiểu bởi tầng ứng dụng của hệ thống khác.

*   **Chức năng chính:**
	
    *   **Định dạng dữ liệu:** Chuyển đổi dữ liệu sang một định dạng chung mà mạng có thể hiểu.
		
    *   **Mã hóa và giải mã:** Đảm bảo tính bảo mật và bí mật của dữ liệu trong quá trình truyền.
		
    *   **Nén và giải nén:** Giảm kích thước dữ liệu để truyền đi nhanh hơn và tiết kiệm băng thông.
	
*   **Ví dụ thực tế:** Mã hóa HTTPS thông qua SSL/TLS thường được coi là hoạt động ở tầng này. Các định dạng tệp hình ảnh (JPEG, GIF) và video (MPEG) cũng là ví dụ về hoạt động của tầng trình bày.

---

### Tầng 5: Session Layer

Tầng này chịu trách nhiệm thiết lập, quản lý và kết thúc các phiên giao tiếp (kết nối) giữa hai máy tính.

*   **Chức năng chính:**
	
    *   **Thiết lập và quản lý phiên:** Tạo, duy trì và đồng bộ hóa các phiên giao tiếp giữa các ứng dụng.
		
    *   **Điều khiển đối thoại:** Xác định lượt truyền dữ liệu (ai gửi, ai nhận, và trong bao lâu).
		
    *   **Khôi phục phiên:** Nếu một phiên bị gián đoạn, tầng này có thể giúp khôi phục lại từ một điểm kiểm tra (checkpoint), tránh việc phải truyền lại toàn bộ dữ liệu.
	
*   **Ví dụ thực tế:** Khi bạn thực hiện một cuộc gọi video, tầng phiên sẽ duy trì kết nối ổn định trong suốt cuộc gọi. Các giao thức như NetBIOS, RPC cũng hoạt động ở tầng này.

---

### Tầng 4: Transport Layer

Tầng vận chuyển đảm bảo việc truyền dữ liệu hoàn chỉnh và đáng tin cậy từ một tiến trình trên máy gửi đến một tiến trình trên máy nhận.

*   **Chức năng chính:**
	
    *   **Phân đoạn và tái lắp ráp:** Chia nhỏ dữ liệu từ tầng phiên thành các đoạn (segment) nhỏ hơn để truyền đi và tập hợp chúng lại ở phía nhận.
		
    *   **Kiểm soát luồng:** Điều chỉnh tốc độ truyền dữ liệu để tránh làm quá tải thiết bị nhận.
		
    *   **Kiểm soát lỗi:** Đảm bảo dữ liệu đến nơi một cách chính xác, không bị lỗi, mất mát hay trùng lặp.
		
    *   Cung cấp hai loại giao thức chính:
		
        *   **TCP (Transmission Control Protocol):** Hướng kết nối, đảm bảo độ tin cậy cao (dữ liệu được gửi đầy đủ và đúng thứ tự). Thích hợp cho việc tải tệp, gửi email.
			
        *   **UDP (User Datagram Protocol):** Không kết nối, truyền dữ liệu nhanh hơn nhưng không đảm bảo độ tin cậy. Thích hợp cho streaming video, game online.
	
---

### Tầng 3: Network Layer

Tầng mạng chịu trách nhiệm cho việc định địa chỉ logic và định tuyến các gói tin (packet) qua các mạng khác nhau để đến đúng đích.

*   **Chức năng chính:**
	
    *   **Định địa chỉ logic (Logical Addressing):** Gán địa chỉ IP cho các thiết bị để xác định chúng trên mạng.
		
    *   **Định tuyến (Routing):** Xác định con đường tốt nhất để các gói tin di chuyển từ nguồn đến đích qua nhiều mạng khác nhau. Các thiết bị định tuyến (router) hoạt động ở tầng này.
	
*   **Ví dụ thực tế:** Khi bạn truy cập một trang web, tầng mạng sẽ xác định đường đi cho dữ liệu của bạn qua Internet để đến được máy chủ của trang web đó. Giao thức IP (Internet Protocol) là giao thức chính ở tầng này.

---

### Tầng 2: Data Link Layer

Tầng này cung cấp phương tiện truyền dữ liệu đáng tin cậy qua một liên kết vật lý trực tiếp. Nó nhận các gói tin từ tầng mạng và đóng gói chúng thành các khung (frame).

*   **Chức năng chính:**
	
    *   **Định địa chỉ vật lý (Physical Addressing):** Thêm địa chỉ MAC (Media Access Control) của thiết bị gửi và nhận vào mỗi khung. Địa chỉ MAC là duy nhất cho mỗi card mạng.
		
    *   **Kiểm soát lỗi:** Phát hiện và sửa lỗi có thể xảy ra ở tầng vật lý.
		
    *   **Kiểm soát truy cập môi trường (Media Access Control - MAC):** Điều khiển việc các thiết bị trên cùng một mạng chia sẻ truy cập vào môi trường truyền.
	
*   **Ví dụ thực tế:** Các thiết bị chuyển mạch (switch) hoạt động ở tầng này. Giao thức Ethernet là một ví dụ điển hình.

---

### Tầng 1: Physical Layer

Đây là tầng thấp nhất, chịu trách nhiệm truyền các bit dữ liệu (0 và 1) qua môi trường truyền vật lý.

*   **Chức năng chính:**
	
    *   **Định nghĩa các đặc tính vật lý:** Quy định về các thiết bị phần cứng như cáp mạng, đầu nối, card mạng, cũng như các đặc tính về điện, cơ và quang.
		
    *   **Biểu diễn bit:** Chuyển đổi các bit 0 và 1 thành các tín hiệu điện, ánh sáng hoặc sóng vô tuyến để truyền đi.
		
    *   **Tốc độ dữ liệu:** Xác định số bit được truyền đi mỗi giây.
	
*   **Ví dụ thực tế:** Cáp đồng, cáp quang, sóng Wi-Fi, hub, và repeater là những ví dụ về các thành phần hoạt động ở tầng vật lý.

## Ưu và nhược điểm của mô hình OSI

**Ưu điểm:**
	
*   **Chuẩn hóa:** Tạo ra một tiêu chuẩn chung, giúp các nhà sản xuất khác nhau tạo ra các sản phẩm tương thích.
	
*   **Giảm độ phức tạp:** Chia nhỏ quá trình truyền thông phức tạp thành các phần đơn giản, dễ quản lý và dễ hiểu hơn.
	
*   **Hỗ trợ kỹ thuật module:** Cho phép thay đổi hoặc phát triển công nghệ ở một tầng mà không ảnh hưởng đến các tầng khác.
	
*   **Dễ dàng khắc phục sự cố:** Giúp các kỹ sư mạng xác định vấn đề xảy ra ở tầng nào một cách nhanh chóng.
	
**Nhược điểm:**
	
*   **Tính lý thuyết:** Mô hình OSI chỉ là một mô hình tham chiếu và không được triển khai rộng rãi trong thực tế như mô hình TCP/IP.
	
*   **Phức tạp:** Một số người cho rằng mô hình 7 tầng là quá phức tạp và một số tầng có chức năng không thực sự cần thiết trong nhiều ứng dụng thực tế.