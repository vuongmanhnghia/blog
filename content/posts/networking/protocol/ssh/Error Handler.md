---
title: Hướng dẫn xử lý sự cố và các lỗi thường gặp khi thiết lập SSH
date: 2025-09-10
image: /thumb/ssh-error.png
categories:
    - protocol
tags:
    - ssh
draft: false
---

Ngay cả với một thiết lập cẩn thận, các vấn đề vẫn có thể phát sinh. Việc hiểu rõ cách chẩn đoán và khắc phục các lỗi SSH phổ biến là một kỹ năng quan trọng.

<!--more-->

## Chế độ Verbose

Trước khi thử bất kỳ giải pháp nào, bước đầu tiên luôn là thu thập thêm thông tin. Tùy chọn `-v` (verbose) của lệnh `ssh` sẽ in ra chi tiết quá trình kết nối, cho bạn biết file cấu hình nào đang được đọc, khóa nào đang được thử, và chính xác lỗi xảy ra ở đâu.

```bash
$ ssh -vT git@github.com
```

## Error 1: `Permission denied (publickey)`

-   **Ý nghĩa:** Đây là lỗi xác thực phổ biến nhất. Nó có nghĩa là máy chủ GitHub đã từ chối tất cả các khóa SSH mà client của bạn cung cấp.
	
-   **Các bước kiểm tra và khắc phục:**
	
    1. **Kiểm tra khóa trên GitHub:** Đảm bảo rằng khóa công khai của bạn đã được thêm chính xác vào tài khoản GitHub.
		
    2. **Kiểm tra `ssh-agent`:** Chạy `ssh-add -l` để xem các khóa hiện có trong agent. Nếu danh sách trống hoặc không chứa khóa bạn cần, hãy chạy lại `ssh-add ~/.ssh/your_private_key` để thêm nó vào.
		
    3. **Kiểm tra quyền truy cập file:** SSH yêu cầu quyền truy cập rất nghiêm ngặt. Thư mục `~/.ssh` phải có quyền là `700` (drwx−−−−−−), và file khóa riêng tư của bạn phải có quyền là `600` (−rw−−−−−−−). Sử dụng các lệnh sau để sửa:
	
        ```bash
        $ chmod 700 ~/.ssh
        $ chmod 600 ~/.ssh/your_private_key
        ```
	
    4. **Kiểm tra `~/.ssh/config`:** Nếu bạn đang sử dụng file cấu hình, hãy kiểm tra kỹ lưỡng xem `Host` alias có khớp với URL remote của Git không, và `IdentityFile` có trỏ đến đúng file khóa riêng tư không.
	
## Error 2: `Host key verification failed`

-   **Ý nghĩa:** Dấu vân tay của máy chủ GitHub đã thay đổi so với lần cuối bạn kết nối. Đây là một cơ chế bảo mật quan trọng để cảnh báo về khả năng có một cuộc tấn công Man-in-the-Middle.
	
-   **Cách khắc phục an toàn:**
	
    1. **Không bao giờ** bỏ qua cảnh báo này một cách mù quáng.
		
    2. Truy cập trang tài liệu chính thức của GitHub để xác minh dấu vân tay máy chủ mới nhất của họ.
		
    3. Nếu dấu vân tay khớp, bạn có thể an toàn xóa khóa cũ khỏi file `~/.ssh/known_hosts` bằng lệnh:
		
        ```bash
        $ ssh-keygen -R github.com
        ```
	
## Error 3: `Agent admitted failure to sign using the key`
	
-   **Ý nghĩa:** `ssh-agent` đang chạy nhưng không thể sử dụng khóa để tạo chữ ký số cần thiết cho việc xác thực. Lỗi này đôi khi xảy ra trên các hệ thống Linux.
	
-   **Cách khắc phục:** Giải pháp thường rất đơn giản là tải lại khóa vào agent. Chạy lệnh `ssh-add` thường sẽ giải quyết được vấn đề này.
	
## Error 4: `Key is already in use`
	
-   **Ý nghĩa:** Bạn đang cố gắng thêm một khóa công khai vào tài khoản GitHub, nhưng khóa đó đã được sử dụng ở một nơi khác - hoặc trên một tài khoản người dùng khác, hoặc trong một kho lưu trữ khác dưới dạng "deploy key".
	
-   **Nguyên tắc:** Một khóa SSH phải là định danh duy nhất cho một người dùng trên toàn bộ nền tảng GitHub. Khi được sử dụng làm deploy key, nó cũng phải là duy nhất cho mỗi kho lưu trữ.
	
-   **Cách khắc phục:**
	
    1. Sử dụng lệnh sau để xác định tài khoản nào đang sử dụng khóa đó:
		
        ```bash
        $ ssh -T -ai ~/.ssh/your_key git@github.com
        ```
		
    2. Gỡ khóa khỏi tài khoản hoặc kho lưu trữ cũ, hoặc đơn giản là tạo một cặp khóa hoàn toàn mới cho mục đích sử dụng mới.
	
## Error 5: Các Phương Pháp Bảo Mật Tốt Nhất (Best Practices) và Tổng Kết

Làm chủ SSH không chỉ dừng lại ở việc thiết lập thành công. Việc duy trì một tư thế bảo mật vững chắc đòi hỏi sự chú ý liên tục. Các phương pháp tốt nhất có thể được tóm gọn trong một vòng đời bảo mật của khóa SSH.

### Vòng Đời Bảo Mật Của Khóa SSH

-   **Tạo (Creation):**
	
    -   **Thuật toán mạnh:** Luôn ưu tiên sử dụng **`Ed25519`** vì hiệu suất và bảo mật vượt trội.
		
    -   **Passphrase mạnh:** Luôn đặt một passphrase mạnh và duy nhất cho mỗi khóa. Sử dụng trình quản lý mật khẩu để lưu trữ an toàn các passphrase này.
	
-   **Bảo vệ (Protection):**
	
    -   **Quyền truy cập file:** Duy trì quyền truy cập file chính xác là điều bắt buộc: `chmod 700 ~/.ssh` và `chmod 600 ~/.ssh/private_key`.
		
    -   **Bí mật tuyệt đối:** **Không bao giờ** chia sẻ, gửi qua email, hoặc lưu trữ khóa riêng tư của bạn ở bất kỳ đâu ngoài máy tính cá nhân đã được bảo vệ. Chỉ có khóa công khai là an toàn để chia sẻ.
	
-   **Sử dụng (Usage):**
	
    -   **Sử dụng `ssh-agent`:** Tận dụng `ssh-agent` để giảm thiểu số lần phải nhập passphrase, qua đó giảm nguy cơ bị keylogger ghi lại.
		
    -   **Cấu hình timeout cho agent:** Để tăng cường bảo mật, hãy đặt thời gian tồn tại cho các khóa trong agent bằng tùy chọn `-t`. Lệnh `ssh-add -t 3600` sẽ yêu cầu agent "quên" khóa sau một giờ (3600 giây) không hoạt động. Điều này cực kỳ hữu ích để bảo vệ chống lại việc truy cập trái phép nếu máy tính của bạn bị bỏ lại mà không được khóa.
	
-   **Bảo trì (Maintenance):**
	
    -   **Kiểm tra định kỳ (Audit):** Lên lịch (ví dụ: hàng quý) để truy cập trang cài đặt SSH trên GitHub và xem lại danh sách các khóa đã được cấp quyền. Xóa ngay lập tức bất kỳ khóa nào bạn không nhận ra, không còn sử dụng, hoặc thuộc về các thiết bị đã mất.
		
    -   **Xoay vòng khóa (Rotation):** Một thực hành bảo mật nâng cao là định kỳ tạo một cặp khóa mới và thay thế các khóa cũ. Việc này giới hạn "cửa sổ cơ hội" cho một kẻ tấn công nếu một khóa cũ bị xâm phạm mà bạn không hề hay biết.
	
---
