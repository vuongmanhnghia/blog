---
title: Labs Operating
date: 2025-08-23
draft: false
tags:
  - system
  - network
---
1 Số Labs từ Cơ bản tới Nâng cao về Operating
<!--more-->

## Tại sao Hệ Điều Hành Vẫn Quan Trọng trong Thế Giới Cloud-Native

Trong lĩnh vực DevOps hiện đại, tồn tại một nghịch lý: trong khi các công cụ cấp cao như Kubernetes, Docker và Ansible trừu tượng hóa hệ điều hành bên dưới, việc hiểu sâu về Linux lại trở nên quan trọng hơn bao giờ hết. Hầu hết các công cụ DevOps cốt lõi đều được xây dựng để chạy tốt nhất trên Linux, biến nó thành nền tảng phổ biến cho cơ sở hạ tầng đám mây và tự động hóa.

Hướng dẫn này được thiết kế để nâng tầm kỹ sư từ một người dùng đơn thuần các công cụ này trở thành một kiến trúc sư hiểu rõ hoạt động bên trong của chúng. Hệ điều hành Linux không nên được xem như một hệ thống cũ kỹ, mà là "API" nền tảng, phổ quát cho mọi hoạt động tự động hóa cơ sở hạ tầng. Tám bài lab dưới đây được cấu trúc như một hành trình có phương pháp, phản ánh quy trình xử lý sự cố trong thực tế, bắt đầu từ các kiểm tra hệ thống cơ bản, đi sâu dần vào phân tích hiệu năng, gỡ lỗi nâng cao và cuối cùng là các nguyên tắc cốt lõi của container hóa. Đây không chỉ là một bộ sưu tập các lệnh; nó là một mô hình tư duy về hệ thống.

## Lab 1: Điều Hướng và Quản Lý Hệ Thống Tệp

**Mục tiêu:** Xây dựng "trí nhớ cơ bắp" để điều hướng hệ thống tệp Linux và thực hiện các thao tác tệp thiết yếu. Đây là nền tảng để tìm kiếm log, quản lý tệp cấu hình và chuẩn bị các tạo phẩm ứng dụng cho việc triển khai.

### Các Khái Niệm Cốt Lõi

- **Triết lý "Mọi thứ đều là tệp":** Trong Linux, một nguyên tắc cốt lõi là mọi thứ, từ thiết bị phần cứng, socket mạng đến các thư mục, đều được biểu diễn dưới dạng tệp. Điều này cung cấp một giao diện thống nhất để tương tác với toàn bộ hệ thống.
    
- **Tiêu chuẩn Phân cấp Hệ thống tệp (FHS):** Cấu trúc thư mục trong Linux tuân theo một tiêu chuẩn, mang lại sự dễ đoán trong quản trị hệ thống. Các thư mục chính bao gồm `/etc` cho các tệp cấu hình, `/var/log` cho các tệp nhật ký, `/home` cho thư mục người dùng và `/usr` cho các tiện ích và ứng dụng hệ thống.
    

### Thực Hành (Từng bước)

1. **Bước 1: Xác định vị trí:** Sử dụng lệnh `pwd` để in ra thư mục làm việc hiện tại và `whoami` để xác định người dùng hiện tại.
    
2. **Bước 2: Khám phá xung quanh:** Sử dụng `ls` với các cờ phổ biến (`-l`, `-a`, `-h`) để liệt kê nội dung thư mục và hiểu định dạng đầu ra (quyền, chủ sở hữu, kích thước, ngày).
    
3. **Bước 3: Di chuyển:** Thực hành điều hướng bằng `cd`, sử dụng cả đường dẫn tuyệt đối (ví dụ: `cd /var/log`) và tương đối (ví dụ: `cd../..`).
    
4. **Bước 4: Tạo và Xóa:** Sử dụng `touch` để tạo các tệp trống, `mkdir` để tạo thư mục (và `-p` để tạo các thư mục cha), và `rm` để xóa tệp và thư mục (`-r` để xóa đệ quy).
    
5. **Bước 5: Thao tác với tệp:** Sử dụng `cp` để sao chép, `mv` để di chuyển/đổi tên, và `cat` để hiển thị nội dung tệp.
    

|Lệnh|Trường Hợp Sử Dụng Phổ Biến|
|---|---|
|`ls`|Liệt kê nội dung của một thư mục.|
|`cd`|Thay đổi thư mục làm việc hiện tại.|
|`pwd`|In ra đường dẫn đầy đủ của thư mục hiện tại.|
|`mkdir`|Tạo một thư mục mới.|
|`rm`|Xóa tệp hoặc thư mục.|
|`cp`|Sao chép tệp hoặc thư mục.|
|`mv`|Di chuyển hoặc đổi tên tệp hoặc thư mục.|
|`touch`|Tạo một tệp trống hoặc cập nhật dấu thời gian của tệp.|
|`cat`|Hiển thị nội dung của một tệp.|
|`head` / `tail`|Hiển thị phần đầu hoặc phần cuối của một tệp.|

## Lab 2: Quản Lý Người Dùng, Nhóm và Quyền Truy Cập

**Mục tiêu:** Bảo mật tài nguyên hệ thống bằng cách làm chủ quyền sở hữu tệp và các danh sách kiểm soát truy cập. Kỹ năng này có thể áp dụng trực tiếp vào việc bảo mật môi trường tác tử CI/CD, thiết lập quyền cho các tạo phẩm triển khai và cấu hình quyền truy cập của người dùng trên máy chủ.

### Các Khái Niệm Cốt Lõi

- **Bộ ba Bảo mật:** Mô hình quyền trong Linux dựa trên ba thực thể: `user` (người dùng, chủ sở hữu), `group` (nhóm), và `other` (những người khác).
    
- **Giải mã Quyền:** Mỗi thực thể có thể được cấp ba loại quyền cơ bản: `read (r)` (đọc), `write (w)` (ghi), và `execute (x)` (thực thi). Ý nghĩa của các quyền này khác nhau giữa tệp và thư mục. Ví dụ, quyền `execute` trên một thư mục cho phép người dùng `cd` vào thư mục đó, trong khi trên một tệp, nó cho phép chạy tệp đó như một chương trình.
    

### Thực Hành (Từng bước)

1. **Bước 1: Quản trị Người dùng và Nhóm:** Tạo một người dùng mới với `useradd`, đặt mật khẩu với `passwd`, và tạo một nhóm mới với `groupadd`. Thêm người dùng vào nhóm vừa tạo.
    
2. **Bước 2: Thay đổi Quyền sở hữu:** Sử dụng `chown` để thay đổi chủ sở hữu của một tệp và `chgrp` (hoặc `chown user:group`) để thay đổi nhóm sở hữu. Luôn sử dụng
    
    `sudo` cho các hoạt động này khi cần thiết.
    
1. **Bước 3: Sửa đổi Quyền bằng Ký hiệu Tượng trưng:** Sử dụng `chmod` với ký hiệu tượng trưng (`u+x`, `g-w`, `o=r`) để thay đổi quyền một cách chi tiết và dễ đọc.
    
2. **Bước 4: Sửa đổi Quyền bằng Ký hiệu Bát phân (Số):** Giới thiệu các giá trị số (r=4, w=2, x=1) và trình bày cách thiết lập các quyền phổ biến như `chmod 755` cho các tập lệnh và `chmod 644` cho các tệp web.
    

|Giá trị Bát phân|Ký hiệu Tượng trưng|Trường Hợp Sử Dụng Phổ Biến|
|---|---|---|
|`777`|`rwxrwxrwx`|Không an toàn, chỉ dùng cho mục đích tạm thời hoặc trong môi trường được kiểm soát chặt chẽ.|
|`755`|`rwxr-xr-x`|Các tập lệnh thực thi, các thư mục cần người khác truy cập.|
|`644`|`rw-r--r--`|Các tệp nội dung web, tệp cấu hình chỉ đọc cho người khác.|
|`600`|`rw-------`|Các tệp nhạy cảm như khóa riêng SSH, chỉ chủ sở hữu mới có thể đọc/ghi.|

## Lab 3: Quản Lý Tiến Trình và Giám Sát Thời Gian Thực

**Mục tiêu:** Học cách xem những gì đang chạy trên hệ thống, diễn giải việc sử dụng tài nguyên và quản lý các tiến trình hoạt động sai. Đây là tuyến phòng thủ đầu tiên khi khắc phục sự cố một ứng dụng chạy chậm hoặc không phản hồi, ngay cả bên trong một container.

### Các Khái Niệm Cốt Lõi

- **Vòng đời Tiến trình:** Một tiến trình là một thực thể của một chương trình đang chạy. Mỗi tiến trình có một Mã định danh Tiến trình (PID) duy nhất và có thể ở các trạng thái khác nhau như đang chạy (running), đang ngủ (sleeping), hoặc zombie (xác sống).
    

### Thực Hành (Từng bước)

1. **Bước 1: Liệt kê Tiến trình Tĩnh:** Sử dụng `ps aux` để có một ảnh chụp nhanh chi tiết về tất cả các tiến trình đang chạy. Phân tích các cột chính: `USER`, `PID`, `%CPU`, `%MEM`, `COMMAND`.
    
2. **Bước 2: Giám sát Thời gian thực với `top`:** Khởi chạy `top` và giải thích khu vực tóm tắt (tải trung bình, tác vụ, trạng thái CPU, bộ nhớ) và danh sách tiến trình tương tác. Trình bày cách sắp xếp theo bộ nhớ (`M`) và CPU (`P`).
    
3. **Bước 3: Giám sát Nâng cao với `htop`:** Giới thiệu `htop` như một giải pháp thay thế thân thiện và tương tác hơn cho `top`. Hướng dẫn người dùng qua các tính năng chính của nó: hiển thị mã màu, cuộn dễ dàng, chế độ xem cây (`F5`), tìm kiếm (`F3`), và sắp xếp (`F6`).
    
4. **Bước 4: Chấm dứt Tiến trình:** Sử dụng lệnh `kill` với PID để gửi tín hiệu. Giải thích sự khác biệt giữa `SIGTERM` (chấm dứt nhẹ nhàng, `kill <PID>`) và `SIGKILL` (chấm dứt cưỡng bức, `kill -9 <PID>`). Trình bày cách chấm dứt một tiến trình trực tiếp từ `htop` (`F9`).
    

Các kỹ năng trong bài lab này không chỉ dành cho các máy chủ truyền thống; chúng là những công cụ chính để gỡ lỗi bên trong một container đang chạy. Khi một container sử dụng quá nhiều CPU hoặc bộ nhớ, quy trình chẩn đoán tiêu chuẩn là `docker exec -it <container_id> bash` theo sau là `htop` hoặc `ps aux`. Kubernetes hoặc Docker có thể cho biết _rằng_ một container không khỏe mạnh, nhưng để tìm ra _lý do tại sao_, cần phải kiểm tra không gian tiến trình bị cô lập bên trong nó bằng chính các công cụ đã học.

## Lab 4: Phân Tích Hiệu Năng Bộ Nhớ và I/O Đĩa

**Mục tiêu:** Vượt ra ngoài việc giám sát CPU để chẩn đoán hai trong số những nút thắt hiệu năng phổ biến nhất: áp lực bộ nhớ và I/O đĩa chậm.

### Các Khái Niệm Cốt Lõi

- **Mô hình Bộ nhớ Linux:** Giải thích sự khác biệt giữa bộ nhớ `used` (đã sử dụng) và `available` (khả dụng), nhấn mạnh vai trò của `buff/cache`. Giải mã lý do tại sao "bộ nhớ trống thấp" thường là bình thường trong Linux. Giới thiệu về Bộ nhớ ảo, Hoán đổi (Swapping) và nguy cơ của Trình tiêu diệt Hết bộ nhớ (OOM Killer).
    
- **Các Chỉ số I/O Đĩa:** Xác định các chỉ số hiệu năng chính (KPI): IOPS (số thao tác mỗi giây), Thông lượng (MB/s), và Độ trễ/`await` (thời gian cho mỗi thao tác).
    

### Thực Hành (Từng bước)

1. **Bước 1: Phân tích Sử dụng Bộ nhớ:** Sử dụng `free -h` để có cái nhìn tổng quan dễ đọc về việc sử dụng RAM và swap. Giải thích từng cột (`total`, `used`, `free`, `buff/cache`, `available`).
    
2. **Bước 2: Giám sát I/O Đĩa với `iostat`:** Chạy `iostat -x 1` để có cái nhìn thời gian thực, mở rộng về các thống kê đĩa. Tập trung vào việc diễn giải các cột quan trọng nhất: `r/s`, `w/s` (IOPS), `rMB/s`, `wMB/s` (Thông lượng), `await` (Độ trễ), và `%util` (Độ bão hòa).
    
3. **Bước 3: Xác định các Tiến trình Gây Tải I/O nặng với `iotop`:** Sử dụng `sudo iotop` để xem một giao diện giống `top` của các tiến trình được xếp hạng theo I/O đĩa hiện tại của chúng. Điều này trả lời trực tiếp câu hỏi, "Tiến trình nào đang làm quá tải đĩa?".
    

Các chỉ số thu thập được trong bài lab này không phải là những con số tùy ý; chúng là dữ liệu thô cung cấp cho các khuôn khổ độ tin cậy cấp cao hơn như "Bốn Tín hiệu Vàng" của SRE của Google (Độ trễ, Lưu lượng, Lỗi, Độ bão hòa). Việc học cách đo lường chúng tại nguồn là một bước tiến từ quản trị hệ thống đơn thuần sang kỹ thuật đảm bảo độ tin cậy. Ví dụ, cột

`await` trong `iostat` là một thước đo trực tiếp về **Độ trễ** I/O đĩa. Các cột IOPS và thông lượng là thước đo trực tiếp về **Lưu lượng** đĩa. Cột `%util` trong `iostat` và `%iowait` từ `top` là các chỉ số trực tiếp về **Độ bão hòa** của đĩa và CPU. Bằng cách hiểu mối liên hệ này, ta có thể chẩn đoán các vấn đề hiệu năng với một tư duy chiến lược, tập trung vào các chỉ số thực sự quan trọng đối với sức khỏe của dịch vụ.

## Lab 5: Các Lệnh Mạng và Xử Lý Sự Cố Thiết Yếu

**Mục tiêu:** Xây dựng một bộ công cụ mạnh mẽ để chẩn đoán các vấn đề mạng, từ kiểm tra kết nối cơ bản đến kiểm tra các kết nối đang hoạt động và các vấn đề DNS—một công việc hàng ngày trong môi trường microservices.

### Các Khái Niệm Cốt Lõi

Các khái niệm cơ bản về mạng bao gồm giao diện mạng, địa chỉ IP, cổng và socket, là những thành phần nền tảng cho mọi giao tiếp trên mạng.

### Thực Hành (Từng bước)

- **Bước 1: Kiểm tra Cấu hình Cục bộ:** Sử dụng `ip addr` (thay thế hiện đại cho `ifconfig`) để xem các giao diện mạng và địa chỉ IP của chúng.
    
- **Bước 2: Kiểm tra Kết nối Cơ bản:** Sử dụng `ping` để kiểm tra khả năng tiếp cận và độ trễ, và `traceroute` để vạch ra đường đi của gói tin mạng đến một đích.
    
- **Bước 3: Xử lý Sự cố DNS:** Sử dụng `dig` và `host` để truy vấn các bản ghi DNS (A, CNAME, MX) và thực hiện tra cứu ngược. Điều này rất quan trọng để gỡ lỗi các vấn đề phát hiện dịch vụ (service discovery).
    
- **Bước 4: Kiểm tra các Kết nối Đang hoạt động:** Giới thiệu `ss` là công cụ thay thế hiện đại, nhanh hơn cho `netstat`. Sử dụng
    
    `ss -tulpn` để tìm các cổng đang lắng nghe và các tiến trình sử dụng chúng. Đây là chìa khóa để trả lời "Ứng dụng của tôi có đang lắng nghe trên đúng cổng không?" và "Cái gì đang kết nối với dịch vụ của tôi?".
    
- **Bước 5: Tương tác với Dịch vụ Web:** Sử dụng `curl` để thực hiện các yêu cầu HTTP, xem các tiêu đề phản hồi (`-I`), và nhận chi tiết kết nối đầy đủ (`-v`), rất cần thiết để kiểm tra API và máy chủ web.
    

|Lệnh `netstat` Cũ|Lệnh `ss` Hiện Đại|Mục Đích|
|---|---|---|
|`netstat -tulpn`|`ss -tulpn`|Liệt kê tất cả các cổng TCP/UDP đang lắng nghe và các tiến trình liên quan.|
|`netstat -tan`|`ss -tan`|Hiển thị tất cả các kết nối TCP (cả đang lắng nghe và đã thiết lập).|
|`netstat -tun`|`ss -tun`|Hiển thị tất cả các kết nối TCP và UDP.|

## Lab 6: Thám Tử - Xử Lý Sự Cố Nâng Cao với `strace`

**Mục tiêu:** Học cách sử dụng `strace` như công cụ gỡ lỗi tối thượng để xem chính xác một ứng dụng đang làm gì ở cấp độ lời gọi hệ thống, khi mà log và giám sát không đủ thông tin.

### Các Khái Niệm Cốt Lõi

- **Ranh giới Kernel-Userspace:** Lời gọi hệ thống (`syscalls`) là giao diện mà qua đó các ứng dụng yêu cầu dịch vụ từ nhân Linux (ví dụ: mở một tệp, gửi dữ liệu mạng). `strace` chặn và giải mã các lời gọi này, cung cấp một cái nhìn không bị che giấu về hoạt động của chương trình.
    

### Thực Hành (Từng bước)

- **Bước 1: Truy vết Cơ bản:** Chạy một lệnh đơn giản dưới `strace` (ví dụ: `strace ls`) để xem luồng đầu ra và hiểu định dạng của nó.
    
- **Bước 2: Gắn vào một Tiến trình Đang chạy:** Tìm PID của một tiến trình đang chạy (sử dụng `ps` hoặc `htop` từ Lab 3) và gắn vào nó với `strace -p <PID>`.
    
- **Bước 3: Lọc Nhiễu:** Sức mạnh thực sự của `strace` nằm ở khả năng lọc. Trình bày cách truy vết các syscall cụ thể với `-e`:
    
    - **Sự cố Truy cập Tệp:** Sử dụng `strace -e trace=file <command>` để gỡ lỗi các lỗi "Permission denied" hoặc "No such file or directory" bằng cách xem chính xác đường dẫn tệp nào đang bị lỗi.
        
    - **Sự cố Mạng:** Sử dụng `strace -e trace=network <command>` để xem các lời gọi `connect`, `sendto`, `recvfrom`, giúp gỡ lỗi các kết nối mạng chậm hoặc thất bại.
        
- **Bước 4: Phân tích Hiệu năng:** Giới thiệu cờ `-T` để hiển thị thời gian đã dành cho mỗi syscall, giúp xác định các nút thắt hiệu năng nơi ứng dụng đang chờ một thao tác I/O chậm.
    

Log ứng dụng, các chỉ số và tài liệu mô tả những gì một chương trình _nên_ làm. `strace` tiết lộ những gì nó _thực sự_ đang làm. Nó là nguồn sự thật tối thượng để gỡ lỗi, bỏ qua tất cả các lớp trừu tượng ở cấp độ ứng dụng. Khi các công cụ khác cung cấp thông tin sai lệch hoặc im lặng, `strace` cung cấp một bản ghi khách quan, không bị lọc về ý định của chương trình, biến nó thành một kỹ năng quan trọng để giải quyết những lỗi "không thể".

## Lab 7: Các Thành Phần Xây Dựng Container: Namespaces

**Mục tiêu:** Giải mã công nghệ container bằng cách trình bày thực tế cách các namespace của Linux tạo ra môi trường bị cô lập cho các tiến trình, mạng và hệ thống tệp.

### Các Khái Niệm Cốt Lõi

- **Namespaces là gì?** Namespaces là một tính năng của nhân Linux giúp phân vùng các tài nguyên hệ thống toàn cục sao cho một tiến trình bên trong một namespace nghĩ rằng nó có một phiên bản riêng của tài nguyên đó (ví dụ: cây tiến trình riêng, ngăn xếp mạng riêng). Đây là cốt lõi của sự cô lập container.
    
- **Các loại Namespaces:** Các loại namespace chính bao gồm PID (Process ID), Net (Network), MNT (Mount), UTS (Hostname), và User. Bài lab này sẽ tập trung vào namespace Mạng (`net`) như một ví dụ trực quan nhất.
    

### Thực Hành (Từng bước)

- **Bước 1: Tạo Network Namespaces:** Sử dụng `ip netns add <name>` để tạo hai namespace mạng riêng biệt (ví dụ: `ns1`, `ns2`).
    
- **Bước 2: Xác minh Sự cô lập:** Chạy `ip netns exec <name> ip addr` để cho thấy mỗi namespace chỉ có giao diện `lo` riêng của nó và đang ở trạng thái `DOWN`.
    
- **Bước 3: Tạo một "Cáp Mạng Ảo":** Sử dụng `ip link add veth-ns1 type veth peer name veth-ns2` để tạo một cặp ethernet ảo (một "dây cáp mạng" ảo).
    
- **Bước 4: Kết nối các Namespaces:** "Cắm" mỗi đầu của cáp ảo vào một namespace bằng cách sử dụng `ip link set <veth-device> netns <name>`.
    
- **Bước 5: Cấu hình Mạng bị cô lập:** Bên trong mỗi namespace, gán một địa chỉ IP cho giao diện veth (`ip netns exec <name> ip addr add...`) và bật giao diện lên (`ip netns exec <name> ip link set... up`).
    
- **Bước 6: Kiểm tra Giao tiếp:** Sử dụng `ip netns exec ns1 ping <ns2_ip>` để cho thấy hai môi trường bị cô lập giờ đây có thể giao tiếp với nhau qua mạng riêng của chúng, nhưng vẫn vô hình đối với máy chủ chủ (host).
    

## Lab 8: Người Quản Lý - Quản Lý Tài Nguyên với Control Groups (cgroups)

**Mục tiêu:** Bổ sung cho sự cô lập từ Lab 7, bài lab này trình bày cách sử dụng cgroups để giới hạn tài nguyên (CPU, bộ nhớ) mà một tiến trình có thể tiêu thụ, hoàn thiện bức tranh về container hóa.

### Các Khái Niệm Cốt Lõi

- **cgroups là gì?** cgroups (control groups) là một tính năng của nhân Linux để giới hạn, tính toán và ưu tiên việc sử dụng tài nguyên cho một tập hợp các tiến trình. Trong khi namespaces cung cấp
    
    _sự cô lập_ ("những gì bạn có thể thấy"), cgroups cung cấp _sự giới hạn_ ("những gì bạn có thể sử dụng").
    
- **Controllers/Subsystems:** cgroups được quản lý thông qua các hệ thống con như `memory`, `cpu`, và `blkio`, mỗi hệ thống con kiểm soát một tài nguyên cụ thể.
    

### Thực Hành (Từng bước)

- **Bước 1: Tạo một cgroup:** Sử dụng `cgcreate -g memory,cpu:/my-app-group` để tạo một cgroup mới được quản lý bởi các controller bộ nhớ và CPU. Hoặc, có thể tạo thư mục thủ công trong hệ thống tệp ảo
    
    `/sys/fs/cgroup/`.
    
- **Bước 2: Đặt Giới hạn Bộ nhớ:** Sử dụng `echo "100M" > /sys/fs/cgroup/memory/my-app-group/memory.limit_in_bytes` để đặt giới hạn bộ nhớ 100MB.
    
- **Bước 3: Đặt Giới hạn CPU:** Trình bày cách đặt hạn ngạch CPU. Ví dụ, `echo 50000 >.../cpu.cfs_quota_us` và `echo 100000 >.../cpu.cfs_period_us` để giới hạn tiến trình ở mức 50% của một lõi CPU.
    
- **Bước 4: Chạy một Tiến trình trong cgroup:** Sử dụng `cgexec -g memory,cpu:/my-app-group <command>` để chạy một tiến trình trong các giới hạn này.
    
- **Bước 5: Quan sát Giới hạn:** Giám sát tiến trình bằng `htop` và xem nó bị điều tiết (CPU) hoặc bị OOM killer chấm dứt khi vượt quá giới hạn bộ nhớ. Kiểm tra các tệp kế toán của cgroup (`memory.usage_in_bytes`, `memory.failcnt`) để thấy việc thực thi giới hạn trong thực tế.
    

Các bài lab 7 và 8 không chỉ là các bài tập lý thuyết; chúng là một minh chứng thực tế về những gì Kubernetes làm "dưới mui xe" mỗi khi nó lập lịch cho một Pod. Sự cô lập mạng của một Pod là một network namespace. Dòng `resources: { limits: { memory: "100Mi" } }` trong tệp YAML của Pod được dịch trực tiếp thành một cấu hình cgroup trên node. Do đó, việc gỡ lỗi một Pod bị OOMKilled trong Kubernetes về cơ bản là việc hiểu sự tương tác giữa ứng dụng và giới hạn bộ nhớ cgroup do Kubelet áp đặt. Hướng dẫn này kết nối tệp YAML trừu tượng của Kubernetes với các tính năng cụ thể của nhân Linux, trao quyền cho kỹ sư để suy luận về hành vi của container từ các nguyên tắc cơ bản, giúp họ trở thành một người vận hành và xử lý sự cố Kubernetes hiệu quả hơn nhiều.

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*