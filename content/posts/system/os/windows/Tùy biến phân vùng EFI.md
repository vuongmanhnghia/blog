---
title: Hướng dẫn tùy biến phân vùng EFI khi cài windows
date: 2025-09-08
image: /images/image-placeholder.png
categories:
    - System
    - OS
tags:
    - windows
    - boot
    - UFI
draft: false
---

Thông thường khi cài windows, mặc định sẽ tự tạo phân vùng Boot EFI 512MB, bài viết này sẽ hướng dẫn bạn cách tùy biến size phân vùng EFI

<!--more-->

## Sử dụng Command Prompt trong quá trình cài đặt

-   **Khởi động từ USB** và đến màn hình chọn ổ đĩa
-   **Nhấn Shift + F10** để mở **Command Prompt**
-   **Chạy các command sau:**

```cmd
diskpart
list disk
select disk 0 (thay 0 bằng số ổ đĩa của bạn)
clean
convert gpt
create partition efi size=4096
format quick fs=fat32 label="System"
assign letter=S
create partition msr size=128
create partition primary
format quick fs=ntfs label="Windows"
assign letter=C
active
exit
```

-   **Đóng Command Prompt** và tiếp tục cài đặt bình thường
-   Chọn phân vùng `Windows` vừa tạo để cài đặt
