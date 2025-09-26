---
title: Các chính sách 'Dọn Dẹp' Cache
date: 2025-08-10
image: /image-placeholder.png
categories:
  - system
tags:
  - cache
draft: false
---

Chúng ta đã biết cache rất hữu ích, nhưng nó có một giới hạn cố hữu: dung lượng nhỏ. Bộ nhớ tốc độ cao (như RAM) rất đắt đỏ, vì vậy cache không thể lưu trữ mọi thứ.

<!--more-->

---

## Các Chính Sách "Dọn Dẹp"

Chúng ta đã biết cache rất hữu ích, nhưng nó có một giới hạn cố hữu: dung lượng nhỏ. Bộ nhớ tốc độ cao (như RAM) rất đắt đỏ, vì vậy cache không thể lưu trữ mọi thứ.

Điều này dẫn đến một vấn đề không thể tránh khỏi: khi cache đã đầy và một mục dữ liệu mới cần được thêm vào, hệ thống phải quyết định loại bỏ một mục dữ liệu cũ để nhường chỗ. Quá trình này được gọi là **Eviction**.

Thuật toán được sử dụng để quyết định _mục nào_ sẽ bị loại bỏ được gọi là **Chính sách dọn dẹp (Eviction Policy)**. 

### Các chiến lược dọn dẹp phổ biến

-   **FIFO (First-In, First-Out - Vào trước, Ra trước):**
	
    -   **Nguyên tắc:** Nó loại bỏ mục dữ liệu cũ nhất, bất kể nó có được sử dụng thường xuyên hay không. Nó hoạt động giống như một hàng đợi (queue).
		
    -   **Ưu điểm:** Rất dễ cài đặt và có chi phí quản lý thấp.
		
    -   **Nhược điểm:** Thường không hiệu quả vì nó có thể loại bỏ một mục rất phổ biến chỉ vì nó được nạp vào cache từ lâu.
	
-   **LRU (Least Recently Used - Ít được sử dụng gần đây nhất):**
	
    -   **Nguyên tắc:** Loại bỏ mục dữ liệu mà đã không được truy cập trong khoảng thời gian dài nhất.
		
    -   **Ưu điểm:** Hiệu quả hơn FIFO rất nhiều trong hầu hết các trường hợp thực tế, vì nó giữ lại những dữ liệu đang được sử dụng tích cực.
		
    -   **Nhược điểm:** Phức tạp hơn trong việc triển khai vì nó đòi hỏi phải theo dõi thời gian truy cập của mỗi mục, gây tốn thêm một chút bộ nhớ và xử lý.
	
-   **LFU (Least Frequently Used - Ít được sử dụng thường xuyên nhất):**
	
    -   **Nguyên tắc:** Loại bỏ mục dữ liệu được truy cập với số lần ít nhất.
		
    -   **Ưu điểm:** Rất tốt trong việc xác định và giữ lại các mục dữ liệu "hot" (phổ biến) trong một thời gian dài, ngay cả khi chúng không được truy cập gần đây.
		
    -   **Nhược điểm:** Phức tạp để triển khai hiệu quả. (ví dụ: một mục từng rất hot nhưng giờ không còn ai dùng nữa vẫn có thể chiếm chỗ trong cache một thời gian dài). Nó cũng có thể loại bỏ một mục mới được thêm vào nhưng chưa có cơ hội tích lũy đủ số lần truy cập.

### Bảng so sánh các chính sách dọn dẹp

| Chính sách | Nguyên tắc cốt lõi                         | Ví dụ tương tự                                                       | Ưu điểm                                                                   | Nhược điểm                                                                 | Phù hợp nhất cho                                                                                                     |
| ---------- | ------------------------------------------ | -------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| **FIFO**   | Loại bỏ mục vào cache sớm nhất.            | Xếp hàng mua vé: người đến trước được phục vụ trước.                 | Đơn giản, chi phí thấp.                                                   | Không thông minh, có thể loại bỏ dữ liệu quan trọng.                       | Các hệ thống có mẫu truy cập tuần tự, không lặp lại.                                                                 |
| **LRU**    | Loại bỏ mục ít được dùng đến gần đây nhất. | Dọn dẹp bàn làm việc: trả lại cuốn sách bạn không đụng đến lâu nhất. | Hiệu quả cao trong hầu hết các trường hợp, thích ứng tốt với sự thay đổi. | Phức tạp hơn, cần theo dõi thời gian truy cập.                             | Các ứng dụng thông thường, nơi dữ liệu gần đây có khả năng được tái sử dụng cao (ví dụ: trang tin tức, mạng xã hội). |
| **LFU**    | Loại bỏ mục có số lần truy cập ít nhất.    | Thư viện cho mượn sách: loại bỏ những cuốn ít người mượn nhất.       | Giữ lại được các mục "hot" một cách ổn định.                              | Phức tạp, có thể giữ lại dữ liệu "hot" đã lỗi thời, không thích ứng nhanh. | Các hệ thống có một số dữ liệu cực kỳ phổ biến và ổn định (ví dụ: sản phẩm bán chạy, video viral).                   |

## Giữ Cho Dữ Liệu Đồng Nhất: Các Chính Sách Ghi

Khi một ứng dụng thực hiện thao tác ghi (write) hoặc cập nhật (update), một vấn đề nghiêm trọng nảy sinh. Bây giờ chúng ta có hai bản sao của cùng một dữ liệu: một trong cache và một trong cơ sở dữ liệu. Nếu chúng không được cập nhật đồng bộ, cache sẽ chứa dữ liệu cũ. Việc phục vụ stale data cho người dùng có thể dẫn đến các lỗi nghiêm trọng, thông tin sai lệch và trải nghiệm tồi tệ.

**Chính sách ghi (Write Policy)** là quy tắc xác định cách hệ thống xử lý các thao tác ghi để giải quyết vấn đề về tính nhất quán này.

### Các chính sách ghi cốt lõi

-   **Write-Through (Ghi Xuyên)**
	
    -   **Quy trình:** Khi ứng dụng ghi dữ liệu, nó sẽ ghi **đồng thời** vào cả cache và cơ sở dữ liệu. Thao tác chỉ được coi là hoàn tất khi cả hai nơi đều đã ghi xong.
		
    -   **Lưu đồ:** `Ứng dụng -> Ghi vào Cache -> Ghi vào Database -> Hoàn tất`
		
    -   **Ưu điểm:** Tính nhất quán dữ liệu rất cao. Cache và database luôn đồng bộ. Đơn giản để triển khai và đáng tin cậy.
		
    -   **Nhược điểm:** Độ trễ của thao tác ghi cao, vì ứng dụng phải chờ cả hai thao tác ghi hoàn tất.
		
    -   **Trường hợp sử dụng:** Các ứng dụng quan trọng nơi tính nhất quán dữ liệu là tối thượng, ví dụ như hệ thống ngân hàng, quản lý kho hàng.
	
-   **Write-Back (Ghi Sau / Write-Behind)**
    -   **Quy trình:** Khi ứng dụng ghi dữ liệu, nó chỉ ghi vào cache tốc độ cao trước. Thao tác được xác nhận hoàn tất ngay lập tức. Việc ghi vào cơ sở dữ liệu sẽ được trì hoãn và thực hiện sau đó, có thể là sau một khoảng thời gian nhất định hoặc khi mục cache đó sắp bị dọn dẹp. Hệ thống thường dùng một "bit bẩn" (dirty bit) để đánh dấu các mục trong cache đã bị thay đổi và cần được ghi lại vào database.
		
    -   **Lưu đồ:** `Ứng dụng -> Ghi vào Cache -> Hoàn tất. (Background: Cache -> Ghi vào Database)`
		
    -   **Ưu điểm:** Độ trễ ghi cực thấp và thông lượng cao. Giảm tải cho database bằng cách gộp nhiều lần ghi vào cùng một đối tượng thành một lần ghi duy nhất (write-coalescing).
		
    -   **Nhược điểm:** Có nguy cơ mất dữ liệu nếu cache bị lỗi trước khi dữ liệu kịp ghi vào database. Phức tạp hơn để triển khai.
		
    -   **Trường hợp sử dụng:** Các ứng dụng có lượng ghi lớn, nơi hiệu năng là ưu tiên hàng đầu và có thể chấp nhận một rủi ro nhỏ về mất mát dữ liệu, ví dụ như ghi log hành vi người dùng, cập nhật số lượt xem bài viết.
	
-   **Write-Around (Ghi Vòng)**
	
    -   **Quy trình:** Khi ứng dụng ghi dữ liệu, nó sẽ ghi **trực tiếp** vào cơ sở dữ liệu, hoàn toàn bỏ qua cache. Dữ liệu chỉ được nạp vào cache sau này, khi có một yêu cầu đọc bị cache miss.
		
    -   **Lưu đồ:** `Ứng dụng -> Ghi vào Database -> Hoàn tất`
		
    -   **Ưu điểm:** Tránh "làm ô nhiễm" cache bằng những dữ liệu có thể không bao giờ được đọc lại.
		
    -   **Nhược điểm:** Một yêu cầu đọc ngay sau khi ghi sẽ luôn luôn là cache miss, dẫn đến độ trễ đọc cao cho dữ liệu vừa được ghi.
		
    -   **Trường hợp sử dụng:** Các ứng dụng ghi dữ liệu nhưng hiếm khi đọc lại ngay sau đó, ví dụ như các hệ thống nhập dữ liệu hàng loạt (bulk data ingestion), lưu trữ log.
	
Các chính sách ghi không tồn tại một cách độc lập. Chúng liên kết chặt chẽ với cách hệ thống xử lý một **write miss** (khi ứng dụng muốn ghi vào một mục không có trong cache). Có hai lựa chọn:

1. **Write Allocate (Fetch on Write):** Khi có write miss, hệ thống sẽ tải khối dữ liệu đó từ database vào cache trước, rồi mới thực hiện thao tác ghi.
	
2. **No-Write Allocate:** Khi có write miss, hệ thống sẽ ghi thẳng vào database, không tải dữ liệu đó vào cache.