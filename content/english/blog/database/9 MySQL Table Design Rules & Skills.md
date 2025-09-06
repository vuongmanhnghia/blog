---
title: 9 MySQL Table Design Rules & Skills
date: 2025-08-12
draft: false
tags:
  - database
  - sql
---
Principles and skills to extend MySQL table design
<!--more-->
Trong thế giới phát triển ứng dụng Backend, việc thiết kế cơ sở dữ liệu (database) không chỉ là một công việc kỹ thuật mà còn là một nghệ thuật đòi hỏi sự tỉ mỉ, hiểu biết sâu sắc về dữ liệu và tầm nhìn dài hạn về tính mở rộng của hệ thống. Đặc biệt, đối với các ứng dụng có nhiều kịch bản phức tạp như chat nhóm (chat group) với nhiều người dùng tham gia, việc lưu trữ dữ liệu đòi hỏi một phương pháp tiếp cận có nguyên tắc.

Dưới đây là 9 nguyên tắc cốt lõi và một số kỹ năng mở rộng mà mọi lập trình viên Backend cần nắm vững khi khởi tạo bảng trong MySQL, đảm bảo ứng dụng không chỉ chạy đúng mà còn hiệu quả và dễ bảo trì:

**1. Mọi Table Luôn Phải Có Các Column Mặc Định**

Một thiết kế table hoàn chỉnh cần có ít nhất 5 trường mặc định để theo dõi lịch sử và tính nhất quán của dữ liệu:

• **version**: Ghi lại số lần chỉnh sửa của table, đồng thời liên quan đến các khái niệm khóa lạc quan (optimistic lock) và khóa bi quan (pessimistic lock)

• **creator_id**: (Tùy chọn, tùy thuộc vào công ty) Ai là người tạo bản ghi này

• **modifier**: Ai là người cuối cùng sửa đổi bản ghi, quan trọng để biết hành động cuối cùng trên table

• **create_at**: Thời gian bản ghi được tạo

• **update_at**: Thời gian bản ghi được cập nhật lần cuối

**2. Giải Thích Ngữ Nghĩa Các Column Bằng Comment**

Khi viết DDL (Data Definition Language) cho MySQL, PostgreSQL, hoặc bất kỳ hệ quản trị cơ sở dữ liệu nào, **hãy luôn thêm comment giải thích ý nghĩa của từng column**. Điều này đặc biệt quan trọng cho các trường kiểu liệt kê (enumeration) như `status` (ví dụ: 1 là private, 2 là public, 3 là friends, 4 là only me). Việc comment rõ ràng giúp các thành viên mới gia nhập team dễ dàng hiểu và làm quen với cấu trúc dữ liệu, tránh sự hiểu lầm về ngữ nghĩa của các trường

**3. Xóa Dữ Liệu Không Phải Xóa "Bay" (Xóa Logic)**

**Không bao giờ sử dụng lệnh** **DELETE** **để xóa vật lý dữ liệu trực tiếp trong môi trường sản phẩm**. Thay vào đó, hãy sử dụng phương pháp **xóa logic (soft delete)** bằng cách thêm một trường để đánh dấu bản ghi đã bị xóa hay chưa, và thời gian xóa

• Ban đầu có thể sử dụng hai trường: `is_deleted` (0: hoạt động, 1: đã xóa) và `deleted_at` (thời gian xóa)

• Cách tối ưu hơn là **chỉ sử dụng một trường** **deleted_at**: Nếu giá trị là `NULL` nghĩa là bản ghi chưa bị xóa; nếu có giá trị thời gian, đó là thời gian bản ghi bị xóa

• **Lưu ý**: Giá trị `NULL` có thể gây nhược điểm nghiêm trọng về hiệu suất index khi dữ liệu lớn, do đó cần cân nhắc kỹ hoặc tìm hiểu sâu hơn về `NULL` trong database

**4. Quy Ước Đặt Tên Với Prefix (Tiền Tố)**

Các trường (field) trong table nên có các tiền tố (prefix) để dễ dàng xác định nguồn gốc khi các bảng được join lại với nhau. Ví dụ, bảng `account` có thể có trường `acc_number`. Việc này cực kỳ quan trọng vì trong thực tế, chúng ta ít khi làm việc với dữ liệu độc lập mà thường phải join nhiều bảng (ít nhất 3 bảng là nguyên tắc làm việc). Nếu không có prefix, việc phân biệt `ID` hay `create_at` thuộc về bảng nào khi join sẽ gây ra sự hiểu nhầm và lỗi

**5. Tách Bảng Khi Có Quá Nhiều Trường (Vertical Partitioning)**

Một table không nên có quá nhiều trường (column), **tối đa khoảng 20 trường**. Nếu vượt quá, cần phải tách bảng dọc (vertical partition). Bảng có nhiều trường sẽ làm dữ liệu lưu trữ lớn, giảm hiệu suất truy vấn và tốn bộ nhớ

• **Tách bảng**: Chia thành một bảng chính chứa các trường được truy cập thường xuyên và quan trọng (ví dụ: `title`, `status`, `thumbnail` của một bài post), và một bảng chi tiết chứa các trường ít quan trọng hơn hoặc chỉ hiển thị khi người dùng click vào (ví dụ: `content`, `description`)

• Mối quan hệ giữa hai bảng này thường là **1-1**, giúp việc join đơn giản và hiệu quả, không ảnh hưởng đến hiệu suất

**6. Chọn Kiểu Dữ Liệu và Độ Dài Thích Hợp**

Một hệ thống tốt không chỉ chạy đúng mà còn phải chạy hiệu quả. Việc chọn kiểu dữ liệu và độ dài phù hợp giúp:

• **Tiết kiệm bộ nhớ (memory)** và dung lượng đĩa (disk)

• **Tối ưu tốc độ query**

• **Giảm tỷ lệ Input/Output (I/O)**. Ví dụ:

1. Trường `title` không nên để `VARCHAR(255)` nếu độ dài thực tế chỉ khoảng 100 ký tự (như tiêu đề video YouTube/TikTok)

2. Trường `language` chỉ cần `CHAR(2)` (ví dụ: "en", "vi") thay vì `VARCHAR` dài

3. Trường `status` chỉ nên dùng **TINYINT** (kích thước 1 byte, lưu trữ 0-255) thay vì `INT` (kích thước 4 byte, lưu trữ 0-4 tỷ ID) nếu các giá trị chỉ là 1, 2, 3

**7. Nguyên Tắc Not NULL**

**Không nên cho phép giá trị** **NULL** **bừa bãi**. `NULL` không phải là một số, một chuỗi hay một biến boolean; nó là một vùng không xác định. `NULL` có thể:

• Làm hỏng logic nghiệp vụ nếu quên xử lý

• Gây lỗi index khi so sánh bằng `NULL` (ví dụ `WHERE column IS NULL` thường không sử dụng index hiệu quả). Các trường bắt buộc phải có giá trị (như `title`, `status`, `create_at`) nên được khai báo là **NOT NULL**. Khi không có giá trị, hãy sử dụng **DEFAULT** đi kèm với `NOT NULL`

**8. Chiến Lược Đánh Index**

Index là chìa khóa để tối ưu hiệu suất truy vấn

• **Nên đánh index** cho các trường ít trùng lặp và thường xuyên được sử dụng trong truy vấn, ví dụ: `creator_id` và `create_at` (quan trọng khi truy vấn theo thời gian). Luôn có prefix `idx_` cho các index

• **Trường** **deleted_at** **luôn cần được đánh index** để tránh hiển thị các bản ghi đã bị xóa ra công khai, điều này có thể dẫn đến các vấn đề pháp lý (ví dụ: GDPR của Châu Âu)

• **QUY TẮC VÀNG**: **Không nên đánh index cho các trường có dữ liệu lặp lại quá nhiều** (ví dụ: trường `status` mà 90% bản ghi có cùng một giá trị). Việc đánh index trong trường hợp này thậm chí có thể làm chậm truy vấn hơn so với không đánh index, vì database sẽ quét toàn bộ table thay vì sử dụng index

• **Giải pháp thay thế khi cần truy vấn các trường có nhiều giá trị trùng lặp**:

1. **Thêm trường tiền tố phạm vi thời gian**: Ví dụ, kết hợp `status` với `create_at` theo phạm vi thời gian (`WHERE status = 1 AND create_at BETWEEN '2025-06-15 00:00 :00' AND '2025-06-15 23:59:59'`) để giúp index hoạt động hiệu quả hơn

2. **Chia table thành các phân vùng (Partition)**: Phù hợp với dữ liệu lớn, giúp chia nhỏ dữ liệu. Tuy nhiên, Partition không thay thế được index và có nhược điểm riêng, chỉ nên dùng khi thực sự cần và hiểu rõ

3. **Tạo View**: View có thể hoạt động rất tốt trong các truy vấn với stored procedure hoặc function, giúp truy vấn nhanh hơn khi dữ liệu được lặp lại và cảm thấy đúng đánh lặp lại

**9. Nguyên Tắc Normal Form (3NF, 4NF, 5NF)**

Normalization là một nguyên tắc cơ bản trong thiết kế database nhằm giảm thiểu sự dư thừa dữ liệu và cải thiện tính toàn vẹn dữ liệu

• **3NF (Third Normal Form)** là một nguyên tắc cơ bản cần nắm vững

• Ngoài ra, còn có các dạng chuẩn mở rộng hơn như **4NF (Fourth Normal Form)** và **5NF (Fifth Normal Form)**, giúp tối ưu hóa hơn nữa về sự mở rộng và tính linh hoạt của database

. Việc tìm hiểu sâu về các Normal Form này sẽ giúp bạn thiết kế database hiệu quả hơn cho các mô hình kinh doanh phức tạp

**Kết Luận**

Các nguyên tắc là kim chỉ nam quan trọng, nhưng chúng ta cũng cần linh hoạt mở rộng chúng để phục vụ cho mô hình kinh doanh cụ thể của dự án. Nguyên tắc có thể bị phá vỡ bởi một nguyên tắc khác tốt hơn trong một hoàn cảnh cụ thể, nhưng nếu chưa có lý do chính đáng để phá vỡ, hãy cố gắng tuân thủ chúng. Việc nắm vững và áp dụng những nguyên tắc này sẽ giúp bạn xây dựng những ứng dụng Backend mạnh mẽ, ổn định và dễ dàng mở rộng trong tương lai.

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*