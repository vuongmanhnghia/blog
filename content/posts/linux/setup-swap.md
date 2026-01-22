---
title: Hướng dẫn setup Swap trên Linux
date: 2026-01-17
image:
categories:
  - linux
tags:
  - swap
draft: false
---

Để bật Swap (bộ nhớ ảo) cho Ubuntu, cách đơn giản và phổ biến nhất hiện nay là tạo một **Swap File** (tệp hoán đổi). Cách này linh hoạt hơn so với việc chia phân vùng ổ cứng (Swap Partition)

<!--more-->

---
### Bước 1: Kiểm tra Swap hiện có

Trước tiên, hãy kiểm tra xem hệ thống đã có swap chưa:

```bash
sudo swapon --show
```

Hoặc:

```bash
free -h
```

Nếu kết quả trống hoặc phần Swap hiển thị `0B`, nghĩa là chưa có swap.

### Bước 2: Tạo Swap File

Ví dụ này sẽ tạo một file Swap dung lượng **2GB** (bạn có thể thay `2G` bằng `1G`, `4G` tùy nhu cầu và dung lượng ổ cứng còn trống).

Chạy lệnh sau:

```bash
sudo fallocate -l 2G /swapfile
```

*Lưu ý: Nếu lệnh `fallocate` báo lỗi (hiếm gặp), bạn có thể dùng lệnh `sudo dd if=/dev/zero of=/swapfile bs=1024 count=2097152`.*

### Bước 3: Phân quyền cho file Swap

Vì lý do bảo mật, chỉ có tài khoản root mới được phép đọc/ghi file này.

```bash
sudo chmod 600 /swapfile
```

### Bước 4: Thiết lập file thành vùng Swap

Báo cho hệ thống biết file này sẽ được dùng làm bộ nhớ ảo:

```bash
sudo mkswap /swapfile
```

### Bước 5: Kích hoạt Swap

Bật swap lên:

```bash
sudo swapon /swapfile
```

Bây giờ hãy kiểm tra lại xem đã nhận chưa:

```bash
sudo swapon --show
```

### Bước 6: Giữ cấu hình vĩnh viễn (Quan trọng)

Nếu chỉ làm đến Bước 5, khi khởi động lại máy (Reboot), Swap sẽ bị tắt. Để tự động bật Swap mỗi khi khởi động, bạn cần thêm thông tin vào file `/etc/fstab`.

Cách an toàn nhất là chạy lệnh backup file cấu hình trước:

```bash
sudo cp /etc/fstab /etc/fstab.bak
```

Sau đó chạy lệnh này để thêm cấu hình swap vào cuối file:

```bash
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

### Bước 7: Tối ưu hóa Swap (Tùy chọn - Khuyên dùng)

Tham số `swappiness` quy định mức độ ưu tiên sử dụng Swap của hệ thống (từ 0 đến 100).

*   Mặc định là **60**: Hệ thống sẽ khá tích cực đẩy dữ liệu từ RAM sang Swap.
	
*   Nên chỉnh về **10**: Hệ thống sẽ cố gắng dùng hết RAM vật lý trước rồi mới dùng đến Swap (giúp máy chạy mượt hơn).

Kiểm tra chỉ số hiện tại:

```bash
cat /proc/sys/vm/swappiness
```


Để đổi thành 10, hãy sửa file cấu hình:

```bash
sudo nano /etc/sysctl.conf
```

Kéo xuống cuối file và thêm dòng này vào:

```text
vm.swappiness=10
```

Nhấn `Ctrl + O` (Enter) để lưu và `Ctrl + X` để thoát.

---

### Bonus: Cách xóa Swap (Nếu không muốn dùng nữa)

Nếu bạn muốn tắt và xóa file swap đi, hãy làm theo thứ tự:

1. Tắt swap: `sudo swapoff -v /swapfile`
	
2. Xóa dòng cấu hình trong `/etc/fstab` (dùng lệnh `sudo nano /etc/fstab` và xóa dòng `/swapfile...`).
	
3. Xóa file: `sudo rm /swapfile`
