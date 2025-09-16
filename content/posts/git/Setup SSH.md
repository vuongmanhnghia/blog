---
title: Hướng dẫn thiết lập khóa SSH cho github
date: 2025-09-10
image: /thumb/setup-ssh.png
categories:
    - protocol
    - git
tags:
    - ssh
draft: false
---

Chi tiết các bước thiết lập khóa SSH cho github từ A - Z

<!--more-->

Phần này sẽ hướng dẫn chi tiết từng bước để tạo và cấu hình khóa SSH cho tài khoản GitHub của bạn.

### Bước 1: Tạo Cặp Khóa SSH với `ssh-keygen`

CLI `ssh-keygen` được sử dụng để tạo ra cặp khóa công khai và riêng tư, là nền tảng của việc xác thực bằng SSH.

#### Lựa chọn Thuật toán Mã hóa

Việc lựa chọn thuật toán mã hóa là một quyết định quan trọng ảnh hưởng đến cả hiệu suất và bảo mật.

-   **Ed25519 (Khuyến nghị):** Đây là thuật toán hiện đại, được khuyến nghị sử dụng. Ed25519 cung cấp mức độ bảo mật rất cao với độ dài khóa ngắn hơn, giúp quá trình xác thực diễn ra nhanh hơn.
    ```bash
    $ ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
-   **RSA (Lựa chọn thay thế):** RSA là một thuật toán cũ. Nếu bạn cần hỗ trợ các hệ thống cũ không tương thích với Ed25519. Tuy nhiên, điều cực kỳ quan trọng là phải sử dụng độ dài khóa đủ lớn. Mức khuyến nghị tối thiểu hiện nay là 4096 bits để đảm bảo an toàn.
    ```bash
    $ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```

> Trong quá trình tạo khóa, bạn sẽ được nhắc nhập một "passphrase". Đây là một lớp bảo vệ cực kỳ quan trọng và **rất nên được sử dụng**. Passphrase này sẽ mã hóa file khóa riêng tư của bạn trên đĩa. Điều này có nghĩa là, ngay cả khi máy tính của bạn bị đánh cắp và kẻ tấn công có được file khóa riêng tư, họ cũng không thể sử dụng nó nếu không biết passphrase. Đây là tuyến phòng thủ cuối cùng để bảo vệ danh tính số của bạn.

#### Lưu khóa và Đặt tên file tùy chỉnh

Theo mặc định, `ssh-keygen` sẽ lưu cặp khóa vào thư mục `~/.ssh/` với tên file là `id_ed25519` và `id_ed25519.pub` (hoặc `id_rsa` cho RSA). Mặc dù bạn có thể chấp nhận giá trị mặc định. Đặc biệt khi bạn dự định quản lý nhiều khóa cho các tài khoản khác nhau. Ví dụ, bạn có thể đặt tên là

`~/.ssh/id_ed25519_personal` cho tài khoản cá nhân và `~/.ssh/id_ed25519_work` cho tài khoản công việc. Điều này sẽ giúp việc quản lý trở nên dễ dàng hơn ở các bước nâng cao.

### Bước 2: Quản Lý Khóa với `ssh-agent`

`ssh-agent` là một chương trình chạy nền có vai trò giữ các khóa riêng tư đã được giải mã trong bộ nhớ. Điều này cho phép bạn chỉ cần nhập passphrase một lần cho mỗi phiên làm việc, thay vì mỗi lần kết nối SSH.

-   **Khởi động ssh-agent:**
    Chạy lệnh sau trong terminal để khởi động agent cho phiên làm việc hiện tại của bạn.
    ```bash
    $ eval "$(ssh-agent -s)"
    ```
-   **Thêm khóa riêng tư vào ssh-agent:**
    Sử dụng lệnh ssh-add để thêm khóa riêng tư của bạn vào agent. Bạn sẽ được yêu cầu nhập passphrase mà bạn đã tạo ở Bước 1.
    ```bash
    $ ssh-add ~/.ssh/your_private_key_filename
    ```

### Bước 3: Thêm Khóa Công Khai (Public Key) vào Tài Khoản GitHub

Bước tiếp theo là thông báo cho GitHub về danh tính của bạn. Hãy nhớ rằng chỉ có file khóa công khai (có đuôi `.pub`) mới được chia sẻ.

-   **Sao chép nội dung khóa công khai:**
    -   **macOS:**
        ```bash
        $ pbcopy < ~/.ssh/id_ed25519_personal.pub
        ```
    -   **Windows (sử dụng Git Bash hoặc WSL):**
        ```bash
        $ cat ~/.ssh/id_ed25519_personal.pub | clip
        ```
-   **Thêm khóa vào GitHub:**
    -   Truy cập tài khoản GitHub của bạn trên trình duyệt.
    -   Vào **Settings** (Cài đặt)
    -   Trong thanh bên trái, chọn **SSH and GPG keys** (Khóa SSH và GPG).
    -   Nhấp vào nút **New SSH key** (Khóa SSH mới).
    -   Trong trường **Title**, đặt một cái tên mang tính mô tả cho khóa của bạn (ví dụ: "MacBook Pro Cá Nhân").
    -   Trong trường **Key**, dán nội dung khóa công khai bạn đã sao chép.
    -   Nhấp vào Add SSH key (Thêm khóa SSH) để hoàn tất.

### Bước 4: Kiểm Tra Kết Nối

Sau khi hoàn tất các bước trên, bạn cần kiểm tra để đảm bảo mọi thứ hoạt động chính xác.

-   Chạy lệnh kiểm tra:
    ```bash
    $ ssh -T git@github.com
    ```
-   Xác thực máy chủ (lần đầu tiên):
    ```bash
    The authenticity of host 'github.com (IP_ADDRESS)' can't be established.
    ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
    Are you sure you want to continue connecting (yes/no)?
    ```
    Đây là một tính năng bảo mật của SSH để chống lại các cuộc tấn công xen giữa (man-in-the-middle). Sau khi xác nhận, gõ `yes` và nhấn Enter.
-   Kết quả thành công:
    ```bash
    Hi username! You've successfully authenticated, but GitHub does not provide shell access.
    ```
    Điều này xác nhận rằng cặp khóa SSH của bạn đã được thiết lập chính xác và GitHub đã xác thực thành công danh tính của bạn.
