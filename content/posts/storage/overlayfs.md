---
title: OverlayFS - overlay2 on Docker
date: 2025-12-28
image:
categories:
  - storage
tags:
  - overlayfs
draft: false
---

Nếu UnionFS là ý tưởng, thì OverlayFS là bản thực thi xuất sắc nhất hiện nay trên Linux. Nó khắc phục được sự cồng kềnh và chậm chạp của các thế hệ trước (như AUFS hay Device Mapper)

<!--more-->

---

Tiếp nối câu chuyện về UnionFS, chúng ta sẽ đi sâu vào **OverlayFS** (cụ thể là driver `overlay2` trong Docker).

### 1. Kiến trúc 4 thành phần của OverlayFS

Khác với cách nói chung chung "xếp lớp", OverlayFS định nghĩa cấu trúc rất rõ ràng với 4 thư mục chính khi mount:

1.  **LowerDir (Tầng dưới - Read-only):**
	
    *   Đây chính là các **Docker Image layers**.
		
    *   Nó có thể bao gồm nhiều lớp xếp chồng lên nhau.
		
    *   Đặc điểm: Chỉ được đọc, tuyệt đối không được sửa.
	
2.  **UpperDir (Tầng trên - Read-Write):**
	
    *   Đây là **Container layer**.
		
    *   Nơi chứa tất cả những thay đổi bạn thực hiện khi container đang chạy (file mới tạo, file bị sửa).
	
3.  **Merged (Tầng hợp nhất - View):**
	
    *   Đây là điểm mount mà người dùng nhìn thấy (ví dụ `/var/lib/docker/overlay2/.../merged`).
		
    *   Nó ảo hóa việc gộp `LowerDir` và `UpperDir`.
	
4.  **WorkDir (Tầng đệm):**
	
    *   Đây là thư mục nội bộ để OverlayFS xử lý các tác vụ trung gian (như chuẩn bị file trước khi di chuyển sang UpperDir) để đảm bảo tính toàn vẹn dữ liệu (atomicity).

### 2. Cơ chế hoạt động chi tiết (Deep Dive)

OverlayFS hoạt động ở cấp độ **File (Tệp tin)**, không phải cấp độ Block (Khối đĩa). Điều này rất quan trọng để hiểu hiệu năng.

**A. Đọc file (Reading)**

*   Nếu file nằm ở `UpperDir`: Hệ thống đọc ngay lập tức (Rất nhanh).
	
*   Nếu file không có ở `Upper` mà chỉ có ở `Lower`: Hệ thống đọc từ `Lower`.
	
*   **Hiệu năng:** Gần như tốc độ ổ cứng gốc (Native speed).

**B. Ghi file (Writing & Copy_up) - Điểm mấu chốt**

Đây là lúc cơ chế **Copy-on-Write (CoW)** của OverlayFS hoạt động, thuật ngữ chuyên ngành gọi là **`copy_up`**:

1.  Bạn mở một file 100MB có sẵn trong Image (Lower) để sửa.
	
2.  OverlayFS nhận lệnh ghi. Nó tạm dừng lại.
	
3.  Nó tìm file đó ở `LowerDir`.
	
4.  Nó **COPY toàn bộ file 100MB** đó lên `UpperDir`.
	
5.  Sau khi copy xong, nó mới cho phép ứng dụng ghi dữ liệu vào bản sao ở `UpperDir`.

> **Lưu ý quan trọng:** OverlayFS hoạt động theo file. Dù bạn chỉ sửa 1 ký tự trong file 1GB, nó cũng phải copy cả file 1GB đó lên trên. Đây là lý do nó chậm hơn Volume khi ghi lần đầu.

**C. Xóa file (Deleting & Whiteout)**

Làm sao xóa file ở `LowerDir` (vốn Read-only)?

*   OverlayFS tạo ra một file đặc biệt trong `UpperDir` gọi là **Whiteout file** (thường là một character device với major/minor number là 0/0).
	
*   File này trùng tên với file cần xóa.
	
*   Khi bạn nhìn vào thư mục `Merged`, OverlayFS thấy file Whiteout này và sẽ "ẩn" file gốc ở dưới đi.

### 3. Tại sao Overlay2 lại tốt hơn các UnionFS cũ (như AUFS)?

Trước đây Docker dùng AUFS, nhưng giờ chuyển sang Overlay2 vì 2 lý do cực lớn:

**1. Page Cache Sharing (Chia sẻ bộ nhớ đệm) - Cực kỳ quan trọng**

Hãy tưởng tượng bạn chạy **10 Container** từ cùng một Image `node:latest`.

*   Image này có file `/usr/bin/node` (nặng 50MB).
	
*   **Với các công nghệ cũ (Device Mapper):** Nó có thể tải 10 bản copy vào RAM -> Tốn 500MB RAM.
	
*   **Với OverlayFS:** Vì các lớp `LowerDir` là giống hệt nhau về mặt vật lý, Linux Kernel thông minh nhận ra chúng cùng chung một **Inode** trên ổ cứng.
	
    *   Kernel chỉ tải file `/usr/bin/node` vào RAM **một lần duy nhất** (Page Cache).
		
    *   Cả 10 container đều dùng chung vùng nhớ đệm đó.
		
    *   **Kết quả:** Tiết kiệm RAM khủng khiếp khi chạy nhiều container giống nhau (ví dụ trong Kubernetes).

**2. Tốc độ và Sự đơn giản**

*   OverlayFS được tích hợp trực tiếp vào **Linux Kernel Mainline**. Nó không cần cài thêm module ngoài. Code của nó gọn nhẹ hơn nhiều so với AUFS.
	
*   Tốc độ tạo container (mount overlay) nhanh hơn rất nhiều so với việc tạo snapshot của Device Mapper.

**4. Giới hạn của OverlayFS**

Dù rất tốt, OverlayFS vẫn có điểm yếu mà bạn cần biết khi vận hành hệ thống:

1.  **Rename Directory (Đổi tên thư mục):** OverlayFS (chuẩn POSIX) không hỗ trợ hoàn hảo việc đổi tên thư mục nếu thư mục đó nằm ở lớp `Lower` và bạn muốn đổi tên nó ở lớp `Upper`. Docker phải dùng mẹo (copy thư mục cũ sang tên mới rồi xóa cũ) -> Rất tốn kém nếu thư mục lớn.
	
2.  **Không phù hợp ghi dữ liệu lớn:** Như đã nói, vì cơ chế copy toàn bộ file (`copy_up`), nên tuyệt đối không để Database file trên OverlayFS.
	
3.  **Inode exhaustion (Cạn kiệt Inode):** Đây là vấn đề của driver `overlay` cũ. Driver `overlay2` đã khắc phục được điều này, nhưng nếu bạn tạo quá nhiều file nhỏ trong container, bạn vẫn có thể làm hết Inode của ổ cứng host.

**Tóm lại:** OverlayFS là sự kết hợp hoàn hảo giữa tốc độ đọc (nhờ Page Cache sharing) và khả năng quản lý layer linh hoạt. Tuy nhiên, bản chất "Copy nguyên file" khi ghi đè khiến nó luôn thua Volume ở các tác vụ ghi nặng (Write-heavy workloads).

---

### Bài viết liên quan

- [UnionFS](posts/storage/unionfs)
	
- [Tại sao overlay2 trên Docker lại có hiệu năng kém hơn Volume/Bind Mount ?](overlay2-vs-volume-&-bind-mount)

---

