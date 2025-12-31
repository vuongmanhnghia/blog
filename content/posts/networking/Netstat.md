---
title: Netstat - Công cụ giám sát Networking
date: 2025-11-30
image:
categories:
  - network
  - internet
  - tool
tags:
  - netstat
draft: false
---
**Netstat** là công cụ dòng lệnh dùng để hiển thị chi tiết các kết nối mạng (TCP/UDP), bảng định tuyến và các cổng đang lắng nghe, giúp quản trị viên giám sát và xử lý sự cố hệ thống.

<!--more-->

---

### 1. Tư duy cốt lõi: Tại sao cần Netstat?

Khi một ứng dụng bị lỗi kết nối, DevOps Engineer sẽ đặt ra các câu hỏi sau và `netstat` là công cụ trả lời:
	
*   **Availability:** Port của service có đang mở (Listening) không?
	
*   **Binding:** Service đang lắng nghe trên IP nào? (Localhost `127.0.0.1` hay Public `0.0.0.0`)?
	
*   **Process Mapping:** Process nào (PID) đang chiếm dụng port đó?
	
*   **Performance:** Có bao nhiêu kết nối đang ở trạng thái chờ (TIME_WAIT, CLOSE_WAIT)?
	
*   **Security:** Có IP lạ nào đang kết nối vào server không?

---

### 2. "Vũ khí" thường dùng: Các Flag quan trọng

**Combo: `netstat -tulpn`**

Đây là lệnh đầu tiên tôi gõ khi debug network.

*   `-t` (TCP): Chỉ hiện các kết nối TCP.
	
*   `-u` (UDP): Chỉ hiện các kết nối UDP.
	
*   `-l` (Listening): Chỉ hiện các socket đang lắng nghe (Server mode).
	
*   `-p` (Process): Hiển thị PID và tên chương trình (Cần quyền `sudo`).
	
*   `-n` (Numeric): **Rất quan trọng**. Hiển thị IP và Port bằng số thay vì phân giải tên miền (DNS resolution). Nếu không có `-n`, lệnh sẽ chạy rất chậm khi DNS server gặp vấn đề.

**Ví dụ output:**

```bash
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1234/nginx
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      5678/mysqld
```

*   **Phân tích:**
	
	* **Nginx** đang mở port 80 cho tất cả IP (`0.0.0.0`)
		
	* **MySQL** chỉ cho phép kết nối từ nội bộ (`127.0.0.1`). Đây là một check-point về bảo mật.

---

### 3. Phân tích sâu về TCP States (Quan trọng cho Performance)

Cần đặc biệt chú ý đến cột **State**. Nó phản ánh sức khỏe của ứng dụng.

**a. `ESTABLISHED`**

Kết nối đang hoạt động bình thường.

*   **Use case:** Đếm số lượng user đang online (concurrent connections).

    ```bash
    netstat -anp | grep :80 | grep ESTABLISHED | wc -l
    ```

- `-a` (All):
	
	- Tất cả các socket, bao gồm cả các socket đang lắng nghe (Listening) và các socket đã thiết lập kết nối.
		
	- Nếu không có cờ này, mặc định netstat thường chỉ hiện các kết nối đã thiết lập.
    
- `-n` (Numeric): Đã giải thích ở trên
    
- `-p` (Program):
	
	- Hiển thị **PID** (Process ID) và **tên chương trình** đang sở hữu kết nối đó (ví dụ: 1234/nginx)
		
	- Cần `root` hoặc `sudo` để thấy PID của các process không thuộc user hiện tại 

- `wc -l`:  Công cụ đếm
    
    - `-l` (Lines Flag này bảo wc chỉ đếm **số dòng**.
        
    - -> Kết quả cuối cùng trả về một con số duy nhất (Ví dụ: 50 nghĩa là có 50 người đang kết nối vào web server).
	
**b. `TIME_WAIT`**

Kết nối đã đóng, nhưng kernel giữ lại socket một lúc để đảm bảo các gói tin lạc đường được xử lý xong.
	
*   **Vấn đề:** Nếu server có quá nhiều `TIME_WAIT` (hàng nghìn), server có thể bị cạn kiệt **Ephemeral Ports** (hết port để mở kết nối mới).
	
*   **Giải pháp:** Tinh chỉnh sysctl (`net.ipv4.tcp_tw_reuse`, `net.ipv4.tcp_fin_timeout`).

**c. `CLOSE_WAIT`**

Đây là trạng thái nguy hiểm nhất.
	
*   **Ý nghĩa:** Phía bên kia đã đóng kết nối, nhưng ứng dụng trên server của bạn **chưa** đóng socket.
	
*   **Nguyên nhân:** Thường là do **bug trong code** (quên `socket.close()`) hoặc ứng dụng bị treo/deadlock.
	
*   **Hành động:** Báo ngay cho team Dev hoặc restart service để giải phóng tài nguyên.
	
**d. `SYN_SENT`**

Server gửi yêu cầu kết nối nhưng không nhận được phản hồi.
	
*   **Nguyên nhân:** Thường do Firewall chặn hoặc IP đích không tồn tại.

---

### 4. Netstat trong Security & Audit (Bảo mật)

**a. Phát hiện DDoS hoặc Traffic bất thường**

Bạn muốn biết IP nào đang kết nối nhiều nhất vào server?

```bash
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -10
```

*   Lệnh này sẽ liệt kê Top 10 IP đang kết nối.

**b. Kiểm tra Backdoor/Malware**

Nếu thấy một port lạ mở (ví dụ: 4444, 6666) và process name lạ hoặc không có tên:

```bash
netstat -tulpn
```

Kiểm tra PID đó là gì: `ps -ef | grep <PID>`.

---

### 5. Routing và Interface Statistics

Ngoài socket, `netstat` còn dùng để check tầng mạng thấp hơn.

**a. Routing Table (`netstat -r` hoặc `netstat -rn`)**

Tương đương lệnh `route -n` hoặc `ip route`.

*   Dùng để kiểm tra Default Gateway (`0.0.0.0`) có đúng không khi server không ra được internet.

**b. Interface Statistics (`netstat -i`)**

```bash
Iface      MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
eth0      1500   12345      0      0      0    12345      0      0      0 BMRU
```

*   **RX-ERR / TX-ERR:** Nếu số này tăng, có thể do cáp mạng hỏng, switch lỗi hoặc duplex mismatch.
	
*   **RX-DRP (Drop):** Server quá tải, CPU không xử lý kịp gói tin, hoặc firewall (iptables) đang drop gói tin.

---

### 6. Sự chuyển dịch: Netstat vs. SS (Socket Statistics)

Đây là kiến thức phân biệt giữa Junior và Senior.

*   **Netstat:** Đọc thông tin từ `/proc/net/tcp`. Khi hệ thống có hàng chục nghìn kết nối, việc đọc file này rất chậm và tốn CPU.
	
*   **SS (`iproute2` package):** Lấy thông tin trực tiếp từ kernel space qua **Netlink API**. Nhanh hơn rất nhiều.

**Bảng chuyển đổi cho DevOps:**

| Mục đích                            | Lệnh Netstat (Cũ)         | Lệnh SS (Mới - Khuyên dùng) |     |
| :---------------------------------- | :------------------------ | :-------------------------- | --- |
| Xem tất cả TCP/UDP port đang listen | `netstat -tulpn`          | `ss -tulpn`                 |     |
| Xem kết nối đã thiết lập            | `netstat -atn`            | `ss -atn`                   |     |
| Xem tóm tắt thống kê (Summary)      | `netstat -s`              | `ss -s` (Rất gọn và đẹp)    |     |
| Lọc theo port                       | `netstat -an \| grep :80` | `ss -tn sport = :80`        |     |

---

### 7. Tổng kết: Checklist cho DevOps Engineer

Khi sử dụng `netstat`, hãy luôn nhớ quy trình tư duy này:
	
1.  **Check Listening:** Service có chạy và bind đúng IP/Port không? (`-tulpn`)
	
2.  **Check Connection:** Ai đang kết nối vào? (`-an`)
	
3.  **Check State:** Có bị leak connection (`CLOSE_WAIT`) hay cạn resource (`TIME_WAIT`) không?
	
4.  **Check Bottleneck:** Có IP nào spam kết nối không? (Dùng `awk` để lọc).
	
5.  **Performance:** Nếu server tải cao, hãy chuyển sang dùng `ss` thay vì `netstat`.

---