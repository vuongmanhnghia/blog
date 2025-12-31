---
title: Điều gì sẽ xảy ra khi gõ bất kỳ command nào trong terminal trên Linux ?
date: 2025-11-30
image:
categories:
  - linux
  - system
  - workflow
tags:
  - kernel
draft: false
---
Để trả lời câu này sâu sắc, chúng ta không chỉ nhìn ở bề nổi (gõ lệnh -> ra kết quả), mà phải nhìn xuống tầng **Kernel** và **System Calls**

<!--more-->

---
### 1. Phân tích cú pháp (Parsing) & Tokenization

Khi bạn gõ ví dụ: `ls -l /var/log` và nhấn Enter:
	
*   **Shell (Bash/Zsh)** sẽ đọc dòng chữ đó.
	
*   Nó cắt chuỗi thành các **Tokens** (từ đơn):
	
    *   Command: `ls`
		
    *   Argument: `-l`
		
    *   Argument: `/var/log`
	
### 2. Kiểm tra Alias và Hàm (Aliases & Functions)

Trước khi tìm file để chạy, Shell kiểm tra **Alias** trước:
	
1.  **Alias:** Có phải bạn đã đặt `alias ls='ls --color=auto'` không? Nếu có, nó sẽ thay thế `ls` bằng lệnh đầy đủ.
	
2.  **Functions:** Có hàm nào tên là `ls` được định nghĩa trong `.bashrc` không?
	
### 3. Kiểm tra Shell Built-in (Lệnh nội tại)

Shell kiểm tra xem lệnh này có phải là **Built-in** không.
	
*   **Built-in:** Là lệnh nằm ngay trong code của Shell, không cần gọi file bên ngoài (Ví dụ: `cd`, `echo`, `alias`, `export`).
	
    *   *Tại sao `cd` phải là built-in?* Vì nếu `cd` là một chương trình bên ngoài, khi chạy nó sẽ tạo ra một tiến trình con (child process), tiến trình con đổi thư mục rồi tắt đi, tiến trình cha (Shell hiện tại) vẫn ở thư mục cũ. Do đó `cd` phải do chính Shell thực hiện.
	
*   **External:** `ls` không phải built-in, nên Shell tiếp tục bước sau.

### 4. Mở rộng (Expansion)

Shell xử lý các ký tự đặc biệt trước khi chạy lệnh:

*   **Brace expansion:** `echo {a,b}` -> `a b`
	
*   **Variable expansion:** `$HOME` -> `/home/user`
	
*   **Command substitution:** `$(date)` -> `Sun Nov 30...`
	
*   **Globbing (Wildcards):** `*.txt` -> danh sách file đuôi txt.
	
### 5. Tìm kiếm đường dẫn (Path Resolution)

Nếu lệnh không chứa đường dẫn tuyệt đối (như `/bin/ls`) mà chỉ là `ls`, Shell sẽ tìm trong biến môi trường **`$PATH`**.
	
*   Nó quét lần lượt: `/usr/local/bin` -> `/usr/bin` -> `/bin`...
	
*   Để tối ưu, Shell thường dùng **Hash Table** (bảng băm) để nhớ vị trí các lệnh đã chạy trước đó (gõ `hash` để xem).

### 6. Cơ chế Fork - Exec - Wait (Trái tim của Linux Process)

Đây là bước quan trọng nhất về mặt hệ thống (System Internals). Khi đã tìm thấy file thực thi `/usr/bin/ls`, Shell thực hiện 3 bước thần thánh:

1.  **`fork()` (Phân thân):**
	
    *   Shell (Process cha - Parent) gọi system call `fork()` để tạo ra một bản sao y hệt của chính nó (Process con - Child).
		
    *   Lúc này, ta có 2 tiến trình giống hệt nhau đang chạy.
	
2.  **`exec()` (Thay thế - Cụ thể là `execve`):**
	
    *   Trong Process con, nó gọi system call `execve()`.
		
    *   Lệnh này sẽ **xóa sạch** bộ nhớ của Process con và nạp mã nguồn của chương trình mới (`/usr/bin/ls`) vào thay thế.
		
    *   Process con giờ đây chính thức biến thành chương trình `ls`.
	
3.  **`wait()` (Chờ đợi):**
	
    *   Process cha (Shell) gọi `wait()` và tạm dừng hoạt động (ngủ) để chờ Process con chạy xong.
	
### 7. Nạp thư viện động (Dynamic Linking)

Trước khi `ls` thực sự chạy code của nó, Kernel thấy file này cần các thư viện `.so` (Shared Objects, giống `.dll` bên Windows).
	
*   Trình liên kết động (`ld-linux.so`) sẽ được gọi để load các thư viện cần thiết (như `libc.so`, `libselinux.so`...) vào bộ nhớ.
	
*   *DevOps Tip:* Dùng lệnh `ldd /bin/ls` để xem nó cần thư viện nào.
	
### 8. Thực thi và I/O
	
*   Chương trình `ls` chạy, đọc thư mục, format kết quả.
	
*   Nó ghi kết quả ra **Standard Output (stdout - File Descriptor 1)**. Mặc định stdout trỏ về màn hình terminal của bạn nên bạn thấy chữ hiện lên.

### 9. Kết thúc (Termination)
	
*   Khi `ls` chạy xong, nó gọi `exit(0)` (0 nghĩa là thành công).
	
*   Kernel gửi tín hiệu **SIGCHLD** cho Process cha (Shell) báo rằng "Con ông xong việc rồi".
	
*   Shell thức dậy từ lệnh `wait()`, thu thập **Exit Code** (mã thoát).
		
    *   *DevOps Tip:* Mã này được lưu vào biến `$?`. Bạn có thể `echo $?` để xem. (0 = OK, khác 0 = Lỗi).
	
### 10. Prompt quay lại

Shell in lại dấu nhắc lệnh (ví dụ: `user@host:~$`) và chờ đợi lệnh tiếp theo của bạn.
