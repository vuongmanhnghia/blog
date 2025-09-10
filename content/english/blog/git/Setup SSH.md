---
title: Hướng dẫn thiết lập khóa SSH cho github
date: 2025-09-10
image: /images/image-placeholder.png
categories:
  - protocol
  - git
author: Nagih
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

- **Ed25519 (Khuyến nghị):** Đây là thuật toán hiện đại, được khuyến nghị sử dụng. Ed25519 cung cấp mức độ bảo mật rất cao với độ dài khóa ngắn hơn, giúp quá trình xác thực diễn ra nhanh hơn.
    
    ```bash
    $ ssh-keygen -t ed25519 -C "your_email@example.com"
    ```
    
- **RSA (Lựa chọn thay thế):** RSA là một thuật toán cũ. Nếu bạn cần hỗ trợ các hệ thống cũ không tương thích với Ed25519. Tuy nhiên, điều cực kỳ quan trọng là phải sử dụng độ dài khóa đủ lớn. Mức khuyến nghị tối thiểu hiện nay là 4096 bits để đảm bảo an toàn.
    
    ```bash
    $ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
    ```
    

>Trong quá trình tạo khóa, bạn sẽ được nhắc nhập một "passphrase". Đây là một lớp bảo vệ cực kỳ quan trọng và **rất nên được sử dụng**. Passphrase này sẽ mã hóa file khóa riêng tư của bạn trên đĩa. Điều này có nghĩa là, ngay cả khi máy tính của bạn bị đánh cắp và kẻ tấn công có được file khóa riêng tư, họ cũng không thể sử dụng nó nếu không biết passphrase. Đây là tuyến phòng thủ cuối cùng để bảo vệ danh tính số của bạn.

#### Lưu khóa và Đặt tên file tùy chỉnh

Theo mặc định, `ssh-keygen` sẽ lưu cặp khóa vào thư mục `~/.ssh/` với tên file là `id_ed25519` và `id_ed25519.pub` (hoặc `id_rsa` cho RSA). Mặc dù bạn có thể chấp nhận giá trị mặc định. Đặc biệt khi bạn dự định quản lý nhiều khóa cho các tài khoản khác nhau. Ví dụ, bạn có thể đặt tên là

`~/.ssh/id_ed25519_personal` cho tài khoản cá nhân và `~/.ssh/id_ed25519_work` cho tài khoản công việc. Điều này sẽ giúp việc quản lý trở nên dễ dàng hơn ở các bước nâng cao.

### Bước 2: Quản Lý Khóa với `ssh-agent`

`ssh-agent` là một chương trình chạy nền có vai trò giữ các khóa riêng tư đã được giải mã trong bộ nhớ. Điều này cho phép bạn chỉ cần nhập passphrase một lần cho mỗi phiên làm việc, thay vì mỗi lần kết nối SSH.

- **Khởi động ssh-agent:**
    
    Chạy lệnh sau trong terminal để khởi động agent cho phiên làm việc hiện tại của bạn.
    
    ```bash
    $ eval "$(ssh-agent -s)"
    ```
    
- **Thêm khóa riêng tư vào ssh-agent:**
    
    Sử dụng lệnh ssh-add để thêm khóa riêng tư của bạn vào agent. Bạn sẽ được yêu cầu nhập passphrase mà bạn đã tạo ở Bước 1.
    
    ```bash
    $ ssh-add ~/.ssh/your_private_key_filename
    ```
    
### Bước 3: Thêm Khóa Công Khai (Public Key) vào Tài Khoản GitHub

Bước tiếp theo là thông báo cho GitHub về danh tính của bạn. Hãy nhớ rằng chỉ có file khóa công khai (có đuôi `.pub`) mới được chia sẻ.

- **Sao chép nội dung khóa công khai:**
    
    - **macOS:**
        
        ```bash
        $ pbcopy < ~/.ssh/id_ed25519_personal.pub
        ```
        
    - **Windows (sử dụng Git Bash hoặc WSL):**
        
        ```bash
        $ cat ~/.ssh/id_ed25519_personal.pub | clip
        ```
        
    
- **Thêm khóa vào GitHub:**
    
    - Truy cập tài khoản GitHub của bạn trên trình duyệt.
        
    - Vào **Settings** (Cài đặt)
        
    - Trong thanh bên trái, chọn **SSH and GPG keys** (Khóa SSH và GPG).
        
    - Nhấp vào nút **New SSH key** (Khóa SSH mới).
        
    - Trong trường **Title**, đặt một cái tên mang tính mô tả cho khóa của bạn (ví dụ: "MacBook Pro Cá Nhân").
        
    - Trong trường **Key**, dán nội dung khóa công khai bạn đã sao chép.
        
    - Nhấp vào Add SSH key (Thêm khóa SSH) để hoàn tất.
        

### Bước 4: Kiểm Tra Kết Nối

Sau khi hoàn tất các bước trên, bạn cần kiểm tra để đảm bảo mọi thứ hoạt động chính xác.

- Chạy lệnh kiểm tra:
    
    ```bash
    $ ssh -T git@github.com
    ```
    
- Xác thực máy chủ (lần đầu tiên):
    
    ```
    The authenticity of host 'github.com (IP_ADDRESS)' can't be established.
    ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
    Are you sure you want to continue connecting (yes/no)?
    ```
    
    Đây là một tính năng bảo mật của SSH để chống lại các cuộc tấn công xen giữa (man-in-the-middle). Sau khi xác nhận, gõ `yes` và nhấn Enter.
    
- Kết quả thành công:
    
    ```
    Hi username! You've successfully authenticated, but GitHub does not provide shell access.
    ```
    
    Điều này xác nhận rằng cặp khóa SSH của bạn đã được thiết lập chính xác và GitHub đã xác thực thành công danh tính của bạn.
    

## Phần 3: Nâng Cao Kỹ Năng với File Cấu Hình SSH (`~/.ssh/config`)

Đối với các nhà phát triển làm việc trên nhiều dự án hoặc có nhiều danh tính (ví dụ: tài khoản cá nhân và tài khoản công việc), việc quản lý nhiều khóa SSH có thể trở nên phức tạp. File cấu hình `~/.ssh/config` là một công cụ mạnh mẽ giúp tự động hóa và đơn giản hóa quá trình này, biến SSH từ một công cụ kết nối đơn thuần thành một hệ thống quản lý danh tính hiệu quả.

### Giới thiệu `~/.ssh/config`

File `~/.ssh/config` cho phép bạn tạo các bí danh (alias) và các quy tắc kết nối cụ thể cho từng máy chủ. Thay vì phải gõ các lệnh dài dòng với các tùy chọn phức tạp, bạn có thể định nghĩa tất cả trong file này. Cấu trúc của file bao gồm các khối `Host`, mỗi khối chứa các chỉ thị áp dụng cho host đó.

### Kịch bản: Quản lý nhiều tài khoản GitHub (Cá nhân & Công việc)

Đây là một kịch bản rất phổ biến. Mục tiêu là có thể làm việc trên các kho lưu trữ của cả hai tài khoản trên cùng một máy tính mà không cần phải thay đổi cấu hình thủ công mỗi lần chuyển đổi.

1. Tạo khóa SSH thứ hai:
    
    Thực hiện lại Bước 1 trong Phần 2 để tạo một cặp khóa mới dành riêng cho tài khoản công việc. Hãy chắc chắn đặt một tên file khác biệt, ví dụ: id_ed25519_work. Sau đó, thêm khóa công khai này vào tài khoản GitHub công việc của bạn.
    
2. Cấu hình ~/.ssh/config:
    
    Mở file ~/.ssh/config (nếu chưa có, hãy tạo nó) và thêm vào nội dung sau:
    
    ```
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
    
    

#### Phân tích sâu các chỉ thị

- `Host github.com-personal`: Đây là bí danh (alias) bạn sẽ sử dụng. Khi Git hoặc SSH thấy host này, nó sẽ áp dụng các quy tắc bên dưới.
    
- `HostName github.com`: Đây là tên máy chủ thực tế mà SSH sẽ kết nối đến.
    
- `User git`: GitHub yêu cầu tất cả các kết nối SSH sử dụng user `git`.
    
- `IdentityFile ~/.ssh/id_ed25519_personal`: Chỉ thị này yêu cầu SSH sử dụng file khóa riêng tư cụ thể này để xác thực.
    
- `IdentitiesOnly yes`: Đây là một chỉ thị cực kỳ quan trọng. Theo mặc định, SSH client có thể thử tất cả các khóa có sẵn trong `ssh-agent` hoặc các file mặc định. Khi kết nối đến GitHub, nếu gửi sai khóa, kết nối có thể bị từ chối sau vài lần thử. `IdentitiesOnly yes` buộc SSH client chỉ sử dụng duy nhất khóa được chỉ định trong `IdentityFile` cho host này, loại bỏ sự mơ hồ và ngăn ngừa lỗi xác thực.
    

### Áp dụng cấu hình vào Git

Sau khi đã cấu hình `~/.ssh/config`, bạn cần cập nhật URL của các kho lưu trữ Git để chúng sử dụng các bí danh mới.

- Đối với kho lưu trữ mới (khi git clone):
    
    Thay vì sử dụng URL SSH mặc định, hãy thay thế github.com bằng bí danh bạn đã tạo.
    
    Bash
    
    ```
    # Clone kho lưu trữ công việc
    $ git clone git@github.com-work:work-organization/project.git
    ```
    
    
- Đối với kho lưu trữ đã có:
    
    Sử dụng lệnh git remote set-url để cập nhật URL của remote origin.
    
    Bash
    
    ```
    # Điều hướng đến thư mục kho lưu trữ công việc của bạn
    $ cd path/to/work/project
    
    # Cập nhật URL của remote
    $ git remote set-url origin git@github.com-work:work-organization/project.git
    ```
    
    
    Bạn có thể kiểm tra lại bằng lệnh `git remote -v`.
    

Với thiết lập này, quy trình làm việc của bạn sẽ trở nên hoàn toàn tự động. Khi bạn ở trong một thư mục dự án công việc, các lệnh Git sẽ tự động sử dụng khóa công việc. Khi ở trong dự án cá nhân, chúng sẽ sử dụng khóa cá nhân. Điều này không chỉ là một mẹo tiện lợi, mà là một mô hình nền tảng để quản lý danh tính chuyên nghiệp, giúp ngăn chặn các lỗi như commit nhầm tài khoản và loại bỏ hoàn toàn các rào cản trong quy trình làm việc đa tài khoản.

## Phần 4: Xử Lý Sự Cố và Các Lỗi Thường Gặp

Ngay cả với một thiết lập cẩn thận, các vấn đề vẫn có thể phát sinh. Việc hiểu rõ cách chẩn đoán và khắc phục các lỗi SSH phổ biến là một kỹ năng quan trọng.

### Công cụ chẩn đoán chính: Chế độ Verbose

Trước khi thử bất kỳ giải pháp nào, bước đầu tiên luôn là thu thập thêm thông tin. Tùy chọn `-v` (verbose) của lệnh `ssh` sẽ in ra chi tiết quá trình kết nối, cho bạn biết file cấu hình nào đang được đọc, khóa nào đang được thử, và chính xác lỗi xảy ra ở đâu.

Bash

```
$ ssh -vT git@github.com
```

### Lỗi 1: `Permission denied (publickey)`

- **Ý nghĩa:** Đây là lỗi xác thực phổ biến nhất. Nó có nghĩa là máy chủ GitHub đã từ chối tất cả các khóa SSH mà client của bạn cung cấp.
    
- **Các bước kiểm tra và khắc phục:**
    
    1. **Kiểm tra khóa trên GitHub:** Đảm bảo rằng khóa công khai của bạn đã được thêm chính xác vào tài khoản GitHub. Quay lại Phần 2, Bước 3 để xác minh.
        
    2. **Kiểm tra `ssh-agent`:** Chạy `ssh-add -l` để xem các khóa hiện có trong agent. Nếu danh sách trống hoặc không chứa khóa bạn cần, hãy chạy lại `ssh-add ~/.ssh/your_private_key` để thêm nó vào.
        
    3. **Kiểm tra quyền truy cập file:** SSH yêu cầu quyền truy cập rất nghiêm ngặt. Thư mục `~/.ssh` phải có quyền là `700` (drwx−−−−−−), và file khóa riêng tư của bạn phải có quyền là `600` (−rw−−−−−−−). Sử dụng các lệnh sau để sửa:
        
        Bash
        
        ```
        $ chmod 700 ~/.ssh
        $ chmod 600 ~/.ssh/your_private_key
        ```
        
        
    4. **Kiểm tra `~/.ssh/config`:** Nếu bạn đang sử dụng file cấu hình, hãy kiểm tra kỹ lưỡng xem `Host` alias có khớp với URL remote của Git không, và `IdentityFile` có trỏ đến đúng file khóa riêng tư không.
        

### Lỗi 2: `Host key verification failed`

- **Ý nghĩa:** Dấu vân tay của máy chủ GitHub đã thay đổi so với lần cuối bạn kết nối. Đây là một cơ chế bảo mật quan trọng để cảnh báo về khả năng có một cuộc tấn công Man-in-the-Middle.42
    
- **Cách khắc phục an toàn:**
    
    1. **Không bao giờ** bỏ qua cảnh báo này một cách mù quáng.
        
    2. Truy cập trang tài liệu chính thức của GitHub để xác minh dấu vân tay máy chủ mới nhất của họ.
        
    3. Nếu dấu vân tay khớp, bạn có thể an toàn xóa khóa cũ khỏi file `~/.ssh/known_hosts` bằng lệnh:
        
        Bash
        
        ```
        $ ssh-keygen -R github.com
        ```
        
    
    Lần kết nối tiếp theo, bạn sẽ được yêu cầu chấp nhận khóa mới.
    

### Lỗi 3: `Agent admitted failure to sign using the key`

- **Ý nghĩa:** `ssh-agent` đang chạy nhưng không thể sử dụng khóa để tạo chữ ký số cần thiết cho việc xác thực. Lỗi này đôi khi xảy ra trên các hệ thống Linux.
    
- **Cách khắc phục:** Giải pháp thường rất đơn giản là tải lại khóa vào agent. Chạy lệnh `ssh-add` thường sẽ giải quyết được vấn đề này.
    

### Lỗi 4: `Key is already in use`

- **Ý nghĩa:** Bạn đang cố gắng thêm một khóa công khai vào tài khoản GitHub, nhưng khóa đó đã được sử dụng ở một nơi khác - hoặc trên một tài khoản người dùng khác, hoặc trong một kho lưu trữ khác dưới dạng "deploy key".
    
- **Nguyên tắc:** Một khóa SSH phải là định danh duy nhất cho một người dùng trên toàn bộ nền tảng GitHub. Khi được sử dụng làm deploy key, nó cũng phải là duy nhất cho mỗi kho lưu trữ.
    
- **Cách khắc phục:**
    
    1. Sử dụng lệnh sau để xác định tài khoản nào đang sử dụng khóa đó:
        
        Bash
        
        ```
        $ ssh -T -ai ~/.ssh/your_key git@github.com
        ```
        
        Phản hồi sẽ cho bạn biết khóa này đang được liên kết với `username` nào.
        
    2. Gỡ khóa khỏi tài khoản hoặc kho lưu trữ cũ, hoặc đơn giản là tạo một cặp khóa hoàn toàn mới cho mục đích sử dụng mới.
        

## Phần 5: Các Phương Pháp Bảo Mật Tốt Nhất (Best Practices) và Tổng Kết

Làm chủ SSH không chỉ dừng lại ở việc thiết lập thành công. Việc duy trì một tư thế bảo mật vững chắc đòi hỏi sự chú ý liên tục. Các phương pháp tốt nhất có thể được tóm gọn trong một vòng đời bảo mật của khóa SSH.

### Vòng Đời Bảo Mật Của Khóa SSH

- **Tạo (Creation):**
    
    - **Thuật toán mạnh:** Luôn ưu tiên sử dụng **Ed25519** vì hiệu suất và bảo mật vượt trội.
        
    - **Passphrase mạnh:** Luôn đặt một passphrase mạnh và duy nhất cho mỗi khóa. Sử dụng trình quản lý mật khẩu để lưu trữ an toàn các passphrase này.
        
- **Bảo vệ (Protection):**
    
    - **Quyền truy cập file:** Duy trì quyền truy cập file chính xác là điều bắt buộc: `chmod 700 ~/.ssh` và `chmod 600 ~/.ssh/private_key`.
        
    - **Bí mật tuyệt đối:** **Không bao giờ** chia sẻ, gửi qua email, hoặc lưu trữ khóa riêng tư của bạn ở bất kỳ đâu ngoài máy tính cá nhân đã được bảo vệ. Chỉ có khóa công khai là an toàn để chia sẻ.
        
- **Sử dụng (Usage):**
    
    - **Sử dụng `ssh-agent`:** Tận dụng `ssh-agent` để giảm thiểu số lần phải nhập passphrase, qua đó giảm nguy cơ bị keylogger ghi lại.
        
    - **Cấu hình timeout cho agent:** Để tăng cường bảo mật, hãy đặt thời gian tồn tại cho các khóa trong agent bằng tùy chọn `-t`. Lệnh `ssh-add -t 3600` sẽ yêu cầu agent "quên" khóa sau một giờ (3600 giây) không hoạt động. Điều này cực kỳ hữu ích để bảo vệ chống lại việc truy cập trái phép nếu máy tính của bạn bị bỏ lại mà không được khóa.
        
- **Bảo trì (Maintenance):**
    
    - **Kiểm tra định kỳ (Audit):** Lên lịch (ví dụ: hàng quý) để truy cập trang cài đặt SSH trên GitHub và xem lại danh sách các khóa đã được cấp quyền. Xóa ngay lập tức bất kỳ khóa nào bạn không nhận ra, không còn sử dụng, hoặc thuộc về các thiết bị đã mất.
        
    - **Xoay vòng khóa (Rotation):** Một thực hành bảo mật nâng cao là định kỳ tạo một cặp khóa mới và thay thế các khóa cũ. Việc này giới hạn "cửa sổ cơ hội" cho một kẻ tấn công nếu một khóa cũ bị xâm phạm mà bạn không hề hay biết.
        

### Tổng kết

Hành trình từ việc hiểu rõ giá trị của SSH đến việc thiết lập, quản lý chuyên nghiệp và xử lý sự cố là một quá trình đầu tư vào kỹ năng cốt lõi của một nhà phát triển phần mềm. Việc làm chủ SSH không chỉ là một biện pháp tăng cường bảo mật; đó là một tuyên bố về sự chuyên nghiệp, một cam kết về hiệu quả và là nền tảng cho một quy trình làm việc an toàn, liền mạch và năng suất hơn trên GitHub và xa hơn nữa. Bằng cách áp dụng các kiến thức và thực hành tốt nhất được trình bày trong báo cáo này, các nhà phát triển có thể tự tin tương tác với các hệ thống từ xa, biết rằng danh tính số và tài sản trí tuệ của họ được bảo vệ bởi một trong những tiêu chuẩn vàng của ngành công nghệ.

*Nếu thấy hay, hãy để lại cho mình xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*