---
title: Hướng dẫn quản lý nhiều khóa SSH trên 1 thiết bị
date: 2025-09-10
image: thumb/ssh
categories:
  - protocol
tags:
  - ssh
draft: false
---

biến SSH từ một công cụ kết nối đơn thuần thành một hệ thống quản lý danh tính hiệu quả

<!--more-->

---
## Giới thiệu `~/.ssh/config`

File `~/.ssh/config` cho phép bạn tạo các bí danh (alias) và các quy tắc kết nối cụ thể cho từng máy chủ. Thay vì phải gõ các lệnh dài dòng với các tùy chọn phức tạp, bạn có thể định nghĩa tất cả trong file này. Cấu trúc của file bao gồm các khối `Host`, mỗi khối chứa các chỉ thị áp dụng cho host đó.

## Kịch bản: Quản lý nhiều tài khoản GitHub (Cá nhân & Công việc)

Đây là một kịch bản rất phổ biến. Mục tiêu là có thể làm việc trên các kho lưu trữ của cả hai tài khoản trên cùng một máy tính mà không cần phải thay đổi cấu hình thủ công mỗi lần chuyển đổi.

1. **Tạo khóa SSH thứ hai:**

    Hãy chắc chắn rằng bạn đã tạo 1 cặp khóa mới dành cho công việc và đặt một tên file khác biệt, ví dụ: `id_ed25519_work`. Sau đó, thêm khóa công khai này vào tài khoản GitHub công việc.

2. **Cấu hình ~/.ssh/config:**

    Mở file ~/.ssh/config (nếu chưa có, hãy tạo nó) và thêm vào nội dung sau:

    ```bash
    # Tài khoản GitHub cá nhân
    Host github.com-personal
      HostName github.com
      User git
      IdentityFile ~/.ssh/id_ed25519_personal
      IdentitiesOnly yes

    # Tài khoản GitHub công việc
    Host github.com-work
      HostName github.com
      User git
      IdentityFile ~/.ssh/id_ed25519_work
      IdentitiesOnly yes
    ```

#### Phân tích

-   `Host github.com-personal`: Đây là bí danh (alias) bạn sẽ sử dụng. Khi Git hoặc SSH thấy host này, nó sẽ áp dụng các quy tắc bên dưới.
	
-   `HostName github.com`: Đây là tên máy chủ thực tế mà SSH sẽ kết nối đến.
	
-   `User git`: GitHub yêu cầu tất cả các kết nối SSH sử dụng user `git`.
	
-   `IdentityFile ~/.ssh/id_ed25519_personal`: Yêu cầu SSH sử dụng file khóa riêng tư cụ thể này để xác thực.
	
-   `IdentitiesOnly yes`: Cực kỳ quan trọng. Theo mặc định, SSH client có thể thử tất cả các khóa có sẵn trong `ssh-agent` hoặc các file mặc định. Khi kết nối đến GitHub, nếu gửi sai khóa, kết nối có thể bị từ chối sau vài lần thử. `IdentitiesOnly yes` buộc SSH client chỉ sử dụng duy nhất khóa được chỉ định trong `IdentityFile` cho host này, loại bỏ sự mơ hồ và ngăn ngừa lỗi xác thực.

### Áp dụng cấu hình vào Git

Sau khi đã cấu hình `~/.ssh/config`, bạn cần cập nhật URL của các kho lưu trữ Git để chúng sử dụng các bí danh mới.

-   Đối với kho lưu trữ mới (khi git clone):
    Thay vì sử dụng URL SSH mặc định, hãy thay thế github.com bằng bí danh bạn đã tạo.
    ```bash
    # Clone kho lưu trữ công việc
    $ git clone git@github.com-work:work-organization/project.git
    ```
-   Đối với kho lưu trữ đã có:
    Sử dụng lệnh git remote set-url để cập nhật URL của remote origin.

    ```bash
    # Điều hướng đến thư mục kho lưu trữ công việc của bạn
    $ cd path/to/work/project

    # Cập nhật URL của remote
    $ git remote set-url origin git@github.com-work:work-organization/project.git
    ```

    Bạn có thể kiểm tra lại bằng lệnh `git remote -v`.

Với thiết lập này, quy trình làm việc của bạn sẽ trở nên hoàn toàn tự động. Khi bạn ở trong một thư mục dự án công việc, các lệnh Git sẽ tự động sử dụng khóa công việc. Khi ở trong dự án cá nhân, chúng sẽ sử dụng khóa cá nhân.
