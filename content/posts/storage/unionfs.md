---
title: UnionFS - Union File System
date: 2025-12-28
image:
categories:
  - storage
tags:
  - unionfs
draft: false
---

UnionFS cho phép bạn "xếp chồng" nhiều thư mục (hoặc ổ đĩa) khác nhau lên nhau để tạo thành một hệ thống tệp tin duy nhất và thống nhất

<!--more-->

---

**UnionFS** (**Union File System**) là một dịch vụ hệ thống tệp tin (filesystem service) cho Linux, FreeBSD và NetBSD.

### 1. Cơ chế hoạt động (Hãy tưởng tượng về các "Layer")

Để dễ hình dung, hãy tưởng tượng UnionFS giống như các **Layer (lớp) trong Photoshop** hoặc các tấm phim trong suốt xếp chồng lên nhau:

*   **Xếp chồng:** Bạn có thư mục A và thư mục B. UnionFS cho phép bạn gộp chúng lại thành thư mục C.
	
*   **Thứ tự ưu tiên:** Khi bạn nhìn vào thư mục C, bạn sẽ thấy nội dung của cả A và B. Nếu cả A và B đều có một file tên là `text.txt`, thì file nằm ở lớp trên (ví dụ là A) sẽ được hiển thị, file ở lớp dưới (B) sẽ bị che khuất.
	
*   **Trong suốt:** Người dùng hoặc ứng dụng khi truy cập vào thư mục C sẽ không biết nó được ghép từ A và B, họ chỉ thấy một thư mục bình thường.

### 2. Hai tính năng kỹ thuật quan trọng

UnionFS trở nên mạnh mẽ nhờ hai cơ chế xử lý file:

*   **Copy-on-Write (CoW):**
	
    *   Thường thì lớp dưới cùng là **Read-only** (Chỉ đọc - không thể sửa), và lớp trên cùng là **Writeable** (Có thể ghi).
		
    *   Nếu bạn muốn sửa một file nằm ở **Read-only** layer, UnionFS sẽ tự động **copy** file đó lên lớp **Writeable** layer, sau đó áp dụng thay đổi trên bản copy đó. File gốc ở dưới vẫn giữ nguyên.
	
*   **Whiteout (Xóa giả):**
	
    *   Nếu bạn xóa một file nằm ở **Read-only** layer, UnionFS không thể xóa nó thật (vì là chỉ đọc).
		
    *   Thay vào đó, nó tạo ra một "dấu hiệu" (whiteout) ở lớp trên cùng để che file đó đi. Hệ thống nhìn vào sẽ tưởng là file đã bị xóa.

### 3. Ứng dụng thực tế (Tại sao lại cần UnionFS?)

UnionFS (và các biến thể hiện đại hơn như **OverlayFS**, **AuFS**) là công nghệ cốt lõi của nhiều công cụ phổ biến:

*   **Docker & Container:** Đây là ứng dụng nổi tiếng nhất.
	
    *   Một Docker Image gồm nhiều lớp (layers) xếp chồng lên nhau (ví dụ: lớp OS, lớp thư viện, lớp ứng dụng).
		
    *   Khi bạn chạy container, Docker dùng công nghệ kiểu UnionFS để gộp các lớp read-only đó lại và thêm một lớp writable mỏng ở trên cùng để bạn thao tác. Điều này giúp tiết kiệm dung lượng ổ cứng cực lớn (các container có thể dùng chung các lớp dưới).
	
*   **Live CD / Live USB Linux:**
	
    *   Khi bạn chạy Ubuntu từ USB mà không cài đặt, hệ điều hành nằm trên USB là dạng nén, chỉ đọc (Read-only).
	
    *   Mọi thay đổi bạn làm (tạo file, cài phần mềm) được lưu vào RAM (lớp Writable).
	
    *   UnionFS gộp lớp USB và lớp RAM lại để bạn dùng như một máy tính bình thường. Khi tắt máy, lớp RAM mất đi, USB vẫn nguyên vẹn.
	
*   **Firmware Router/IoT:** Giúp khôi phục cài đặt gốc dễ dàng. Hệ điều hành gốc nằm ở lớp dưới (bảo vệ tuyệt đối), cài đặt của người dùng nằm ở lớp trên. Khi "Reset", chỉ cần xóa lớp trên là xong.

### 4. Tình trạng hiện nay

Mặc dù thuật ngữ "UnionFS" vẫn hay được dùng để chỉ chung cho công nghệ này, nhưng dự án **UnionFS** gốc hiện nay ít được sử dụng trực tiếp trong các nhân Linux hiện đại.

Thay vào đó, **OverlayFS** là công nghệ kế thừa, ổn định hơn và đã được tích hợp chính thức vào Linux Kernel, đang được sử dụng bởi Docker và hầu hết các hệ thống hiện nay.

**Tóm lại:** UnionFS là công nghệ "xếp hình" các thư mục, cho phép giữ nguyên file gốc trong khi vẫn có thể chỉnh sửa trên một lớp ảo phủ lên trên.

---

### Bài viết liên quan

- [OverlayFS](posts/storage/overlayfs)
	
- [Tại sao overlay2 trên Docker lại có hiệu năng kém hơn Volume/Bind Mount ?](overlay2-vs-volume-&-bind-mount)

---