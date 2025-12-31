---
title: Hướng dẫn thiết lập Network Bridge giữa máy Host và máy ảo
date: 2025-11-10
image:
categories:
  - network
  - internet
tags:
  - bridge
draft: false
---

**bridged network** là phương pháp chuyên nghiệp và linh hoạt nhất cho máy chủ ảo, vì nó cho phép máy ảo của bạn hoạt động như một thiết bị vật lý thực thụ trên mạng của bạn.

<!--more-->

---
### Tổng quan Workflow

1.  **Chuẩn bị (Trên máy Host):** Thu thập thông tin mạng và chọn IP tĩnh cho máy ảo.
2.  **Cấu hình Mạng Host (Trên máy Host):** Tạo một "cầu nối mạng" (hình) để kết nối card mạng vật lý với máy ảo.
3.  **Cấu hình Máy ảo (Trên máy Host):** Cấu hình sử dụng network bridge vừa tạo.
4.  **Cấu hình IP Tĩnh (Trong máy ảo Guest):** Truy cập vào máy ảo và thiết lập IP tĩnh bằng `netplan`.
5.  **Kiểm tra và Hoàn tất.**

---

### Bước 1: Chuẩn bị (Trên máy Host)

1.  **Tìm tên card mạng vật lý và Gateway:**
	
    ```bash
    ip addr       # Tìm tên card mạng, vd: eno1, eth0, wlp3s0
    ip route      # Tìm địa chỉ Default Gateway
    ```
    *Giả sử card mạng vật lý của bạn là `eno1` và Gateway là `192.168.0.1`.*
	
2.  **Chọn IP tĩnh cho máy ảo:**
	
    *   Dựa vào Gateway `192.168.0.1`, bạn biết mạng của mình là `192.168.0.x`.
		
    *   Kiểm tra dải DHCP trên router của bạn (ví dụ: `192.168.0.100` - `192.168.0.199`).
		
    *   Chọn một IP **nằm ngoài** dải DHCP đó để tránh xung đột. Ví dụ: **`192.168.0.55`**.
		
    *   Kiểm tra xem IP này có đang được sử dụng không: `ping -c 3 192.168.0.55`. Nếu không có phản hồi là tốt.
	
3.  **Tổng hợp thông tin:**

| Thông tin                | Giá trị ví dụ          | Ghi chú                  |
| :----------------------- | :--------------------- | :----------------------- |
| Tên card mạng vật lý     | `eno1`                 | Ghi lại tên thật của bạn |
| Địa chỉ IP tĩnh (cho VM) | `192.168.0.55`         | IP bạn vừa chọn          |
| Gateway                  | `192.168.0.1`          | Địa chỉ router của bạn   |
| Netmask / CIDR           | `255.255.255.0` / `24` | Ghi `24` là đủ           |
| DNS Servers              | `1.1.1.1`, `1.0.0.1`   | Dùng DNS bạn muốn        |

---

### Bước 2: Cấu hình Cầu nối Mạng trên Host (`nmcli`)

1.  **Tạo một cầu nối ảo tên `br0`:**
	
    ```bash
    sudo nmcli con add type bridge con-name br0 ifname br0
    ```
    
2.  **Cấu hình IP cho cầu nối `br0`:** Cầu nối này sẽ "tiếp quản" địa chỉ IP của máy Host.
	
    ```bash
    # Lấy IP hiện tại của máy host, vd: 192.168.0.40
    # Bạn có thể giữ IP động hoặc đặt IP tĩnh cho máy host, ở đây ta đặt tĩnh cho ổn định
    sudo nmcli con mod br0 ipv4.addresses 192.168.0.40/24 ipv4.gateway 192.168.0.1 ipv4.dns "1.1.1.1,1.0.0.1" ipv4.method manual
    ```
    
3.  **Gán card mạng vật lý `eno1` vào cầu nối `br0`**
	
    ```bash
    # Thay 'eno1' bằng tên card mạng thật của bạn
    sudo nmcli con add type bridge-slave con-name br0-slave ifname eno1 master br0
    ```
    
4.  **Kích hoạt cầu nối:**
	
    ```bash
    # Tắt kết nối cũ của card vật lý (nếu đang hoạt động)
    sudo nmcli con down eno1
    
    # Kích hoạt cầu nối
    sudo nmcli con up br0
    ```
    *Lưu ý: Bạn có thể bị mất kết nối mạng trong giây lát. Sau bước này, máy host của bạn sẽ truy cập mạng thông qua `br0`.*

5.  **Kiểm tra lại:** Chạy `ip addr`. Bạn sẽ thấy `br0` có địa chỉ IP, và `eno1` không có IP nhưng có trạng thái `master br0`.

---

### Bước 3: Cấu hình Máy ảo sử dụng Cầu nối

Bây giờ, hãy chỉ cho máy ảo của bạn sử dụng `br0`.

*   **Cách 1: Dùng `virt-manager` (GUI):**
	
    1.  Tắt máy ảo.
		
    2.  Mở `virt-manager`, chọn máy ảo và vào phần **Details** (Biểu tượng bóng đèn).
		
    3.  Chọn mục **"NIC"** (Network Interface Controller).
		
    4.  Trong phần **"Network source"**, chọn **"Bridge device"**.
		
    5.  Trong ô **"Device name"**, nhập `br0`.
		
    6.  Lưu lại.
	
*   **Cách 2: Dùng `virsh` (Dòng lệnh):**
	
    1.  Tắt máy ảo: `virsh shutdown ten_may_ao`
		
    2.  Mở file cấu hình XML của máy ảo: `virsh edit ten_may_ao`
		
    3.  Tìm đến phần `<interface>`. Nó sẽ trông giống như thế này:
		
        ```xml
        <interface type='network'>
          <source network='default'/>
          ...
        </interface>
        ```
		
    4.  Sửa nó thành:
		
        ```xml
        <interface type='bridge'>
          <source bridge='br0'/>
          <model type='virtio'/>  <!-- Giữ nguyên model type nếu có -->
          ...
        </interface>
        ```
		
    5.  Lưu và thoát.

---

### Bước 4: Cấu hình IP Tĩnh trong Máy ảo (Netplan)

1.  **Khởi động máy ảo** của bạn và đăng nhập.
	
2.  Tìm tên file cấu hình netplan trong `/etc/netplan/` (ví dụ: `00-installer-config.yaml`).
	
3.  Mở file đó để chỉnh sửa: `sudo nano /etc/netplan/00-installer-config.yaml`.
	
4.  Xóa nội dung cũ và thay bằng cấu hình sau (sử dụng thông tin bạn đã chuẩn bị ở Bước 1). **Cẩn thận với thụt đầu dòng!**
	
    ```yaml
    network:
      ethernets:
        ens3: # <-- Thay bằng tên card mạng trong máy ảo (dùng 'ip a' để xem)
          dhcp4: no
          addresses:
            - 192.168.0.55/24 # <-- IP tĩnh bạn đã chọn
          gateway4: 192.168.0.1
          nameservers:
            addresses: [1.1.1.1, 1.0.0.1]
      version: 2
    ```
    
5.  Lưu file (`Ctrl + X`, `Y`, `Enter`).
	
6.  Áp dụng cấu hình: `sudo netplan apply`.

---

### Bước 5: Kiểm tra và Hoàn tất

1.  **Trong máy ảo:**
	
    *   `ip a`: Kiểm tra xem máy ảo đã nhận đúng IP `192.168.0.55` chưa.
		
    *   `ping 192.168.0.1`: Ping tới gateway.
		
    *   `ping google.com`: Ping ra Internet để kiểm tra DNS.
	
2.  **Trên máy Host (hoặc một máy tính khác cùng mạng):**
	
    *   `ping 192.168.0.55`: Ping tới địa chỉ IP mới của máy ảo.
	
Nếu tất cả các bước ping đều thành công, bạn đã hoàn tất! Máy ảo của bạn giờ đây đã là một thành viên chính thức trên mạng LAN với một địa chỉ IP tĩnh đáng tin cậy.

---