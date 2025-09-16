---
title: "Cache"
date: 2025-08-10
image: "/images/image-placeholder.png"
categories: ["system"]
tags: ["cache"]
draft: false
---

Overview of Cache

<!--more-->

Trong thế giới phát triển phần mềm, chúng ta luôn bị ám ảnh bởi một từ khóa: **hiệu năng**. Làm thế nào để ứng dụng chạy nhanh hơn? Làm sao để trang web tải trong chớp mắt? Làm sao để hệ thống chịu được hàng triệu lượt truy cập mà không sụp đổ? Giữa vô vàn câu trả lời, có một khái niệm nền tảng, một kỹ thuật được áp dụng ở mọi quy mô, từ con chip nhỏ trong CPU đến các hệ thống phân tán toàn cầu. Đó chính là **Cache**.

Nhiều người đã nghe về cache, có thể là "xóa cache trình duyệt" hay "cache của CPU". Nhưng cache thực sự là gì? Nó hoạt động ra sao và tại sao nó lại quan trọng đến vậy?

Bài viết này sẽ đưa bạn đi từ những khái niệm cơ bản nhất đến các chiến lược chuyên sâu trong thiết kế hệ thống. Hy vọng rằng sau khi đọc xong, bạn sẽ có một cái nhìn rõ ràng và sâu sắc về "vũ khí bí mật" mang tên cache.

Hãy cùng bắt đầu!

## Cache Là Gì?

Để hiểu về cache, hãy bắt đầu bằng một câu chuyện đơn giản.

### Câu chuyện về Thư viện và Chiếc bàn làm việc

Hãy tưởng tượng bạn là một nhà nghiên cứu cần rất nhiều sách cho công việc của mình. Toàn bộ sách được lưu trữ trong một thư viện khổng lồ ở phía bên kia thành phố. Mỗi khi cần một thông tin, bạn phải mất công di chuyển đến thư viện, tìm đúng cuốn sách, đọc, rồi lại đi về. Quá trình này rất chậm chạp và tốn thời gian.

Bây giờ, bạn nghĩ ra một giải pháp thông minh hơn. Thay vì mỗi lần cần lại chạy đi, bạn sẽ mang những cuốn sách hay dùng nhất về đặt ngay trên chiếc bàn làm việc của mình. Chiếc bàn này tuy nhỏ, không thể chứa cả thư viện, nhưng nó ở ngay trước mặt bạn. Lần tới, khi cần thông tin từ những cuốn sách đó, bạn chỉ cần với tay là có ngay, nhanh hơn gấp trăm lần so với việc đi đến thư viện.

Trong thế giới máy tính, câu chuyện này diễn ra liên tục.

-   **Thư viện khổng lồ** chính là nơi lưu trữ dữ liệu chính, ví dụ như ổ cứng (HDD/SSD) hoặc Database. Nơi này có dung lượng lớn nhưng tốc độ truy cập khá chậm.
-   **Chiếc bàn làm việc** của bạn chính là **Cache**.

**Cache** là một lớp lưu trữ dữ liệu tốc độ cao, có kích thước nhỏ, dùng để chứa một tập hợp con của dữ liệu gốc. Mục đích của nó là để các yêu cầu truy xuất dữ liệu trong tương lai được phục vụ nhanh hơn rất nhiều so với việc phải lấy dữ liệu từ database. Về cơ bản, cache cho phép chúng ta tái sử dụng một cách hiệu quả những dữ liệu đã được truy xuất hoặc tính toán trước đó.

### Tại sao Cache lại quan trọng đến vậy?

Sử dụng cache mang lại 3 lợi ích cốt lõi, biến nó trở thành một kỹ thuật không thể thiếu trong hầu hết mọi hệ thống máy tính hiện đại.

1. **Tăng tốc độ một cách chóng mặt (Performance):** Đây là mục đích chính. Cache thường được triển khai trên các phần cứng truy cập nhanh như RAM (Bộ nhớ truy cập ngẫu nhiên). Tốc độ truy cập RAM nhanh hơn hàng trăm, thậm chí hàng nghìn lần so với ổ đĩa. Việc phục vụ dữ liệu từ cache giúp giảm độ trễ (latency) và tăng số lượng thao tác I/O mỗi giây (IOPS) một cách đáng kể, làm cho ứng dụng trở nên mượt mà và phản hồi nhanh hơn.
2. **Giảm tải cho hệ thống Backend:** Cache hoạt động như một tấm khiên, che chắn cho cơ sở dữ liệu hoặc các dịch vụ API. Thay vì mọi yêu cầu đều phải truy cập vào cơ sở dữ liệu, phần lớn các yêu cầu đọc sẽ được cache xử lý. Điều này giúp cơ sở dữ liệu không bị quá tải, đặc biệt là trong những thời điểm có lưu lượng truy cập tăng đột biến, và giữ cho toàn bộ hệ thống ổn định.
3. **Tiết kiệm chi phí (Cost Efficiency):** Ở quy mô lớn, việc phục vụ dữ liệu từ cache trong bộ nhớ (in-memory) có thể rẻ hơn đáng kể so với việc phải nâng cấp liên tục các máy chủ cơ sở dữ liệu hoặc trả chi phí cho lưu lượng mạng cao khi truy xuất dữ liệu từ các dịch vụ đám mây.

### Cache Hit và Cache Miss

Hoạt động của cache xoay quanh hai kịch bản chính: **Cache Hit** và **Cache Miss**. Khi một client (có thể là CPU, trình duyệt web, hoặc ứng dụng của bạn) cần dữ liệu, nó sẽ luôn hỏi cache trước tiên.

-   **Cache Hit (Tìm thấy trong Cache):** Đây là kịch bản lý tưởng. Dữ liệu được yêu cầu có tồn tại trong cache. Cache sẽ ngay lập tức trả về dữ liệu này cho client. Quá trình này cực kỳ nhanh chóng.
-   **Cache Miss (Không tìm thấy trong Cache):** Đây là kịch bản không mong muốn. Dữ liệu được yêu cầu không có trong cache. Khi đó, hệ thống buộc phải truy cập đến database để lấy dữ liệu. Sau khi lấy được, dữ liệu này sẽ được sao chép một bản vào cache để những lần yêu cầu sau sẽ trở thành cache hit, rồi mới được trả về cho client.

Một điểm cực kỳ quan trọng cần nhận thức ở đây là sự tồn tại của "Cache Miss" cho thấy một sự thật nền tảng: cache không phải là một phép màu tăng tốc miễn phí. Nó đi kèm với sự đánh đổi và chi phí. Một cache miss vốn dĩ còn **chậm hơn** một hệ thống không có cache. Bởi vì trong một hệ thống không cache, thời gian truy xuất chỉ đơn giản là thời gian lấy dữ liệu từ nguồn chính. Còn trong một cache miss, tổng thời gian là `Thời gian kiểm tra cache (và thất bại)` + `Thời gian lấy dữ liệu từ database`.

Do đó, mục tiêu của mọi chiến lược caching không chỉ đơn giản là "có cache", mà là thiết kế một hệ thống nơi tổng thời gian tiết kiệm được từ vô số các cache hit phải lớn hơn rất nhiều so với tổng thời gian bị mất đi do các cache miss không thể tránh khỏi. Điều này biến caching từ một công cụ đơn thuần thành một bài toán tối ưu hóa chiến lược.

### Tỷ lệ Cache Hit (Cache Hit Ratio)

Để biết cache của chúng ta có hoạt động hiệu quả hay không, chúng ta cần một thước đo. Thước đo quan trọng nhất chính là **Tỷ lệ Cache Hit (Cache Hit Ratio)**.

Công thức tính rất đơn giản

Tỷ lệ Cache Hit= Cache Hit​ / (Cache Hit + Cache Miss)

Tỷ lệ này, thường được biểu diễn dưới dạng phần trăm, cho biết có bao nhiêu phần trăm yêu cầu được phục vụ nhanh chóng từ cache. Một tỷ lệ cache hit cao (thường từ 80-95% trở lên đối với nội dung tĩnh) cho thấy cache đang hoạt động rất hiệu quả. Ngược lại, một tỷ lệ thấp cho thấy cache đang không được sử dụng tốt, có thể do cấu hình sai, chính sách dọn dẹp không phù hợp, hoặc kích thước cache quá nhỏ.

### Cache Phần cứng (CPU Cache)

Loại cache nhanh nhất, cơ bản nhất nằm ở cấp độ phần cứng, được tích hợp trực tiếp CPU. Mục đích của nó là để bắc một cây cầu qua "vực thẳm" tốc độ giữa một CPU siêu nhanh và RAM chậm hơn nhiều.

Để hiểu điều này, chúng ta cần biết về **Hệ thống phân cấp bộ nhớ (Memory Hierarchy)**. Đây là một mô hình tổ chức bộ nhớ trong máy tính thành nhiều cấp, giống như một kim tự tháp. Càng ở đỉnh kim tự tháp, bộ nhớ càng nhanh, càng đắt và dung lượng càng nhỏ. Càng xuống đáy, bộ nhớ càng chậm, càng rẻ và dung lượng càng lớn.

Code snippet

```
(1) Register
(2) L1 Cache
(3) L2 Cache
(4) L3 Cache
(5) RAM <- Redis
(6) SSD
(7) HDD
```

CPU cache được chia thành nhiều cấp (Level), thường là L1, L2, và L3:

-   **L1 Cache (Level 1):** Đây là bộ nhớ cache nhỏ nhất và nhanh nhất, được tích hợp ngay trong từng nhân (core) của CPU
-   **L2 Cache (Level 2):** Lớn hơn L1 nhưng chậm hơn một chút. L2 cache có thể nằm riêng cho từng nhân hoặc chung cho một vài nhân, tùy vào kiến trúc CPU.
-   **L3 Cache (Level 3):** Lớn nhất và chậm nhất trong các cấp CPU cache. L3 cache thường được dùng chung cho tất cả các nhân trên một con chip. Nó giúp tăng tốc độ giao tiếp giữa các nhân và giảm thiểu việc phải truy cập ra RAM.

### Cache Phần mềm

Ngoài phần cứng, caching là một kỹ thuật được quản lý bởi phần mềm ở nhiều lớp khác nhau trong một ứng dụng. Đây là những loại cache mà các lập trình viên chúng ta thường xuyên tương tác và thiết kế.

-   **Cache Trình duyệt (Browser Cache):** Khi bạn truy cập một trang web, trình duyệt của bạn sẽ tự động lưu các tài nguyên tĩnh như hình ảnh, file CSS, JavaScript vào một thư mục trên ổ cứng. Lần sau khi bạn quay lại trang đó, trình duyệt sẽ tải các tài nguyên này từ ổ cứng thay vì phải tải lại từ server, giúp trang web hiển thị gần như ngay lập tức. Đây là một dạng cache phía client (client-side), riêng tư cho mỗi người dùng.
-   **Cache Mạng Phân phối Nội dung (CDN - Content Delivery Network):** Đây là một mạng lưới các máy chủ proxy được đặt ở nhiều vị trí địa lý trên toàn cầu. Các máy chủ này lưu trữ (cache) bản sao của nội dung trang web (như video, hình ảnh, file tĩnh). Ví dụ điển hình là Netflix hay YouTube. Khi bạn ở Việt Nam và xem một video, rất có thể bạn đang nhận dữ liệu từ một máy chủ CDN đặt tại Singapore hoặc Hồng Kông, chứ không phải từ máy chủ gốc ở Mỹ. Điều này giúp giảm đáng kể độ trễ và tăng tốc độ tải.
-   **Cache Cơ sở dữ liệu (Database Cache):** Hầu hết các hệ quản trị cơ sở dữ liệu như MySQL, PostgreSQL đều có một bộ đệm cache nội bộ. Nó lưu lại kết quả của các câu truy vấn (query) được thực thi thường xuyên. Khi nhận được một câu truy vấn giống hệt, thay vì phải quét lại toàn bộ bảng dữ liệu, database sẽ trả về kết quả từ cache của nó.
-   **Cache Ứng dụng (Application Cache / In-Memory Cache):** Đây là lớp cache mà các lập trình viên chủ động thêm vào kiến trúc ứng dụng của mình, thường sử dụng các công cụ chuyên dụng như **Redis** hoặc **Memcached**. Lớp cache này có thể lưu trữ bất cứ thứ gì: kết quả của các phép tính toán phức tạp, phản hồi từ các API, các đối tượng dữ liệu đã được định dạng sẵn... Việc này giúp ứng dụng không phải tính toán lại hoặc truy vấn lại những thông tin tốn kém trên mỗi yêu cầu.

Hãy xem xét cấu trúc: `Client -> Cache -> Nguồn`.

-   Với CPU: Client là nhân xử lý, Cache là L1, Nguồn là RAM.
-   Với Web: Client là công cụ render, Cache là ổ cứng cục bộ, Nguồn là web server.
-   Với CDN: Client là trình duyệt, Cache là máy chủ biên (edge server), Nguồn là máy chủ gốc (origin server).
-   Với App: Client là logic nghiệp vụ, Cache là Redis/Memcached, Nguồn là Database.

## Khi Cache Bị Đầy: Các Chính Sách "Dọn Dẹp"

Chúng ta đã biết cache rất hữu ích, nhưng nó có một giới hạn cố hữu: dung lượng nhỏ. Bộ nhớ tốc độ cao (như RAM) rất đắt đỏ, vì vậy cache không thể lưu trữ mọi thứ.

Điều này dẫn đến một vấn đề không thể tránh khỏi: khi cache đã đầy và một mục dữ liệu mới cần được thêm vào, hệ thống phải quyết định loại bỏ một mục dữ liệu cũ để nhường chỗ. Quá trình này được gọi là **Eviction** (dọn dẹp/loại bỏ).

Thuật toán được sử dụng để quyết định _mục nào_ sẽ bị loại bỏ được gọi là **Chính sách dọn dẹp (Eviction Policy)**. Quay lại với câu chuyện thư viện, khi bàn làm việc của bạn đã chật kín sách, bạn sẽ phải chọn một cuốn để trả lại thư viện trước khi mang cuốn mới về. Bạn chọn cuốn nào? Sự lựa chọn của bạn chính là một chính sách dọn dẹp.

Dưới đây là các chiến lược dọn dẹp phổ biến nhất.

### Các chiến lược dọn dẹp phổ biến

-   **FIFO (First-In, First-Out - Vào trước, Ra trước):**
    -   **Nguyên tắc:** Đây là chính sách đơn giản nhất. Nó loại bỏ mục dữ liệu cũ nhất, tức là mục đã nằm trong cache lâu nhất, bất kể nó có được sử dụng thường xuyên hay không. Nó hoạt động giống như một hàng đợi (queue).
    -   **Ưu điểm:** Rất dễ cài đặt và có chi phí quản lý thấp.
    -   **Nhược điểm:** Thường không hiệu quả vì nó có thể loại bỏ một mục rất phổ biến chỉ vì nó được nạp vào cache từ lâu.
-   **LRU (Least Recently Used - Ít được sử dụng gần đây nhất):**
    -   **Nguyên tắc:** Chính sách này loại bỏ mục dữ liệu mà đã không được truy cập trong khoảng thời gian dài nhất. Nó hoạt động dựa trên nguyên tắc **tính cục bộ về thời gian (temporal locality)**
    -   **Ưu điểm:** Hiệu quả hơn FIFO rất nhiều trong hầu hết các trường hợp thực tế, vì nó giữ lại những dữ liệu đang được sử dụng tích cực.
    -   **Nhược điểm:** Phức tạp hơn trong việc triển khai vì nó đòi hỏi phải theo dõi thời gian truy cập của mỗi mục, gây tốn thêm một chút bộ nhớ và xử lý.
-   **LFU (Least Frequently Used - Ít được sử dụng thường xuyên nhất):**
    -   **Nguyên tắc:** Chính sách này loại bỏ mục dữ liệu được truy cập với số lần ít nhất. Nó dựa trên nguyên tắc **tính cục bộ về tần suất (frequency locality)** – ý tưởng rằng có một số dữ liệu vốn dĩ đã phổ biến hơn những dữ liệu khác.
    -   **Ưu điểm:** Rất tốt trong việc xác định và giữ lại các mục dữ liệu "hot" (phổ biến) trong một thời gian dài, ngay cả khi chúng không được truy cập gần đây.
    -   **Nhược điểm:** Phức tạp để triển khai hiệu quả. Nó có thể không thích ứng nhanh với các mẫu truy cập thay đổi (ví dụ: một mục từng rất hot nhưng giờ không còn ai dùng nữa vẫn có thể chiếm chỗ trong cache một thời gian dài). Nó cũng có thể loại bỏ một mục mới được thêm vào nhưng chưa có cơ hội tích lũy đủ số lần truy cập.

### Bảng so sánh các chính sách dọn dẹp

Để giúp bạn dễ dàng lựa chọn, đây là bảng so sánh các chính sách phổ biến:

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

Sự kết hợp giữa chính sách ghi và chính sách write miss tạo ra các chiến lược hoàn chỉnh. Ví dụ, một hệ thống **Write-Back** thường đi kèm với **Write Allocate**. Triết lý của Write-Back là hấp thụ các thao tác ghi để tăng hiệu năng, với giả định rằng dữ liệu đó sẽ sớm được truy cập lại. Vì vậy, khi có write miss, việc tải dữ liệu vào cache trước là hợp lý để các thao tác sau đó có thể hưởng lợi từ cache. Ngược lại, một hệ thống **Write-Through** thường sử dụng **No-Write Allocate** (chính là chiến lược Write-Around). Triết lý của Write-Through là an toàn dữ liệu. Nếu có write miss, việc tải dữ liệu vào cache chỉ để ghi nó ngay lập tức ra database là không hiệu quả. Sẽ đơn giản hơn nếu ghi thẳng vào database và tránh làm ô nhiễm cache.

Hiểu được mối liên kết nhân quả này giúp các nhà phát triển đưa ra quyết định kiến trúc mạch lạc và tối ưu hơn, thay vì chọn hai chính sách một cách ngẫu nhiên.

## Xây Dựng Hệ Thống Với Cache: Các Mẫu Thiết Kế

### Mẫu 1: Cache-Aside (Lazy Loading)

Đây là mẫu thiết kế phổ biến và trực quan nhất. Trong mẫu này, logic của ứng dụng chịu trách nhiệm hoàn toàn cho việc quản lý cache.

-   **Quy trình:**

    -   Ứng dụng cần đọc dữ liệu, nó sẽ kiểm tra cache trước.
    -   Nếu có (cache hit), dữ liệu được trả về.
    -   Nếu không có (cache miss), **ứng dụng** sẽ đọc dữ liệu từ database.
    -   Sau đó, **ứng dụng** sẽ ghi dữ liệu vừa đọc được vào cache.
    -   Khi ghi dữ liệu, ứng dụng thường sẽ cập nhật database trước, sau đó **vô hiệu hóa (invalidate)** mục tương ứng trong cache.

    ![Image Description](/images/Pasted image 20250810134139.png/)

-   **Ưu điểm:** Ứng dụng có toàn quyền kiểm soát. Cache chỉ lưu những dữ liệu thực sự được yêu cầu, giúp tiết kiệm không gian. Hệ thống có khả năng chống chịu lỗi cache tốt (nếu cache sập, ứng dụng có thể đọc trực tiếp từ database).
-   **Nhược điểm:** Yêu cầu đầu tiên cho bất kỳ dữ liệu nào cũng sẽ là cache miss. Code của ứng dụng phức tạp hơn vì phải chứa logic quản lý cache.

### Mẫu 2: Read-Through

Mẫu này trừu tượng hóa database khỏi ứng dụng. Ứng dụng chỉ cần "nói chuyện" với cache.

-   **Quy trình:**
    -   Ứng dụng yêu cầu dữ liệu từ cache.
    -   Nếu cache có, nó sẽ trả về.
    -   Nếu cache không có, **chính cache** sẽ chịu trách nhiệm đi lấy dữ liệu từ database, lưu lại rồi trả về cho ứng dụng.
-   **Ưu điểm:** Đơn giản hóa code ứng dụng vì logic caching được đóng gói trong cache provider.
-   **Nhược điểm:** Kém linh hoạt hơn. Cache provider phải hỗ trợ mẫu này.

### Mẫu 3 & 4: Write-Through và Write-Behind (Write-Back)

Đây là các mẫu tập trung vào việc ghi, thường đi đôi với Read-Through.

-   **Write-Through:** Ứng dụng ghi dữ liệu vào cache, và **cache** sẽ chịu trách nhiệm ghi đồng bộ dữ liệu đó vào database. Điều này đảm bảo tính nhất quán cao.
-   **Write-Behind:** Ứng dụng ghi dữ liệu vào cache, và **cache** sẽ ghi dữ liệu đó vào database một cách bất đồng bộ (trong nền). Điều này cho hiệu năng ghi rất cao.

Sự lựa chọn giữa Cache-Aside và các mẫu Read/Write-Through không chỉ là chi tiết kỹ thuật, mà là một quyết định kiến trúc nền tảng về **sự phân tách trách nhiệm (separation of concerns)**.

-   **Cache-Aside** đặt trách nhiệm điều phối dữ liệu lên vai ứng dụng. Ứng dụng "biết" cả về cache và database.
-   **Read/Write-Through** coi cache như một lớp mặt tiền (facade) cho database. Ứng dụng chỉ cần biết "lấy dữ liệu" hoặc "ghi dữ liệu" tại một điểm duy nhất là cache.

Mô hình Read-Through thúc đẩy sự phân tách trách nhiệm sạch sẽ hơn, dẫn đến code ứng dụng đơn giản và dễ bảo trì hơn. Tuy nhiên, nó lại ràng buộc chặt chẽ cache với database, khiến việc thay đổi database hoặc sử dụng cache cho các nguồn dữ liệu khác trở nên khó khăn. Ngược lại, Cache-Aside linh hoạt hơn – cache có thể chứa dữ liệu từ nhiều nguồn (database, API, file,...) – nhưng phải trả giá bằng sự phức tạp tăng lên trong code ứng dụng. Đây là một sự đánh đổi kinh điển giữa đơn giản/đóng gói và linh hoạt/kiểm soát.

## Thách Thức Lớn Nhất: Dữ Liệu Cũ và Vô Hiệu Hóa Cache

Vấn đề cốt lõi vẫn là **stale data**. Khi dữ liệu trong nguồn chính bị thay đổi bởi một tiến trình khác mà cache không hề hay biết, cache sẽ trở nên lỗi thời. Phục vụ dữ liệu lỗi thời này có thể gây ra những hậu quả tai hại.

**Cache Invalidation** là quá trình đánh dấu hoặc loại bỏ dữ liệu trong cache để nó không còn hợp lệ nữa.

### Các chiến lược vô hiệu hóa cache

-   **Time-To-Live (TTL) Expiration (Hết hạn theo thời gian):**
    -   **Quy trình:** Đây là chiến lược đơn giản nhất. Khi dữ liệu được lưu vào cache, nó được gán một "tuổi thọ", ví dụ 5 phút. Sau 5 phút, dữ liệu này tự động bị coi là không hợp lệ và sẽ bị xóa hoặc bỏ qua trong lần truy cập tiếp theo, buộc hệ thống phải lấy lại dữ liệu mới từ database.
    -   **Ưu điểm:** Dễ triển khai, đảm bảo dữ liệu cuối cùng sẽ nhất quán.
    -   **Nhược điểm:** Dữ liệu có thể bị lỗi thời trong suốt khoảng thời gian TTL. Việc chọn TTL phù hợp là một nghệ thuật cân bằng khó khăn: TTL quá ngắn sẽ làm giảm tỷ lệ cache hit, TTL quá dài sẽ tăng nguy cơ stale data.
-   **Event-Driven Invalidation (Active Deletion - Xóa chủ động):**
    -   **Quy trình:** Một cách tiếp cận chủ động hơn. Khi dữ liệu trong database được cập nhật (ví dụ, người dùng đổi ảnh đại diện), ứng dụng sẽ gửi một lệnh `DELETE` hoặc `INVALIDATE` rõ ràng đến cache để xóa mục tương ứng.
    -   **Ưu điểm:** Đảm bảo dữ liệu được vô hiệu hóa gần như ngay lập tức, mang lại tính nhất quán cao hơn nhiều so với TTL.
    -   **Nhược điểm:** Phức tạp hơn để triển khai. Nó đòi hỏi sự liên kết chặt chẽ giữa code ghi vào database và cache. Trong một hệ thống phân tán, nó rất dễ gặp phải các vấn đề về **race condition** (tranh chấp) hoặc lỗi mạng.

Vấn đề "khó" của cache invalidation không chỉ nằm ở việc _khi nào_ cần vô hiệu hóa, mà là làm thế nào để đảm bảo việc vô hiệu hóa đó là _chính xác_ và _nguyên tử_ trong một môi trường có nhiều tiến trình chạy đồng thời. Đây là lúc chúng ta đối mặt với một vấn đề kinh điển về race condition.

Hãy xem xét kịch bản sau trong mẫu Cache-Aside:

1. Tiến trình A đọc dữ liệu X. Bị cache miss.
2. Tiến trình A đi đến database để đọc dữ liệu X (phiên bản cũ).
3. Trong lúc đó, tiến trình B cập nhật dữ liệu X trong database và ngay lập tức gửi lệnh vô hiệu hóa cache cho X.
4. Tiến trình A, sau khi đọc xong dữ liệu X (phiên bản cũ) từ database, giờ đây lại ghi nó vào cache.
5. **Kết quả:** Cache bây giờ chứa dữ liệu X đã lỗi thời, và lệnh vô hiệu hóa của tiến trình B trở nên vô nghĩa. Dữ liệu lỗi thời này sẽ tồn tại trong cache cho đến khi TTL hết hạn.
   ![Image Description](/images/Pasted image 20250810134758.png/)

Đây không phải là lỗi của một công cụ cụ thể, mà là một lỗ hổng cơ bản trong việc định thời của các hoạt động phân tán. Các giải pháp cho vấn đề này, như sử dụng **phiên bản (versioning)** cho dữ liệu hoặc **cơ chế cho thuê (lease)**, không còn là các kỹ thuật vô hiệu hóa đơn giản nữa. Chúng là các cơ chế kiểm soát tương tranh (concurrency control) phức tạp. Ví dụ, với cơ chế lease mà Facebook sử dụng, chỉ tiến trình nào nhận được "hợp đồng thuê" khi bị cache miss mới có quyền ghi lại vào cache. Nếu một lệnh vô hiệu hóa xảy ra trong thời gian đó, "hợp đồng thuê" sẽ bị thu hồi, và thao tác ghi dữ liệu cũ của tiến trình A sẽ bị từ chối.

## Kết luận: Cache - Sự Đánh Đổi Thông Minh

Nếu có một điều cần đọng lại, đó là: **Cache không phải là một viên đạn bạc, mà là một kỹ thuật mạnh mẽ đòi hỏi sự đánh đổi thông minh.**

Mỗi quyết định bạn đưa ra – chọn loại cache nào, chính sách dọn dẹp ra sao, chính sách ghi nào, mẫu thiết kế nào – đều là một sự cân bằng giữa các yếu tố:

-   **Hiệu năng** và **Chi phí**
-   **Độ phức tạp** và **Tính đơn giản**
-   **Tính nhất quán dữ liệu** và **Độ trễ**
-   **Mô hình tối ưu nhất mà tôi biết**
    ![Image Description](/images/Pasted image 20250810135418.png/)

Không có câu trả lời nào là đúng cho mọi trường hợp. Một hệ thống yêu cầu tính nhất quán tuyệt đối sẽ phải hy sinh một phần hiệu năng ghi (sử dụng Write-Through). Một hệ thống cần hiệu năng ghi tối đa có thể phải chấp nhận rủi ro về dữ liệu (sử dụng Write-Back).

Hiểu rõ các khái niệm và chiến lược này không phải để tìm ra một "công thức hoàn hảo", mà là để trang bị cho bạn một bộ công cụ mạnh mẽ. Với bộ công cụ này, bạn có thể phân tích yêu cầu của ứng dụng, dự đoán các mẫu truy cập, và đưa ra những quyết định kiến trúc sáng suốt, phù hợp nhất với bài toán cụ thể của mình.

Chúc bạn thành công trên con đường xây dựng những hệ thống nhanh hơn, mạnh hơn và hiệu quả hơn!

---

_Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!_
