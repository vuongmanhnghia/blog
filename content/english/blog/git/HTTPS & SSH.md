---
title: SSH - Github
meta_title: SSH - Github
description: SSH and GitHub Tutorial
date: 2025-09-01
image: /images/image-placeholder.png
categories:
  - protocol
  - git
author: Nagih
tags:
  - ssh
draft: false
---
Những hạn chế của xác thực qua HTTPS và sự thay thế SSH
<!--more-->
Trong hệ sinh thái phát triển phần mềm hiện đại, GitHub không chỉ là một kho lưu trữ mã nguồn mà còn là trung tâm cộng tác, quản lý dự án và triển khai ứng dụng. Việc tương tác hiệu quả và an toàn với nền tảng này là một kỹ năng cơ bản đối với mọi nhà phát triển. Mặc dù HTTPS cung cấp một phương thức kết nối ban đầu đơn giản, việc chuyển sang sử dụng giao thức SSH (Secure Shell) là một bước tiến quan trọng, không chỉ nâng cao đáng kể mức độ bảo mật mà còn tối ưu hóa quy trình làm việc hàng ngày.

### 1. Những Hạn Chế của Xác thực qua HTTPS

Khi bắt đầu với Git và GitHub, hầu hết người dùng đều chọn HTTPS vì sự đơn giản của nó. Tuy nhiên, phương thức này có những hạn chế cố hữu. Xác thực qua HTTPS yêu cầu sử dụng Personal Access Token (PAT), một chuỗi ký tự hoạt động tương tự như mật khẩu.

Mặc dù dễ thiết lập, quy trình này bộc lộ sự bất tiện trong quá trình sử dụng lâu dài. Git sẽ thường xuyên yêu cầu người dùng nhập thông tin xác thực, làm gián đoạn luồng công việc. Mặc dù các công cụ hỗ trợ quản lý thông tin đăng nhập (credential helpers) có thể lưu trữ token, nhưng chúng lại đặt ra một vấn đề khác về mức độ an toàn của việc lưu trữ này. Quan trọng hơn, một PAT bị rò rỉ có thể cấp cho kẻ tấn công quyền truy cập không chỉ vào các kho lưu trữ mà còn có thể vào toàn bộ tài khoản GitHub, tùy thuộc vào phạm vi quyền hạn được cấp cho token đó.

### So Sánh Nhanh: HTTPS và SSH trên GitHub

Để tóm tắt những khác biệt chính, bảng dưới đây cung cấp một cái nhìn tổng quan về hai phương thức xác thực.

| Tiêu chí              | HTTPS (với Personal Access Token)                             | SSH                                                            |
| --------------------- | ------------------------------------------------------------- | -------------------------------------------------------------- |
| **Cơ chế Xác thực**   | Dựa trên token (hoạt động như mật khẩu) 1                     | Cặp khóa Public/Private (mật mã bất đối xứng) 1                |
| **Mức độ Bảo mật**    | Dễ bị lộ nếu token không được bảo vệ cẩn thận 3               | Rất cao; khóa riêng tư không bao giờ truyền qua mạng 4         |
| **Sự tiện lợi**       | Yêu cầu nhập lại token hoặc phụ thuộc vào credential helper 3 | Rất tiện lợi sau khi thiết lập, không cần nhập lại thông tin 8 |
| **Thiết lập ban đầu** | Đơn giản, chỉ cần tạo token 2                                 | Phức tạp hơn một chút, yêu cầu tạo và quản lý cặp khóa 2       |
| **Quản lý Truy cập**  | Phân quyền thông qua phạm vi của token trên GitHub 1          | Có thể quản lý truy cập chi tiết qua từng khóa riêng lẻ 1      |

