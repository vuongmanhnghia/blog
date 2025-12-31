---
title: Các mẫu thiết kế, xây dựng hệ thống với Cache và chiến lược vô hiệu hóa Cache
date: 2025-08-10
image: /image-placeholder.png
categories:
  - architechture
  - system
tags:
  - cache
draft: true
---


<!--more-->

---

## Các Mẫu Thiết Kế

### Cache-Aside (Lazy Loading)

Đây là mẫu thiết kế phổ biến và trực quan nhất. Trong mẫu này, logic của ứng dụng chịu trách nhiệm hoàn toàn cho việc quản lý cache.

-   **Quy trình:**
	
    -   Ứng dụng cần đọc dữ liệu, nó sẽ kiểm tra cache trước.
		
    -   Nếu có (cache hit), dữ liệu được trả về.
		
    -   Nếu không có (cache miss), **ứng dụng** sẽ đọc dữ liệu từ database.
		
    -   Sau đó, **ứng dụng** sẽ ghi dữ liệu vừa đọc được vào cache.
		
    -   Khi ghi dữ liệu, ứng dụng thường sẽ cập nhật database trước, sau đó **vô hiệu hóa (invalidate)** mục tương ứng trong cache.
    ![Image Description](posts/imagespasted-image-20250810134139png)
-   **Ưu điểm:** Ứng dụng có toàn quyền kiểm soát. Cache chỉ lưu những dữ liệu thực sự được yêu cầu, giúp tiết kiệm không gian. Hệ thống có khả năng chống chịu lỗi cache tốt (nếu cache sập, ứng dụng có thể đọc trực tiếp từ database).
	
-   **Nhược điểm:** Yêu cầu đầu tiên cho bất kỳ dữ liệu nào cũng sẽ là cache miss. Code của ứng dụng phức tạp hơn vì phải chứa logic quản lý cache.

### Read-Through

Mẫu này trừu tượng hóa database khỏi ứng dụng. Ứng dụng chỉ cần "nói chuyện" với cache.

-   **Quy trình:**
	
    -   Ứng dụng yêu cầu dữ liệu từ cache.
		
    -   Nếu cache có, nó sẽ trả về.
		
    -   Nếu cache không có, **chính cache** sẽ chịu trách nhiệm đi lấy dữ liệu từ database, lưu lại rồi trả về cho ứng dụng.
	
-   **Ưu điểm:** Đơn giản hóa code ứng dụng vì logic caching được đóng gói trong cache provider.
	
-   **Nhược điểm:** Kém linh hoạt hơn. Cache provider phải hỗ trợ mẫu này.

### Write-Through và Write-Behind (Write-Back)

Đây là các mẫu tập trung vào việc ghi, thường đi đôi với Read-Through.

-   **Write-Through:** Ứng dụng ghi dữ liệu vào cache, và **cache** sẽ chịu trách nhiệm ghi đồng bộ dữ liệu đó vào database. Điều này đảm bảo tính nhất quán cao.
	
-   **Write-Behind:** Ứng dụng ghi dữ liệu vào cache, và **cache** sẽ ghi dữ liệu đó vào database một cách bất đồng bộ (trong nền). Điều này cho hiệu năng ghi rất cao.
	
-   **Cache-Aside** đặt trách nhiệm điều phối dữ liệu lên vai ứng dụng. Ứng dụng "biết" cả về cache và database.
-   **Read/Write-Through** coi cache như một lớp mặt tiền (facade) cho database. Ứng dụng chỉ cần biết "lấy dữ liệu" hoặc "ghi dữ liệu" tại một điểm duy nhất là cache.

Mô hình Read-Through thúc đẩy sự phân tách trách nhiệm sạch sẽ hơn, dẫn đến code ứng dụng đơn giản và dễ bảo trì hơn. Tuy nhiên, nó lại ràng buộc chặt chẽ cache với database, khiến việc thay đổi database hoặc sử dụng cache cho các nguồn dữ liệu khác trở nên khó khăn. Ngược lại, Cache-Aside linh hoạt hơn – cache có thể chứa dữ liệu từ nhiều nguồn (database, API, file,...) – nhưng phải trả giá bằng sự phức tạp tăng lên trong code ứng dụng. Đây là một sự đánh đổi kinh điển giữa đơn giản/đóng gói và linh hoạt/kiểm soát.

## Dữ Liệu Cũ và Vô Hiệu Hóa Cache

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
	
Vấn đề "khó" của cache invalidation không chỉ nằm ở việc _khi nào_ cần vô hiệu hóa, mà là làm thế nào để đảm bảo việc vô hiệu hóa đó là _chính xác_ và _nguyên tử_ trong một môi trường có nhiều tiến trình chạy đồng thời.

Hãy xem xét kịch bản sau trong mẫu Cache-Aside:

1. Tiến trình A đọc dữ liệu X. Bị cache miss.
	
2. Tiến trình A đi đến database để đọc dữ liệu X (phiên bản cũ).
	
3. Trong lúc đó, tiến trình B cập nhật dữ liệu X trong database và ngay lập tức gửi lệnh vô hiệu hóa cache cho X.
	
4. Tiến trình A, sau khi đọc xong dữ liệu X (phiên bản cũ) từ database, giờ đây lại ghi nó vào cache.
	
5. **Kết quả:** Cache bây giờ chứa dữ liệu X đã lỗi thời, và lệnh vô hiệu hóa của tiến trình B trở nên vô nghĩa. Dữ liệu lỗi thời này sẽ tồn tại trong cache cho đến khi TTL hết hạn.
	![Image Description](posts/imagespasted-image-20250810134758png)

## Kết luận

Nếu có một điều cần đọng lại, đó là: **Cache không phải là một viên đạn bạc, mà là một kỹ thuật mạnh mẽ đòi hỏi sự đánh đổi thông minh.**

Mỗi quyết định bạn đưa ra – chọn loại cache nào, chính sách dọn dẹp ra sao, chính sách ghi nào, mẫu thiết kế nào – đều là một sự cân bằng giữa các yếu tố:

-   **Hiệu năng** và **Chi phí**
	
-   **Độ phức tạp** và **Tính đơn giản**
	
-   **Tính nhất quán dữ liệu** và **Độ trễ**
	
-   **Mô hình tối ưu nhất mà mình biết**
    ![Image Description](posts/imagespasted-image-20250810135418png)
---
