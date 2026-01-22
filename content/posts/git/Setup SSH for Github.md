---
title: Hướng dẫn thiết lập khóa SSH cho github
description: Hướng dẫn chi tiết từng bước để tạo và cấu hình khóa SSH cho tài khoản GitHub
date: 2025-09-10
image: /thumb/setup-ssh.png
categories:
  - protocol
  - tool
tags:
  - ssh
  - git
draft: false
---
---
## Bước 1: Tạo Cặp Khóa SSH với `ssh-keygen`

### Thuật toán Mã hóa
	
-   **Ed25519 (Khuyến nghị):** Đây là thuật toán hiện đại, được khuyến nghị sử dụng. Ed25519 cung cấp mức độ bảo mật rất cao với độ dài khóa ngắn hơn, giúp quá trình xác thực diễn ra nhanh hơn.
	
    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
    
-   **RSA (Lựa chọn thay thế):** RSA là một thuật toán cũ. Nếu bạn cần hỗ trợ các hệ thống cũ không tương thích với Ed25519.
	
    ```bash
    ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
	
- **Nhập passphrase** (Nếu cần)
	
	- Passphrase này sẽ mã hóa file khóa riêng tư của bạn trên đĩa
		
	- Ngay cả khi máy tính của bạn bị đánh cắp và kẻ tấn công có được file khóa riêng tư, họ cũng không thể sử dụng nó nếu không biết passphrase.
	
### Lưu khóa và Đặt tên file

Mặc định, `ssh-keygen` sẽ lưu cặp khóa vào thư mục `~/.ssh/` với tên file là `id_ed25519` và `id_ed25519.pub` (hoặc `id_rsa` cho RSA). Có thể đặt tên là `~/.ssh/id_ed25519_personal` cho tài khoản cá nhân và `~/.ssh/id_ed25519_work` cho tài khoản công việc.

## Bước 2: Quản Lý Khóa với `ssh-agent`
	
-   **Khởi động ssh-agent:**
	
    Chạy lệnh sau trong terminal để khởi động agent cho phiên làm việc hiện tại.
	
    ```bash
    eval "$(ssh-agent -s)"
    ```
	
-   **Thêm khóa riêng tư vào ssh-agent:**
	
    Bạn sẽ được yêu cầu nhập **passphrase** nếu đã tạo.
    
    ```bash
    ssh-add ~/.ssh/id_ed25519
    ```
	
## Bước 3: Thêm Public Key vào GitHub Account
	
-   **Copy Public Key**
	
    -   **macOS:**
		
        ```bash
        pbcopy < ~/.ssh/id_ed25519_personal.pub
        ```
	    
    -   **Linux/Windows (Git Bash hoặc WSL):**
		
        ```bash
        cat ~/.ssh/id_ed25519.pub
        ```
		
		Copy public key được in ra màn hình.
	    
-   **Thêm khóa vào GitHub:**
	
    -   Truy cập tài khoản GitHub của bạn trên Browser.
		
    -   Vào **Settings** (Cài đặt)
		
    -   Trong thanh bên trái, chọn **SSH and GPG keys** (Khóa SSH và GPG).
		
    -   Nhấp vào nút **New SSH key** (Khóa SSH mới).
		
    -   Trong trường **Title**, đặt một cái tên mang tính mô tả cho khóa của bạn (ví dụ: "MacBook Pro Cá Nhân").
		
    -   Trong trường **Key**, dán nội dung khóa công khai bạn đã sao chép.
		
    -   Nhấp vào Add SSH key (Thêm khóa SSH) để hoàn tất.
	
## Bước 4: Kiểm Tra Kết Nối
	
-   Chạy lệnh kiểm tra:
	
    ```bash
    ssh -T git@github.com
    ```
    
-   Xác thực máy chủ (lần đầu tiên):
	
    ```bash
    The authenticity of host 'github.com (IP_ADDRESS)' can't be established.
    ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
    Are you sure you want to continue connecting (yes/no)?
    ```
    Đây là một tính năng bảo mật của SSH để chống lại các cuộc tấn công xen giữa (man-in-the-middle). Sau khi xác nhận, gõ `yes` và nhấn Enter.
-   Kết quả thành công:
    ```bash
    Hi username! You've successfully authenticated, but GitHub does not provide shell access.
    ```
    
    Điều này xác nhận rằng cặp khóa SSH của bạn đã được thiết lập chính xác và GitHub đã xác thực thành công danh tính của bạn.
	
---