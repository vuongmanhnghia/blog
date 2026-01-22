---
title: Điều gì xảy ra khi bạn sử dụng lệnh Sudo ?
date: 2025-11-30
image:
categories:
  - linux
  - system
tags:
  - sudo
draft: false
---

Khi bạn gõ `sudo apt update`, không đơn giản là hệ thống "bật công tắc" quyền admin. Đó là một chuỗi các thao tác kiểm tra nghiêm ngặt, thay đổi định danh (Identity) và làm sạch môi trường.

<!--more-->

---

Trước khi tìm hiểu về **Sudo**, bạn nên hiểu về Điều gì sảy ra sau khi sử dụng Command (non-sudo) tại [System Calls](posts/linux/system-calls)

### Giai đoạn 1: Tại Shell (User Space)

Ngay khi bạn nhấn Enter, Shell (Bash/Zsh) của bạn bắt đầu làm việc:

1. **Parsing (Phân tích cú pháp):**
    
    - Shell cắt chuỗi `sudo fdisk -l` thành các token:
        
        - Main Command: `sudo`
            
        - Argument 1: `fdisk`
            
        - Argument 2: `-l`
            
2. **Path Resolution (Tìm đường dẫn):**
    
    - Shell tìm xem `sudo` nằm ở đâu bằng cách quét biến `$PATH` của user hiện tại (`/usr/local/bin`, `/usr/bin`, `/bin`...).
        
    - Nó tìm thấy `/usr/bin/sudo`.
	
### Giai đoạn 2: Khởi chạy Sudo - Quyền lực ngầm (SUID)

Trước khi lệnh chạy, hãy nhìn vào file thực thi của `sudo`

```bash
ls -l /usr/bin/sudo
# Kết quả: -rwsr-xr-x 1 root root ...
```

Bạn thấy chữ **`s`** ở phần quyền hạn (`rws`) không? Đó là **SUID bit**.
	
*   **Bình thường:** Khi bạn chạy một chương trình, nó chạy với quyền của **bạn** (User ID của bạn).
	
*   **Với SUID:** Khi bạn chạy `sudo`, hệ điều hành sẽ chạy nó với quyền của **người sở hữu file** (ở đây là `root`).

Shell gọi Kernel để chạy `/usr/bin/sudo`. Đây là điểm mấu chốt đầu tiên:

1. **Cơ chế SUID (Set User ID):**
    
    - Kernel nhìn vào metadata (Inode) của file `/usr/bin/sudo` và thấy bit **s** (`-rwsr-xr-x`).
        
    - Thay vì chạy `sudo` với quyền của user `devops`, Kernel khởi chạy tiến trình `sudo` với quyền của người sở hữu file này -> **Root**.
        
    - **Kết quả:** Tiến trình sudo vừa sinh ra đã có **Effective UID = 0** (Quyền tối cao).

---

### Giai đoạn 3. Policy Check - `/etc/sudoers`

Dù `sudo` đang chạy với quyền root, nó chưa vội thực thi lệnh của bạn. Nó phải kiểm tra xem bạn có "đủ tuổi" không.
	
*   Nó đọc file `/etc/sudoers` (và thư mục `/etc/sudoers.d/`).
	
*   Nó kiểm tra:
	
    *   User của bạn có nằm trong nhóm được phép (thường là `wheel` hoặc `sudo`) không?
		
    *   Bạn được phép chạy lệnh gì? (ALL commands hay chỉ một số lệnh cụ thể).
		
    *   Bạn có cần nhập mật khẩu không? (`NOPASSWD` hay mặc định).
	
---

### Giai đoạn 4. Xác thực qua PAM (Pluggable Authentication Modules)

Nếu cấu hình yêu cầu mật khẩu, `sudo` không tự kiểm tra mật khẩu (nó không đọc `/etc/shadow`). Nó nhờ một "bảo vệ" chuyên nghiệp tên là **PAM**.
	
*   `sudo` gửi yêu cầu đến thư viện PAM.
	
*   PAM hỏi mật khẩu của **User hiện tại** (không phải mật khẩu root).
	
*   Nếu nhập sai 3 lần -> PAM báo lỗi -> `sudo` ghi log cảnh báo và thoát.

**Cơ chế Timestamp:**

Nếu bạn nhập đúng, `sudo` sẽ tạo một file timestamp (thường ở `/run/sudo/ts/`). Trong vòng 15 phút (mặc định), nếu bạn gọi lại `sudo`, nó kiểm tra timestamp này còn hạn không. Nếu còn, nó bỏ qua bước hỏi mật khẩu.

---

### Giai đoạn 5. Làm sạch và Thiết lập Môi trường (Environment Sanitization)

Để tránh việc user lợi dụng các biến môi trường để hack quyền root, `sudo` sẽ:
	
1.  **Xóa bỏ các biến nguy hiểm:** Đặc biệt là `LD_PRELOAD` (biến này cho phép chèn mã độc vào thư viện động) và `LD_LIBRARY_PATH`.
	
2.  **Reset `$PATH`:**
	
	-  `sudo` ghi đè biến `$PATH` cũ bằng giá trị `secure_path` trong `/etc/sudoers` (để bao gồm `/sbin`, `/usr/sbin`).
	
	- *Nhờ bước này, hệ thống mới "nhìn thấy" lệnh `fdisk` nằm trong `/usr/sbin*`
	
3.  **Thiết lập biến định danh:**
	
    *   `$HOME` trỏ về `/root`.
		
    *   `$USER`, `$LOGNAME` chuyển thành `root`.
		
    *   *(Trừ khi bạn dùng `sudo -E` để giữ nguyên môi trường cũ - nhưng rất rủi ro).*
	
---

### Giai đoạn 6. Ghi Log (Logging)

Trước khi thực sự chạy lệnh, `sudo` ghi lại hành động này để làm bằng chứng (Audit trail).
	
*   Ghi vào: `/var/log/auth.log` (Ubuntu/Debian) hoặc `/var/log/secure` (RHEL/CentOS).
	
*   Nội dung: "User A đã chạy lệnh B vào giờ C tại thư mục D".
	
---

### Giai đoạn 7. Fork và Exec (Chuyển giao quyền lực)

Bây giờ mọi thủ tục đã xong, `sudo` thực hiện bước cuối cùng để chạy lệnh bạn muốn (ví dụ: `apt update`).
	
1.  **`fork()`:** `sudo` tạo ra một tiến trình con (Child process).
	
2.  **Trong tiến trình con:**
	
    *   Gọi system call `setuid(0)` và `setgid(0)`: Lệnh này chính thức đóng dấu "Tôi là Root" vào tiến trình con này vĩnh viễn.
	
    *   Gọi `execve()`: Thay thế mã nguồn của `sudo` bằng mã nguồn của lệnh đích (`apt`).
	
3.  **Trong tiến trình cha (`sudo`):**
	
    *   Nó vẫn chạy và đợi (wait) tiến trình con.
		
    *   Nó đóng vai trò trung gian chuyển tiếp tín hiệu (Signals). Ví dụ: Bạn bấm `Ctrl+C`, `sudo` nhận được và chuyển nó cho tiến trình con đang chạy `apt`.
	
---

### Giai đoạn 8. Kết thúc
	
*   Lệnh `apt` chạy xong và trả về Exit Code (0).
	
*   `sudo` nhận Exit Code đó và trả lại cho Shell của bạn.
	
*   Shell hiển thị lại dấu nhắc lệnh.

---

### Tóm tắt luồng đi (Flowchart dạng text)
	
1.  **User gõ lệnh:** `sudo vim /etc/hosts`
	
2.  **Kernel:** Chạy binary `sudo` với quyền Root (do SUID bit).
	
3.  **Sudo:**
	
    *   Đọc `/etc/sudoers`.
		
    *   Hỏi PAM: "Mật khẩu thằng này đúng không?".
		
    *   PAM: "Đúng".
		
    *   Ghi log vào `/var/log/auth.log`.
		
    *   Xóa biến môi trường độc hại, set lại `$PATH`.
		
    *   `fork()` -> Tạo process con.
	
4.  **Process Con:**
	
    *   `setuid(0)` (Thành root thật sự).
		
    *   `execve("vim")`.
	
5.  **Vim:** Mở ra với quyền `root`.