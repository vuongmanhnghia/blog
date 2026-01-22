---
title: Vai trò và cách hoạt động của OpenSSH Suite
date: 2025-12-20
image:
categories:
  - protocol
tags:
  - ssh
draft: false
---
**OpenSSH (Open Secure Shell)** là bộ công cụ mã nguồn mở triển khai giao thức SSH. Đây là "tiêu chuẩn vàng" được cài đặt mặc định trên hầu hết các hệ điều hành Linux, macOS và cả Windows hiện đại

<!--more-->

---

Để hiểu rõ cách nó hoạt động, chúng ta sẽ mổ xẻ từng thành phần trong bộ OpenSSH Suite theo chức năng của chúng: **Server**, **Client**, **Quản lý khóa**, và **Truyền tải**.

---

## I. Kết nối cơ bản
### 1. `sshd` (SSH Daemon) - "Người gác cổng"

Đây là thành phần quan trọng nhất chạy trên **Server**.

*   **Vai trò:**
	
    *   Luôn luôn chạy ngầm (background process) trên máy chủ.
		
    *   Lắng nghe tại cổng 22 (mặc định) để chờ kết nối từ bên ngoài.
		
    *   Quyết định ai được vào, ai bị chặn.
	
*   **Cách hoạt động:**
	
    1.  Khi nhận được tín hiệu kết nối từ Client, `sshd` sẽ thực hiện bắt tay (handshake) để thiết lập mã hóa.
		
    2.  Nó kiểm tra danh tính người dùng (dựa trên Password hoặc SSH Key).
		
    3.  Nếu xác thực thành công, `sshd` sẽ tạo ra một phiên làm việc (session) mới và khởi chạy môi trường dòng lệnh (shell) cho người dùng đó.
		
    4.  Mọi lệnh bạn gõ từ máy mình sẽ được `sshd` nhận, thực thi trên server, rồi gửi kết quả trả về cho bạn.
	
*   **File cấu hình:** `/etc/ssh/sshd_config` (Nơi bạn chỉnh port, tắt login root, tắt password...).

---

### 2. `ssh` (SSH Client) - "Khách"

Đây là lệnh bạn gõ trên máy tính cá nhân (**Client**).

*   **Vai trò:**
	
    *   Khởi tạo kết nối đến Server.
		
    *   Đọc các file cấu hình của người dùng để biết nên kết nối thế nào (dùng key nào, port nào).
		
    *   Mã hóa dữ liệu bạn gõ và gửi đi.
	
*   **Cách hoạt động:**
	
    1.  Bạn gõ `ssh user@host`.
		
    2.  `ssh` tìm file `~/.ssh/config` (nếu có) để xem có cài đặt đặc biệt nào không.
		
    3.  Nó kết nối đến `sshd` ở phía kia.
		
    4.  Nó kiểm tra `~/.ssh/known_hosts` để xem server này có phải server quen không (tránh giả mạo).
		
    5.  Sau khi kết nối xong, nó biến thành cái "loa": Bạn gõ gì nó gửi đi, Server trả lời gì nó hiện lên màn hình.

---

## II. Bộ công cụ quản lý khóa (Key Management)

### 1. `ssh-keygen` - "Máy đúc chìa"
	
*   **Vai trò:** Tạo ra cặp khóa Public/Private.
	
*   **Cách hoạt động:** Nó dùng thuật toán toán học (RSA, Ed25519) để sinh ra 2 chuỗi ký tự ngẫu nhiên có liên kết toán học với nhau.
	
    *   Nó tạo file `id_rsa` (Private - Cất kỹ).
		
    *   Nó tạo file `id_rsa.pub` (Public - Mang đi phát).
	
### 2. `ssh-copy-id` - "Người đưa thư"
	
*   **Vai trò:** Copy Public Key lên Server một cách an toàn và đúng chuẩn.
	
*   **Cách hoạt động:**
	
    1.  Nó kết nối SSH vào server (lần này vẫn cần mật khẩu).
		
    2.  Nó lấy nội dung file `id_rsa.pub` của bạn.
		
    3.  Nó tự động tạo thư mục `~/.ssh` trên server (nếu chưa có).
		
    4.  Nó ghi nội dung key vào file `~/.ssh/authorized_keys` trên server.
		
    5.  Nó set quyền (permission) cho file đó thật chặt chẽ để chỉ user đó mới đọc được (nếu quyền lỏng lẻo, SSH sẽ từ chối key).

### 3. `ssh-agent` & `ssh-add` - "Quản gia giữ chìa"
	
*   **Vấn đề:** Để bảo mật, khi tạo Private Key, bạn thường đặt thêm mật khẩu (passphrase) cho chính cái Key đó. Nghĩa là mỗi lần dùng Key để login, bạn lại phải nhập pass của Key. Rất phiền.
	
*   **Giải pháp:**
	
    *   **`ssh-agent`:** Là một chương trình chạy ngầm trong RAM máy bạn.
		
    *   **`ssh-add`:** Bạn gõ lệnh này, nhập pass của Key **một lần duy nhất**. `ssh-agent` sẽ giải mã Key đó và giữ nó trong RAM.
		
    *   **Kết quả:** Từ đó về sau, khi bạn `ssh` đi đâu, `ssh` sẽ hỏi mượn Key từ `ssh-agent` chứ không hỏi bạn nữa. Bạn không cần gõ pass lại cho đến khi tắt máy.

---

## III. Bộ công cụ truyền file

OpenSSH tận dụng đường hầm bảo mật đã thiết lập để truyền file.

### 1. `scp` (Secure Copy)
	
*   **Vai trò:** Copy file nhanh gọn.
	
*   **Cách hoạt động:** Nó mở một kết nối SSH, nhưng thay vì chạy shell, nó chạy một quy trình copy dữ liệu. Nó đọc file nguồn, mã hóa, gửi qua đường hầm, và bên kia ghi lại thành file đích.
	
*   *Lưu ý:* `scp` đang dần bị thay thế bởi `sftp` trong các phiên bản mới vì lý do kiến trúc bảo mật, nhưng cách dùng vẫn y hệt.

### 2. `sftp` (Secure File Transfer Protocol)
	
*   **Vai trò:** Quản lý file từ xa (giống FTP nhưng an toàn).
	
*   **Cách hoạt động:**
	
    *   Nó là một **Subsystem** (hệ thống con) của SSH.
		
    *   Khi kết nối, `sshd` sẽ kích hoạt phân hệ SFTP server.
		
    *   Nó cho phép bạn thực hiện nhiều thao tác hơn `scp`: liệt kê file, đổi tên, xóa file, tạo thư mục, resume (tải tiếp) file bị đứt quãng.

---

## IV. Các file cấu hình quan trọng (Cần nhớ)

Để làm chủ OpenSSH, bạn phải biết các file này nằm đâu:

| Vị trí          | Tên file                 | Vai trò                                                                                                                                        | Thuộc về |
| :-------------- | :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- | :------- |
| **Trên Server** | `/etc/ssh/sshd_config`   | Cấu hình toàn bộ hành vi của Server (Port, Quyền login...).                                                                                    | `sshd`   |
| **Trên Server** | `~/.ssh/authorized_keys` | Danh sách các Public Key được phép mở cửa vào nhà.                                                                                             | `sshd`   |
| **Trên Client** | `/etc/ssh/ssh_config`    | Cấu hình mặc định cho mọi user trên máy client.                                                                                                | `ssh`    |
| **Trên Client** | `~/.ssh/config`          | Cấu hình riêng cho cá nhân bạn (Alias, User, Port riêng cho từng server).                                                                      | `ssh`    |
| **Trên Client** | `~/.ssh/known_hosts`     | Lưu "vân tay" (fingerprint) của các server đã từng kết nối. Nếu server bị thay đổi (hoặc bị hack), vân tay thay đổi, file này sẽ cảnh báo bạn. | `ssh`    |

## V. Tóm tắt quy trình phối hợp:
	
1.  **Bạn** dùng `ssh-keygen` tạo khóa.
	
2.  **Bạn** dùng `ssh-copy-id` ném khóa sang Server (vào file `authorized_keys`).
	
3.  **Bạn** gõ `ssh`.
	
4.  **Client** (`ssh`) hỏi **Agent** (`ssh-agent`) lấy khóa.
	
5.  **Client** nói chuyện với **Server** (`sshd`).
	
6.  **Server** kiểm tra `authorized_keys`, thấy khớp -> Cho vào.

---