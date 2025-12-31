---
title: Hướng dẫn tùy biến phân vùng EFI khi cài windows
date: 2025-09-08
image: /images/image-placeholder.png
categories:
  - system
  - os
tags:
  - windows
  - boot
  - UFI
draft: false
---

Thông thường khi cài windows, mặc định sẽ tự tạo phân vùng Boot EFI 512MB, bài viết này sẽ hướng dẫn bạn cách tùy biến size phân vùng EFI

<!--more-->

---
*Sử dụng Command Prompt trong quá trình cài đặt*

- **Bước 1:** Khởi động từ USB/DVD cài Windows
	
	- Khi màn hình xuất hiện, nhấn `Shift + F10` để mở `Command Prompt`
	
-   **Bước 2:** Sử dụng DiskPart để tạo phân vùng
	
	```sh
	diskpart
	list disk
	select disk 0 (Chọn ổ đĩa cần cài)
	clean
	convert gpt
	```
	
-   **Bước 3:** Tạo phân vùng EFI với size tùy chỉnh
	
	```sh
	create partition efi size=4096
	format quick fs=fat32 label="System"
	assign letter=S
	active
	```
	
	*Thay 4096 bằng size bạn muốn (MB)*
	
- **Bước 4:** Tạo phân vùng MSR
	
	```sh
	create partition msr size=128
	```
	
- **Bước 5:** Tạo phân vùng chính cho Windows
	
	```sh
	create partition primary
	format quick fs=ntfs label="Windows"
	assign letter=C
	active
	exit
	```
	
	*Thông thường hay xảy ra trường hợp ổ C đang được định nghĩa là USB Boot, lúc này hãy cứ thao tác bằng giao diện như bình thường*
	
---