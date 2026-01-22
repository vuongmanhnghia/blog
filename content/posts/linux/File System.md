---
title: Linux File System
date: 2025-11-30
image:
categories:
  - linux
  - system
  - architechture
tags:
  - file
draft: false
---
<!--more-->

---
### 1. "Everything is a file"

Trong Linux, mọi thứ đều là tập tin (hoặc được biểu diễn như một tập tin):
	
*   **Dữ liệu:** Văn bản, hình ảnh, code.
	
*   **Thiết bị phần cứng:** Ổ cứng (`/dev/sda`), bàn phím, chuột.
	
*   **Tiến trình (Process):** Thông tin về RAM, CPU (`/proc`).
	
*   **Socket/Pipe:** Giao tiếp mạng.
	

---

### 2. Cấu trúc thư mục chuẩn (Filesystem Hierarchy Standard - FHS)

| Folder                | Meaning                                                                                                                                                                              |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/` (Root)            | Gốc của hệ thống. Chỉ user `root` mới có quyền ghi.                                                                                                                                  |
| `/bin` & `/usr/bin`   | Chứa các lệnh cơ bản (`ls`, `cp`, `docker`).                                                                                                                                         |
| `/sbin` & `/usr/sbin` | Chứa lệnh quản trị hệ thống (`iptables`, `reboot`).                                                                                                                                  |
| **`/etc`**            | **Quan trọng:** Chứa file cấu hình (Nginx, SSH, Systemd). Đây là nơi Configuration Management (Ansible/Chef) tác động nhiều nhất.                                                    |
| **`/var`**            | **Quan trọng:** Chứa dữ liệu biến đổi (Variable). <br> - `/var/log`: Log hệ thống (cần monitor để tránh đầy ổ cứng). <br> - `/var/lib`: Dữ liệu database (MySQL, Docker containers). |
| `/home`               | Thư mục cá nhân của user.                                                                                                                                                            |
| `/root`               | Thư mục cá nhân của user root.                                                                                                                                                       |
| `/tmp`                | File tạm. Sẽ bị xóa khi reboot. **Cảnh báo:** Đừng lưu data quan trọng ở đây.                                                                                                        |
| `/boot`               | Kernel và Bootloader.                                                                                                                                                                |
| `/opt`                | Phần mềm bên thứ 3 (thường dùng cho các ứng dụng cài thủ công như Java, Tomcat).                                                                                                     |
| **`/proc` & `/sys`**  | **Virtual Filesystem:** Không chiếm dung lượng ổ cứng, nằm trên RAM. Chứa thông tin kernel, process. Monitoring tool (Prometheus/Nagios) đọc data từ đây.                            |
| `/dev`                | Device files (`/dev/null`, `/dev/zero`, `/dev/random`).                                                                                                                              |

---

### 3. Cơ chế hoạt động (Under the Hood)

**A. Inode (Index Node)**

Mỗi file có 2 phần:
	
1.  **Data:** Nội dung thực sự của file.
	
2.  **Inode:** Metadata (Quyền hạn, chủ sở hữu, kích thước, vị trí block trên ổ cứng, thời gian tạo...).

**Kịch bản:**
	
*   **Lỗi:** "No space left on device" nhưng `df -h` thấy ổ cứng vẫn còn trống 50%.
	
*   **Nguyên nhân:** Hết **Inode** (do tạo quá nhiều file nhỏ, ví dụ: session files của PHP hoặc cache).
	
*   **Check:** `df -i`

**B. Superblock**

Chứa thông tin về chính File System đó (tổng số block, kích thước block, trạng thái mount). Nếu Superblock hỏng, FS sẽ không thể mount được.

**C. Journaling (Nhật ký)**

Các FS hiện đại (ext4, xfs) đều là Journaling File System. Nó ghi lại các thay đổi dự kiến vào một vùng log trước khi ghi thật sự.

*   **Lợi ích:** Giúp phục hồi dữ liệu nhanh chóng nếu mất điện đột ngột, giảm thiểu rủi ro lỗi file system (`fsck`).

---

### 4. Các loại File System phổ biến

Khi format ổ đĩa hoặc mount volume cho Database, bạn cần chọn đúng loại:

1.  **ext4 (Fourth Extended Filesystem):**
	
    *   Chuẩn mực, ổn định, tương thích tốt.
		
    *   Dùng cho: OS disk, General purpose.
	
2.  **XFS:**
	
    *   Hiệu năng cao với file lớn, mở rộng tốt (Scalability). Là mặc định của RHEL/CentOS.
		
    *   Dùng cho: Database server, CI/CD artifacts storage.
		
    *   *Lưu ý:* XFS không thể thu nhỏ (shrink) partition, chỉ có thể mở rộng.
	
3.  **Btrfs & ZFS:**
	
    *   Hỗ trợ nâng cao: Snapshot, Pooling, Checksum (chống bit rot).
	
    *   Dùng cho: Storage Server, Backup server, Container storage driver.
	

---

### 5. Quyền hạn (Permissions) & Security

**A. Cơ bản (UGO - User Group Other)**
	
*   Read (4), Write (2), Execute (1).
	
*   Lệnh: `chmod`, `chown`.
	
**B. Nâng cao (Special Permissions)**
	
*   **SUID (Set User ID):** Chạy file với quyền của người sở hữu file (thường là root) thay vì người chạy lệnh. (Ví dụ: lệnh `passwd`). *Nguy cơ bảo mật cao.*
	
*   **SGID:** File tạo ra trong thư mục sẽ thừa kế Group của thư mục đó (Hữu ích cho Shared Folder).
	
*   **Sticky Bit:** Chỉ người tạo file mới xóa được file trong thư mục chung (Ví dụ: `/tmp`).
	
**C. ACL (Access Control Lists)**

Khi quyền UGO không đủ chi tiết (VD: Muốn user A đọc, user B ghi, user C không làm gì trên cùng 1 file), dùng `setfacl` và `getfacl`.

---

### 6. Quản lý lưu trữ (Storage Management)

**A. Mounting**

Gắn một thiết bị lưu trữ vào cây thư mục.
	
*   Lệnh: `mount /dev/sdb1 /mnt/data`
	
*   **Persist (Bền vững):** Cấu hình trong `/etc/fstab` để tự mount khi khởi động lại. *Lưu ý: Sai cú pháp fstab có thể làm máy không boot được.*
	
**B. LVM (Logical Volume Manager)**

Lớp trừu tượng giữa ổ cứng vật lý và File System.
	
*   **Physical Volume (PV):** Ổ cứng thật.
	
*   **Volume Group (VG):** Gom các PV lại thành 1 cục to.
	
*   **Logical Volume (LV):** Cắt VG ra để dùng (giống partition).
	
*   **Lợi ích cho DevOps:** Có thể mở rộng dung lượng ổ cứng (Resize) online mà không cần tắt server (Zero downtime).

---

### 7. File System trong thế giới Container (Docker/K8s)

**A. Union File System (OverlayFS)**

Docker images được xây dựng từ các **Layers** (lớp).
	
*   **LowerDir:** Các lớp Read-only (Base image).
	
*   **UpperDir:** Lớp Read-write (Container layer).
	
*   **Merged:** Cái bạn nhìn thấy khi chạy container.
	
*   **Cơ chế Copy-on-Write (CoW):** Khi container sửa một file từ image gốc, nó copy file đó lên lớp UpperDir để sửa, file gốc vẫn nguyên vẹn.

**B. Volumes & Bind Mounts**
	
*   Dữ liệu trong container là **Ephemeral** (mất khi container chết).
	
*   Để lưu dữ liệu bền vững (Database), phải dùng **Volume** (Docker quản lý tại `/var/lib/docker/volumes`) hoặc **Bind Mount** (map thư mục host vào container).

---

### 8. Các lệnh và kỹ năng Troubleshooting cần thiết

1.  **Kiểm tra dung lượng:**
	
    *   `df -hT`: Xem dung lượng tổng quát và loại FS.
	
    *   `du -sh *`: Xem thư mục nào chiếm nhiều chỗ nhất.
	
    *   `ncdu`: Công cụ giao diện dòng lệnh để soi dung lượng (rất tiện).
	
2.  **Kiểm tra I/O Performance:**
	
    *   `iostat -xz 1`: Xem tốc độ đọc ghi, %iowait.
	
    *   `iotop`: Xem tiến trình nào đang "ăn" ổ cứng.

3.  **Xử lý file đang mở (Locked files):**
	
    *   `lsof | grep deleted`: Tìm các file đã bị xóa nhưng process vẫn đang giữ (nguyên nhân phổ biến khiến xóa log rồi mà dung lượng không giảm).
	
    *   Giải pháp: Restart process đó (ví dụ: `systemctl reload nginx`).

4.  **Mount/Unmount:**
	
    *   `mount -a`: Mount tất cả trong fstab.
	
    *   `umount -l`: Lazy unmount (dùng khi thư mục đang bị busy/treo).
	
---
### Bài viết liên quan
	
- [Inode trong Linux File System](inode.md)
	
- [Điều gì sẽ xảy ra sau khi Command được gửi đi trên Linux](posts/linux/system-calls)
	
- [Điều gì sẽ xảy ra sau khi sử dụng Sudo](sudo.md)

---