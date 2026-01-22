---
title: Inode trong Linux File System
date: 2025-11-30
image:
categories:
  - linux
  - system
tags:
  - file
draft: false
---

**Inode** (viết tắt của **Index Node**) là một khái niệm cốt lõi và cực kỳ quan trọng trong các hệ thống tập tin (filesystem) của Linux và Unix.

<!--more-->

---

Để hiểu đơn giản: Nếu coi dữ liệu của một file là "nội dung cuốn sách", thì **Inode** chính là "thẻ mục lục" của cuốn sách đó trong thư viện.

### 1. Inode chứa những gì?

Mỗi file trên Linux được gán một số định danh duy nhất gọi là **Inode number**. Inode là một cấu trúc dữ liệu lưu trữ tất cả thông tin về file (metadata), **trừ tên file và nội dung thực sự của file**.

Thông tin trong một Inode bao gồm:
	
*   **Loại file:** (File thường, thư mục, symbolic link, block device...).
	
*   **Quyền hạn (Permissions):** Read, Write, Execute cho Owner, Group, và Others.
	
*   **Chủ sở hữu (Owner/Group):** User ID (UID) và Group ID (GID).
	
*   **Kích thước file (File size):** Dung lượng tính bằng byte.
	
*   **Tem thời gian (Timestamps):**
		
    *   Created (thời điểm tạo).
		
    *   Modified (lần cuối sửa nội dung).
		
    *   Accessed (lần cuối mở file).
		
*   **Số lượng liên kết cứng (Hard link count):** Có bao nhiêu tên file trỏ vào inode này.
	
*   **Vị trí dữ liệu (Pointers to data blocks):** Quan trọng nhất, nó chỉ ra vị trí cụ thể trên ổ cứng nơi dữ liệu thực sự của file được lưu trữ.
	
### 2. Cái gì KHÔNG nằm trong Inode?

Đây là điểm thú vị nhất: **Tên file (Filename) không nằm trong Inode.**
	
*   Tên file được lưu trong dữ liệu của **Thư mục (Directory)** chứa file đó.
	
*   Thư mục thực chất là một file đặc biệt, nội dung của nó chỉ là một danh sách ánh xạ giữa **Tên file** và **Số Inode** tương ứng.
	
### 3. Quy trình truy cập một file diễn ra như thế nào?

Khi bạn gõ lệnh `cat data.txt` hoặc mở một file, hệ thống sẽ làm như sau:
	
1.  Đọc thư mục hiện tại để tìm tên `data.txt`.
	
2.  Lấy số Inode tương ứng với tên `data.txt` (ví dụ: Inode #12345).
	
3.  Truy cập vào Inode #12345 để kiểm tra quyền hạn (bạn có quyền đọc không?).
	
4.  Nếu có quyền, nó dùng các "con trỏ" trong Inode để tìm đến các khối (blocks) trên ổ cứng chứa nội dung văn bản.
	
5.  Hiển thị nội dung lên màn hình.

### 4. Tại sao Inode lại quan trọng?

**a. Hard Links (Liên kết cứng)**

Vì tên file và dữ liệu file (Inode) tách biệt nhau, nên Linux cho phép nhiều tên file khác nhau cùng trỏ vào một số Inode duy nhất.
	
*   Nếu bạn tạo một hard link cho File A thành File B, cả hai đều trỏ vào cùng một Inode.
	
*   Xóa File A không làm mất dữ liệu, vì Inode vẫn còn (do File B vẫn giữ liên kết). Dữ liệu chỉ thực sự bị xóa khi số lượng liên kết (link count) trong Inode giảm về 0.

**b. Di chuyển file (Move) rất nhanh**

Khi bạn dùng lệnh `mv` để di chuyển file trong cùng một phân vùng (partition), hệ thống không hề sao chép dữ liệu của file. Nó chỉ đơn giản là cập nhật lại đường dẫn trong các thư mục để trỏ về số Inode cũ. Do đó, việc di chuyển file 10GB diễn ra tức thì.

**c. Lỗi "No space left on device" dù ổ cứng còn trống**

Mỗi phân vùng (partition) có một số lượng Inode giới hạn được định sẵn khi format (định dạng).
	
*   Nếu bạn tạo hàng triệu file cực nhỏ (ví dụ 1KB), bạn có thể dùng hết số lượng Inode cho phép dù dung lượng ổ cứng (GB) vẫn còn trống rất nhiều.
	
*   Khi hết Inode, bạn không thể tạo thêm file mới nào nữa.
	
### 5. Các lệnh thường dùng với Inode

*   **Xem số Inode của file:**

    ```bash
    ls -i ten_file
    # Hoặc
    ls -li
    ```

*   **Xem chi tiết thông tin Inode:**

    ```bash
    stat ten_file
    ```

*   **Kiểm tra dung lượng và số lượng Inode còn trống:**

    ```bash
    df -i
    # Cột IUse% cho biết bạn đã dùng bao nhiêu phần trăm Inode.
    ```

---