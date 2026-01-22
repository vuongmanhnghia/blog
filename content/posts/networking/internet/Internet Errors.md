---
title: Các vấn đề về Internet và cách khắc phục
date: 2025-09-16
image:
categories:
  - network
  - internet
tags:
  - dns
  - firewall
  - ip
draft: false
---

Các vấn đề về kết nối Internet phổ biến và cách khắc phục chi tiết

<!--more-->

--- 
## I. CHUẨN ĐOÁN VẤN ĐỀ

### Bước 1: Kiểm tra kết nối vật lý

```bash
# Kiểm tra card mạng có được nhận diện không
lspci  | grep -i network
lspci  | grep -i ethernet
lsusb | grep -i wireless

# Kiểm tra interface có tồn tại không
ip link show
ifconfig -a
```

**Kết quả mong đợi:** Thấy các interface như `eth0`, `wlan0`, `enp0s3`

### Bước 2: Kiểm tra trạng thái Interface

```bash
# Xem trạng thái chi tiết
ip addr show
nmcli device status

# Kiểm tra interface có UP không
ip link show eth0     # Thay eth0 bằng interface của bạn
```

**Phân tích kết quả**
	
- `UP`: Interface đã bật
	
- `DOWN`:  Interface bị tắt
	
- `NO-CARRIER`: Không có tín hiệu (Dây mạng rút, không có sóng Wifi)

### Bước 3: Test kết nối từng lớp

```bash
# Layer 1-2: Kiểm tra link local
ping -c 3 127.0.0.1

# Layer 3: Kiểm tra gateway
ip route show                      # Xem default gateway
ping -c 3 <gateway-ip>     # Ping gateway

# Layer 3: Kiểm tra DNS server
ping -c 3 1.1.1.1                     # Ping IP trực tiếp (Cloudflared / Google)

# Layer 4: Kiểm tra phân giải tên miền
nslookup google.com
ping -c 3 google.com
```

### Bước 4: Kiểm tra cấu hình mạng

```bash
# Kiểm tra IP configuration
ip addr show
route -n

# Kiểm tra DNS setting
cat /etc/resolv.conf
system-resolve --status

# Kiểm tra DHCP
sudo dhclient -v eth0     # Test DHCP renewal
```

### Bước 5: Kiểm tra service và process

```bash
# Kiểm tra network services
systemctl status NetworkManager
systemctl status networking
systemctl status systemd-networkd

# Kiểm tra Firewall
sudo ufw status
sudo iptables -L -n

# Kiểm tra process sử dụng network
ss -tuln            # Listening ports
netstart -rn     # Routing table
```

### Bước 6: Xem Logs và Error messages

```bash
journalctl -u NetworkManager -f
dmesg | grep -i network
dmesg | grep -i eth
dmesg | grep -i wlan

# Kernal messages
dmes | tail -20
tail -f var/log/syslog | grep -i network
```

### Ma trận chuẩn đoán nhanh

| Triệu chứng             | Lệnh kiểm tra           | Nguyên nhân có thể           |
| ----------------------- | ----------------------- | ---------------------------- |
| Không thấy interface    | `ip link show`          | Driver không có/sai          |
| Interface DOWN          | `ip link show`          | Interface bị disable         |
| Không có IP             | `ip addr show`          | DHCP fail, static config sai |
| Ping localhost fail     | `ping 127.0.0.1`        | Network stack broken         |
| Ping gateway fail       | `ping <gateway>`        | L2/L3 problem                |
| Ping IP OK, domain fail | `nslookup google.com`   | DNS problem                  |
| Kết nối chậm            | `traceroute google.com` | Routing/bandwidth issue      |
### Scripts auto chuẩn đoán lỗi

```bash
#!/bin/bash
echo "=== NETWORK DIAGNOSTIC REPORT ==="
echo "Date: $(date)"
echo

echo "1. NETWORK INTERFACES:"
ip link show
echo

echo "2. IP ADDRESSES:"
ip addr show
echo

echo "3. ROUTING TABLE:"
ip route show
echo

echo "4. DNS CONFIGURATION:"
cat /etc/resolv.conf
echo

echo "5. CONNECTIVITY TESTS:"
echo -n "Localhost: "
ping -c 1 -W 2 127.0.0.1 >/dev/null 2>&1 && echo "OK" || echo "FAIL"

GATEWAY=$(ip route | grep default | awk '{print $3}' | head -1)
if [ ! -z "$GATEWAY" ]; then
    echo -n "Gateway ($GATEWAY): "
    ping -c 1 -W 2 $GATEWAY >/dev/null 2>&1 && echo "OK" || echo "FAIL"
fi

echo -n "External DNS (8.8.8.8): "
ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1 && echo "OK" || echo "FAIL"

echo -n "Domain resolution (google.com): "
nslookup google.com >/dev/null 2>&1 && echo "OK" || echo "FAIL"

echo
echo "6. ACTIVE SERVICES:"
systemctl is-active NetworkManager 2>/dev/null && echo "NetworkManager: Active" || echo "NetworkManager: Inactive"
systemctl is-active networking 2>/dev/null && echo "networking: Active" || echo "networking: Inactive"
```

Chạy scripts

```bash
chmod +x network-diagnostic.sh
./network-diagnostic.sh
```


---

## II. XỬ LÝ LỖI

### 1. Không kết nối được mạng

*Kiểm tra trạng thái mạng*

```bash
ip link show
ip addr show
nmcli device status
```

*Khắc phục*

```bash
# Khởi động lại network manager
sudo systemctl restart NetworkManager

# Hoặc khởi động lại networking service
sudo systemctl restart networking
```

### 2. Lỗi DNS không phân giải được

*Kiểm tra DNS*

```bash
nslookup google.com
dig google.com
cat /etc/resolv.conf
```

*Khắc phục*

```bash
# Thay đổi DNS server
sudo nano /etc/resolv.conf

# Thêm các dòng sau:
# Cloudflared
nameserver 1.1.1.1
nameserver 1.0.0.1

# Google
nameserver 8.8.8.8
nameserver 8.8.4.4
```

### 3. Lỗi drive card mạng

*Kiểm tra drive*

```bash
lspci -nnk | grep -iA2 net
lsusb  # cho USB WiFi adapter
dmesg | grep -i network
```

*Khắc phục*

```bash
# Cài đặt driver thiếu
sudo apt update
sudo apt install linux-firmware
sudo apt install firmware-iwlwifi  # cho Intel WiFi

# Khởi động lại
sudo modprobe -r iwlwifi && sudo modprobe iwlwifi
```

### 4. Lỗi Wifi không kết nối được

```bash
iwconfig
nmcli dev wifi list
rfkill list
```

*Khắc phục*

```bash
# Bật WiFi nếu bị tắt
sudo rfkill unblock wifi

# Kết nối WiFi
nmcli dev wifi connect "TenWiFi" password "MatKhau"

# Reset network settings
sudo rm /var/lib/NetworkManager/NetworkManager.state
sudo systemctl restart NetworkManager
```

### 5. Lỗi IP conflict hoặc không nhận được IP

```bash
ip route show
dhclient -v
```

*Khắc phục*

```bash
# Renew IP address
sudo dhclient -r
sudo dhclient

# Hoặc reset network interface
sudo ifdown eth0 && sudo ifup eth0
```

### 6. Lỗi firewall chặn kết nối

*Kiểm tra firewall*

```bash
sudo ufw status
sudo iptables -L
```

*Khắc phục*

```bash
# Tạm thời tắt firewall để test
sudo ufw disable

# Hoặc mở port cần thiết
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow ssh
```

### 7. Lỗi proxy settings

*Kiểm tra proxy*

```bash
echo $http_proxy
echo $https_proxy
cat /etc/environment
```

*Khắc phục*

```bash
# Xóa proxy settings
unset http_proxy
unset https_proxy
unset HTTP_PROXY
unset HTTPS_PROXY

# Hoặc cấu hình đúng proxy
export http_proxy=http://proxy-server:port
export https_proxy=http://proxy-server:port
```

### 8. Lỗi MTU size

*Kiểm tra và fix MTU*

```bash
# Kiểm tra MTU hiện tại
ip link show

# Thay đổi MTU
sudo ip link set dev eth0 mtu 1400

# Hoặc cấu hình vĩnh viễn trong /etc/network/interfaces
```


---

## III. RESET HOÀN TOÀN NETWORKING

```bash
# Backup cấu hình cũ nếu cần
sudo cp -r /etc/NetworkManager /etc/NetworkManager.backup

# Reset NetworkManager
sudo rm -rf /etc/NetworkManager/system-connections/*
sudo systemctl stop NetworkManager
sudo systemctl start NetworkManager

# Hoặc reinstall network packages
sudo apt remove --purge network-manager
sudo apt install network-manager
```

--- 
