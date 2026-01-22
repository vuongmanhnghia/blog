---
title: Hướng dẫn sửa lỗi authorized khi SSH vào raspberry pi
date: 2025-09-26
image: /image-placeholder.png
categories:
  - system
  - experience
tags:
  - pi
  - ssh
draft: false
---

Hướng dẫn sửa lỗi authorized khi SSH vào raspberry pi

<!--more-->

---
## Sửa trực tiếp trên Thẻ nhớ

- Tắt Pi và tháo thẻ nhớ SD.
    
- Cắm thẻ nhớ vào máy tính của bạn (bạn có thể cần một đầu đọc thẻ).
    
- Truy cập vào phân vùng có tên `rootfs` (hoặc phân vùng có dung lượng lớn hơn).
    
- Đi đến đường dẫn `/home/nagih/.ssh/`.
    
- **Kiểm tra file `authorized_keys`**: Mở nó ra và đảm bảo nội dung của file `~/.ssh/id_ed25519.pub` trên máy tính của bạn được chép chính xác vào đây, trên một dòng duy nhất.
    
- **Kiểm tra quyền (khó hơn)**: Việc kiểm tra và sửa quyền file trên thẻ SD từ một máy tính khác (như Windows) là không khả thi. Nếu bạn dùng Linux, bạn có thể `mount` thẻ nhớ và dùng `chmod` để sửa.