---
title: Kĩ thuật chuẩn đoán lỗi khi SSH tới server
date: 2025-09-26
image: /image-placeholder.png
categories:
  - experience
  - log
  - server
tags:
  - ssh
draft: false
---

Chia sẻ một số kĩ thuật chuẩn đoán lỗi khi kết nối (SSH) tới server (Mạng nội bộ)

<!--more-->

---
# GIẢ SỬ SERVER LÀ RASPBERRY PI
## 1. Chế độ Verbose của SSH 

Đây là công cụ chẩn đoán mạnh mẽ và hữu ích nhất có sẵn. Nó yêu cầu client SSH in ra tất cả các bước và thông tin trao đổi trong quá trình kết nối.

### **Cách thực hiện:**

Thêm cờ `-v` (verbose) vào lệnh SSH của bạn. Sử dụng `-vvv` để có mức độ chi tiết cao nhất.

```bash
ssh -vvv nagih@192.168.0.102
```

### **Phân tích kết quả:**

Bạn sẽ thấy một loạt các dòng gỡ lỗi (debug). Hãy chú ý đến những dòng cuối cùng trước khi kết nối thất bại.

- **Dừng ở `Connecting to 192.168.0.102 port 22`:** Máy tính của bạn không thể tìm thấy Pi trên mạng. Nguyên nhân có thể là **sai địa chỉ IP**, Pi **chưa khởi động xong**, hoặc bị **tường lửa mạng chặn**.
    
- **Dừng ở `Connection established` rồi báo lỗi:** Kết nối mạng đã thành công, nhưng dịch vụ SSH trên Pi đã từ chối. Đây là dấu hiệu của lỗi cấu hình SSH trên Pi (như `hosts.deny`) hoặc dịch vụ SSH không chạy đúng. Lỗi "Connection closed by..." thường xuất hiện ở giai đoạn này.
    
- **Dừng ở các bước xác thực (`Authenticating`)**: Vấn đề nằm ở mật khẩu hoặc khóa SSH.

## 2. Kiểm tra Kết nối Mạng cơ bản (`ping`) 🌐

Lệnh `ping` giúp xác nhận xem Raspberry Pi có đang "sống" và phản hồi trên mạng hay không.

### **Cách thực hiện:**

```bash
ping 192.168.0.102
```

### **Cách phân tích kết quả:**

- **Nhận được phản hồi `Reply from...`**: Tốt! Raspberry Pi đang hoạt động và có thể truy cập được từ máy của bạn. Vấn đề chắc chắn nằm ở dịch vụ SSH (chưa bật, bị treo, hoặc bị tường lửa chặn).
    
- **Nhận được `Request timed out` hoặc `Destination host unreachable`**: Máy tính của bạn không thể "thấy" Pi. Nguyên nhân có thể là:
    
    - **Sai địa chỉ IP**.
        
    - Pi chưa được cắm nguồn hoặc chưa khởi động xong.
        
    - Pi không kết nối được vào mạng WiFi/LAN.
        
    - Bạn và Pi đang ở hai mạng khác nhau.
	
## 3. Quét Cổng Mạng (`nmap`) 🔍

`nmap` là một công cụ quét mạng mạnh mẽ giúp bạn kiểm tra xem cổng 22 (cổng SSH mặc định) trên Raspberry Pi có đang mở và lắng nghe kết nối hay không.

### **Cách thực hiện:**

Đầu tiên, bạn có thể cần cài đặt nmap. Sau đó, chạy lệnh sau:

```bash
nmap -p 22 192.168.0.102
```

### **Cách phân tích kết quả:**

- **`PORT 22/tcp OPEN`**: Cổng 22 đang mở. Điều này khẳng định dịch vụ SSH đang chạy trên Pi. Nếu bạn vẫn không kết nối được, nguyên nhân gần như chắc chắn là do cấu hình bảo mật trên Pi (như `hosts.deny` hoặc `AllowUsers`).
    
- **`PORT 22/tcp CLOSED`**: Cổng 22 đang bị đóng. Điều này có nghĩa là Pi đang hoạt động, nhưng dịch vụ SSH không chạy hoặc chưa được khởi động.
    
- **`PORT 22/tcp FILTERED`**: Cổng 22 đang bị một thiết bị tường lửa (trên Pi hoặc trên router mạng) chặn. Kết nối từ máy bạn bị lọc và không thể đến được dịch vụ SSH.
	
## 4. Kiểm tra Tệp `known_hosts` của Client

Đôi khi, nếu bạn cài đặt lại hệ điều hành trên Pi hoặc Pi được cấp lại IP của một thiết bị cũ, "dấu vân tay" SSH của nó sẽ thay đổi, gây ra lỗi bảo mật trên máy client.

### **Cách phát hiện:**

Lỗi thường sẽ có thông báo rất rõ ràng, chứa cảnh báo **"REMOTE HOST IDENTIFICATION HAS CHANGED!"**.

#### **Cách khắc phục:**

Chạy lệnh sau trên máy client để xóa thông tin cũ về địa chỉ IP đó:

```bash
ssh-keygen -R "192.168.0.102"
```

Sau đó, hãy thử kết nối lại. Bạn sẽ được hỏi để xác nhận dấu vân tay mới.

## Tóm tắt quy trình chẩn đoán từ Client

1. **Dùng `ping`** để xác nhận Pi có trên mạng không.
    
    - Không thấy? Kiểm tra IP, dây mạng/WiFi, nguồn điện của Pi.
        
2. **Dùng `nmap`** để kiểm tra cổng 22.
    
    - `CLOSED`? Dịch vụ SSH trên Pi chưa chạy.
        
    - `FILTERED`? Tường lửa đang chặn.
        
3. **Dùng `ssh -vvv`** để xem chi tiết quá trình kết nối.
    
    - Lỗi sẽ hiện ra trong các bước cuối cùng, giúp bạn biết vấn đề nằm ở mạng, cấu hình dịch vụ, hay xác thực.

---