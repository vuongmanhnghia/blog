---
title: Giới thiệu về Cache
date: 2025-08-10
image: /images/image-placeholder.png
categories:
  - system
tags:
  - cache
draft: false
---

Nhiều người đã nghe về cache, có thể là "xóa cache trình duyệt" hay "cache của CPU". Nhưng cache thực sự là gì? Nó hoạt động ra sao và tại sao nó lại quan trọng đến vậy?

<!--more-->

---
## Cache Là Gì?

### Câu chuyện về Thư viện và Chiếc bàn làm việc

Hãy tưởng tượng bạn là một nhà nghiên cứu cần rất nhiều sách cho công việc của mình. Toàn bộ sách được lưu trữ trong một thư viện khổng lồ ở phía bên kia thành phố. Mỗi khi cần một thông tin, bạn phải mất công di chuyển đến thư viện, tìm đúng cuốn sách, đọc, rồi lại đi về. Quá trình này rất chậm chạp và tốn thời gian.

Bây giờ, bạn nghĩ ra một giải pháp thông minh hơn. Thay vì mỗi lần cần lại chạy đi, bạn sẽ mang những cuốn sách hay dùng nhất về đặt ngay trên chiếc bàn làm việc của mình. Chiếc bàn này tuy nhỏ, không thể chứa cả thư viện, nhưng nó ở ngay trước mặt bạn. Lần tới, khi cần thông tin từ những cuốn sách đó, bạn chỉ cần với tay là có ngay, nhanh hơn gấp trăm lần so với việc đi đến thư viện.

-   **Thư viện khổng lồ** chính là nơi lưu trữ dữ liệu chính, ví dụ như ổ cứng (HDD/SSD) hoặc Database. Nơi này có dung lượng lớn nhưng tốc độ truy cập khá chậm.
	
-   **Chiếc bàn làm việc** của bạn chính là **Cache**.

**Cache** là một lớp lưu trữ dữ liệu tốc độ cao, có kích thước nhỏ, dùng để chứa một tập hợp con của dữ liệu gốc. Mục đích của nó là để các yêu cầu truy xuất dữ liệu trong tương lai được phục vụ nhanh hơn rất nhiều so với việc phải lấy dữ liệu từ database. Về cơ bản, cache cho phép chúng ta tái sử dụng một cách hiệu quả những dữ liệu đã được truy xuất hoặc tính toán trước đó.

### Tại sao Cache lại quan trọng ?

1. **Tăng tốc độ một cách chóng mặt (Performance):** Đây là mục đích chính. Cache thường được triển khai trên các phần cứng truy cập nhanh như RAM (Bộ nhớ truy cập ngẫu nhiên). Tốc độ truy cập RAM nhanh hơn hàng trăm, thậm chí hàng nghìn lần so với ổ đĩa. 
	
2. **Giảm tải cho hệ thống Backend:** Thay vì mọi yêu cầu đều phải truy cập vào cơ sở dữ liệu, phần lớn các yêu cầu đọc sẽ được cache xử lý. Điều này giúp cơ sở dữ liệu không bị quá tải, đặc biệt là trong những thời điểm có lưu lượng truy cập tăng đột biến, và giữ cho toàn bộ hệ thống ổn định.
	
3. **Tiết kiệm chi phí (Cost Efficiency):** Ở quy mô lớn, việc phục vụ dữ liệu từ cache trong bộ nhớ (in-memory) có thể rẻ hơn đáng kể so với việc phải nâng cấp liên tục các máy chủ cơ sở dữ liệu hoặc trả chi phí cho lưu lượng mạng cao khi truy xuất dữ liệu từ các dịch vụ đám mây.

## Cache Hit và Cache Miss

Hoạt động của cache xoay quanh hai case chính: **Cache Hit** và **Cache Miss**. Khi một client (có thể là CPU, trình duyệt web, hoặc ứng dụng của bạn) cần dữ liệu, nó sẽ luôn hỏi cache trước tiên.

-   **Cache Hit (Tìm thấy trong Cache):** Đây là case lý tưởng. Cache sẽ ngay lập tức trả về dữ liệu này cho client. Quá trình này cực kỳ nhanh chóng.
	
-   **Cache Miss (Không tìm thấy trong Cache):** Đây là case không mong muốn. Khi đó, hệ thống buộc phải truy cập đến database để lấy dữ liệu. Sau khi lấy được, dữ liệu này sẽ được sao chép một bản vào cache để những lần yêu cầu sau sẽ trở thành cache hit, rồi mới được trả về cho client.

> Cache không phải là một phép màu tăng tốc miễn phí. Nó đi kèm với sự đánh đổi và chi phí. Một cache miss vốn dĩ còn **chậm hơn** một hệ thống không có cache. Bởi vì trong một hệ thống không cache, thời gian truy xuất chỉ đơn giản là thời gian lấy dữ liệu từ nguồn chính. Còn trong một cache miss, tổng thời gian là `Thời gian kiểm tra cache (và thất bại)` + `Thời gian lấy dữ liệu từ database`.

Do đó, mục tiêu của mọi chiến lược caching không chỉ đơn giản là "có cache", mà là thiết kế một hệ thống nơi tổng thời gian tiết kiệm được từ vô số các cache hit phải lớn hơn rất nhiều so với tổng thời gian bị mất đi do các cache miss không thể tránh khỏi.

### Tỷ lệ Cache Hit (Cache Hit Ratio)

Công thức tính rất đơn giản

```
Tỷ lệ Cache Hit= Cache Hit​ / (Cache Hit + Cache Miss)
```

Một tỷ lệ cache hit cao (thường từ 80-95% trở lên đối với nội dung tĩnh) cho thấy cache đang hoạt động rất hiệu quả. Ngược lại, một tỷ lệ thấp cho thấy cache đang không được sử dụng tốt, có thể do cấu hình sai, chính sách dọn dẹp không phù hợp, hoặc kích thước cache quá nhỏ.

### Cache Phần cứng (CPU Cache)

**Hệ thống phân cấp bộ nhớ (Memory Hierarchy)**. Đây là một mô hình tổ chức bộ nhớ trong máy tính thành nhiều cấp, giống như một kim tự tháp. Càng ở đỉnh kim tự tháp, bộ nhớ càng nhanh, càng đắt và dung lượng càng nhỏ. Càng xuống đáy, bộ nhớ càng chậm, càng rẻ và dung lượng càng lớn.

```
(1) Register
(2) L1 Cache
(3) L2 Cache
(4) L3 Cache
(5) RAM <- Redis
(6) SSD
(7) HDD
```

CPU cache được chia thành nhiều Level, thường là L1, L2, và L3:

-   **L1 Cache (Level 1):** Đây là bộ nhớ cache nhỏ nhất và nhanh nhất, được tích hợp ngay trong từng nhân (core) của CPU
	
-   **L2 Cache (Level 2):** Lớn hơn L1 nhưng chậm hơn một chút. L2 cache có thể nằm riêng cho từng nhân hoặc chung cho một vài nhân, tùy vào kiến trúc CPU.
	
-   **L3 Cache (Level 3):** Lớn nhất và chậm nhất trong các cấp CPU cache. L3 cache thường được dùng chung cho tất cả các nhân trên một con chip. Nó giúp tăng tốc độ giao tiếp giữa các nhân và giảm thiểu việc phải truy cập ra RAM.

### Cache Phần mềm

-   **Cache Trình duyệt (Browser Cache):** Khi bạn truy cập một trang web, trình duyệt của bạn sẽ tự động lưu các tài nguyên tĩnh như hình ảnh, file CSS, JavaScript vào một thư mục trên ổ cứng. Lần sau khi bạn quay lại trang đó, trình duyệt sẽ tải các tài nguyên này từ ổ cứng thay vì phải tải lại từ server, giúp trang web hiển thị gần như ngay lập tức. Đây là một dạng cache phía client (client-side), riêng tư cho mỗi người dùng.
	
-   **Cache Mạng Phân phối Nội dung (CDN - Content Delivery Network):** Đây là một mạng lưới các máy chủ proxy được đặt ở nhiều vị trí địa lý trên toàn cầu. Các máy chủ này lưu trữ (cache) bản sao của nội dung trang web (như video, hình ảnh, file tĩnh). Ví dụ điển hình là Netflix hay YouTube. Khi bạn ở Việt Nam và xem một video, rất có thể bạn đang nhận dữ liệu từ một máy chủ CDN đặt tại Singapore hoặc Hồng Kông, chứ không phải từ máy chủ gốc ở Mỹ. Điều này giúp giảm đáng kể độ trễ và tăng tốc độ tải.
	
-   **Cache Cơ sở dữ liệu (Database Cache):** Hầu hết các hệ quản trị cơ sở dữ liệu như MySQL, PostgreSQL đều có một bộ đệm cache nội bộ. Nó lưu lại kết quả của các câu truy vấn (query) được thực thi thường xuyên. Khi nhận được một câu truy vấn giống hệt, thay vì phải quét lại toàn bộ bảng dữ liệu, database sẽ trả về kết quả từ cache của nó.
	
-   **Cache Ứng dụng (Application Cache / In-Memory Cache):** Thường sử dụng các công cụ chuyên dụng như **Redis** hoặc **Memcached**. Lớp cache này có thể lưu trữ bất cứ thứ gì. Việc này giúp ứng dụng không phải tính toán lại hoặc truy vấn lại những thông tin tốn kém trên mỗi yêu cầu.
---
