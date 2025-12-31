---
title: Tại sao overlay2 trên Docker lại có hiệu năng kém hơn Volume và Bind Mount ?
date: 2025-12-28
image:
categories:
  - docker
  - storage
tags:
  - overlayfs
  - unionfs
  - cow
draft: false
---

Nguyên nhân cốt lõi nằm ở **Cơ chế Copy-on-Write (CoW)** và **lớp trung gian (Overhead)**

<!--more-->

---
Mặc dù `overlay2` là driver lưu trữ (storage driver) tốt nhất và được khuyến nghị mặc định cho Docker hiện nay, nhưng về mặt vật lý và logic, nó **không thể nhanh bằng** Volume hoặc Bind Mount.

Dưới đây là 4 lý do kỹ thuật chi tiết giải thích tại sao `overlay2` lại chậm hơn, đi sâu vào cơ chế xử lý file:

### 1. Cơ chế `copy_up` ở cấp độ File (File-level Copy-on-Write) - Nguyên nhân lớn nhất

Đây là sự khác biệt chí mạng giữa `overlay2` và Volume.

*   **Volume/Bind Mount (Native Filesystem - ext4/xfs):**
	
    *   Khi bạn sửa một file 1GB, hệ thống file (filesystem) chỉ đơn giản là tìm đến địa chỉ (block) của file đó trên ổ cứng và ghi đè dữ liệu mới vào.
		
    *   Nếu bạn chỉ sửa 1KB cuối file, nó chỉ ghi đúng 1KB đó. **Chi phí gần như bằng 0.**
	
*   **Overlay2:**
	
    *   `overlay2` hoạt động ở cấp độ **File**, không phải cấp độ Block.
		
    *   Khi bạn sửa một file (vốn nằm ở lớp Image/Read-only), `overlay2` buộc phải kích hoạt quy trình `copy_up`.
		
    *   **Quy trình:** Nó phải đọc **toàn bộ file gốc** từ lớp dưới $\rightarrow$ Tạo một file mới ở lớp trên (UpperDir) $\rightarrow$ Ghi toàn bộ dữ liệu cũ vào $\rightarrow$ Sau đó mới áp dụng thay đổi của bạn.
		
    *   **Hệ quả:** Nếu bạn sửa 1 byte trong file log nặng 1GB nằm trong Image, hệ thống phải tốn công Copy cả 1GB đó sang lớp ghi. Điều này gây ra độ trễ (latency) cực lớn (I/O burst) ngay tại thời điểm ghi lần đầu tiên.
	
### 2. Overhead của VFS (Virtual File System) và Tra cứu Inode

Volume là đường thẳng, `overlay2` là đường vòng.

*   **Volume:**
	
    *   Ứng dụng gọi lệnh `open()` $\rightarrow$ Hệ điều hành trỏ thẳng tới Inode trên đĩa $\rightarrow$ Xong.
		
    *   Đường đi ngắn nhất, ít rào cản nhất.
	
*   **Overlay2:**
	
    *   Khi ứng dụng gọi lệnh `open()` hoặc `ls`, Kernel không thể đi thẳng.
		
    *   Nó phải đi qua lớp logic của OverlayFS driver.
		
    *   Driver này phải kiểm tra xem file đó nằm ở `UpperDir` hay `LowerDir`? (Quét các lớp).
		
    *   Nó phải kiểm tra xem file đó có bị đánh dấu là "Whiteout" (đã xóa giả) hay không?
		
    *   Việc logic "nếu - thì" này tốn CPU cycles. Mặc dù rất nhỏ cho mỗi file, nhưng với các ứng dụng web đọc/ghi hàng nghìn file nhỏ (như PHP, Node.js `node_modules`), độ trễ sẽ cộng dồn lại thành đáng kể.

### 3. Vấn đề với các thao tác Metadata (Rename, chmod, chown)

Một số thao tác tưởng chừng đơn giản lại trở nên phức tạp trên OverlayFS:

*   **Rename (Đổi tên thư mục):**
	
    *   Trên Volume (ext4), đổi tên thư mục chỉ là việc sửa đổi metadata, tốn vài mili-giây bất kể thư mục nặng bao nhiêu GB.
		
    *   Trên OverlayFS, chuẩn POSIX không hỗ trợ đầy đủ việc đổi tên thư mục nếu nó nằm ở lớp Read-only. Hệ thống có thể phải thực hiện việc "Copy toàn bộ thư mục sang tên mới rồi xóa cũ". Nếu thư mục đó chứa nhiều data, đây là thảm họa hiệu năng.
		
    *   *Lưu ý: Các phiên bản Kernel mới có tính năng "redirect_dir" để giảm nhẹ vấn đề này, nhưng nó vẫn phức tạp hơn native.*

### 4. Không tận dụng được tối đa các tính năng của Filesystem gốc

*   Volume nằm trực tiếp trên ext4 hoặc xfs của máy chủ (Host). Nó hưởng trọn vẹn các tính năng tối ưu của các hệ thống file này (như extent mapping, delayed allocation...).
	
*   OverlayFS là một lớp phủ. Mọi yêu cầu phải đi qua nó trước khi xuống ext4/xfs. Lớp trung gian này đôi khi làm cản trở các thuật toán tối ưu hóa luồng I/O của hệ điều hành.

---

### 5. Tóm tắt so sánh trực quan

Hãy tưởng tượng bạn muốn sửa một dòng chữ trong một trang sách:

1.  **Volume/Bind Mount:** Bạn cầm bút, viết thẳng lên trang sách đó. (Nhanh, trực tiếp).
	
2.  **Overlay2:** Trang sách đó được ép plastic (Read-only).
	
    *   Bạn phải lấy một tờ giấy trắng (Upper layer).
		
    *   Bạn phải đặt tờ giấy trắng lên trên trang sách.
		
    *   Bạn phải **đồ lại (trace)** toàn bộ nội dung của trang sách cũ lên tờ giấy mới (`copy_up`).
		
    *   Sau đó bạn mới sửa dòng chữ trên tờ giấy mới.

**Kết luận:**

Chính vì thao tác "đồ lại" (`copy_up`) và việc phải quản lý nhiều tờ giấy xếp chồng lên nhau khiến `overlay2` luôn chậm hơn việc viết trực tiếp (Volume).

Đó là lý do tại sao quy tắc vàng trong Docker luôn là: **Code để trong Container (Overlay2) vì ít khi sửa đổi, nhưng Data (Database, Logs) bắt buộc phải để trong Volume.**

--- 

### Bài viết liên quan

- [UnionFS](posts/storage/unionfs)
	
- [OverlayFS](posts/storage/overlayfs)

---