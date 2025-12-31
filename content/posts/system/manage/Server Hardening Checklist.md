---
title: Những điều cần làm ngay sau khi sở hữu 1 server Linux (VPS, Cloud)
date: 2025-11-14
image:
categories:
  - manage
  - server
  - linux
  - system
tags:
  - tips
draft: false
---
<!--more-->

---

### 1. **Tạo user thường + tắt SSH root**

```bash
adduser nagih
usermod -aG sudo nagih
```

Copy SSH key:

```bash
rsync -av /root/.ssh /home/nagih/
chown -R nagih:nagih /home/nagih/.ssh
```

Disable SSH root:

```bash
sudo nano /etc/ssh/sshd_config
```

Sửa:

```bash
PermitRootLogin no
PasswordAuthentication no     # nếu bạn dùng SSH key
```

Reload:

```bash
sudo systemctl reload sshd
```

---

### 2. **Đặt hostname, timezone, locale đúng**

Log hợp lệ để debug. Script không phát điên khi timezone sai.

```bash
sudo hostnamectl set-hostname server-01
sudo timedatectl set-timezone Asia/Ho_Chi_Minh
```

---

### 3. **Cập nhật hệ thống + bật auto security updates**

```bash
sudo apt update && sudo apt upgrade -y
```

Bật auto security patch:

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure unattended-upgrades
```

---

### 4. **Firewall: UFW/NFTABLES**

Ngăn dịch vụ lạ bị expose.

UFW cách đơn giản:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

sudo ufw enable
```

Nếu bạn DevOps hardcore, dùng nftables hoặc firewalld.

---

### 5. **Fail2ban chống brute force**

```bash
sudo apt install fail2ban -y
```

Tạo cấu hình:

```bash
sudo nano /etc/fail2ban/jail.local
```

Ví dụ:

```bash
[sshd]
enabled = true
maxretry = 5
bantime = 1h
```

Restart:

```bash
sudo systemctl restart fail2ban
```

---

### 6. **SSH hardening nâng cao**

Trong `/etc/ssh/sshd_config` thêm:

```bash
Protocol 2
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
ClientAliveInterval 300
ClientAliveCountMax 2
PasswordAuthentication no
```

Nếu bạn muốn whitelist user:

```bash
AllowUsers nagih deploy
```

---

### 7.**Giới hạn sudo để tránh phá server**

Rất nên có `/etc/sudoers.d/99-safe`:

```bash
nagih ALL=(ALL) NOPASSWD: /usr/bin/systemctl, /usr/bin/journalctl, /usr/bin/docker
nagih ALL=(ALL) !/bin/rm -rf /
```

Tuỳ nhu cầu.

---

### 8. **Swap (nếu server ít RAM)**

```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

Thêm vào `/etc/fstab`:

```bash
/swapfile swap swap defaults 0 0
```

---

### 9. **Ứng dụng logs chuẩn hóa**

- `journalctl -u service`
    
- Logrotate cho file log custom
    
- Đồng bộ giờ với NTP
    

Cài chrony:

```bash
sudo apt install chrony -y
```

---

### 10. **Disable dịch vụ không cần**

Giảm attack surface:

```bash
systemctl list-unit-files --type=service
sudo systemctl disable --now bluetooth.service
sudo systemctl disable --now cups.service
sudo systemctl disable --now avahi-daemon.service
```

---

### 11. **Bật AppArmor hoặc SELinux (nếu dùng Ubuntu hoặc CentOS)**

Ubuntu:

```bash
sudo aa-status
```

CentOS:

```bash
sestatus
```

---

### 12. **Cấu hình phân quyền file**

- Không cho world-writable file
    
- Check SUID/SGID
    

```bash
sudo find / -perm /6000 -type f 2>/dev/null
```

Nếu không hiểu file nào → mình đọc giúp.

---

### 13. **Cài monitoring tối thiểu**

Prometheus Node Exporter:

```bash
sudo useradd -rs /bin/false node_exporter
```

Cài binary → systemd → kết nối Grafana.

Còn không thì dùng Netdata cho nhanh.

---

### 14. **Cấu hình backups**

Tối thiểu:

- backup `/etc`
    
- backup database
    
- snapshot volume (nếu cloud)
    
- script cron: rsync → S3/Backblaze
    

---

### 15. **Nếu chạy Docker**

Hardening Docker:

```bash
sudo usermod -aG docker nagih
sudo systemctl enable docker
```

Cấu hình daemon:

`/etc/docker/daemon.json`:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Cài compose plugin:

```
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

---

### 16. **Nếu chạy web service**

- Reverse proxy: Nginx / Caddy
    
- HSTS
    
- Certbot hoặc Traefik cert auto
    
- Rate-limit
    

---

### 17. **Tắt IPv6 nếu không dùng**

```bash
sudo nano /etc/sysctl.conf
```

Thêm:

```bash
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```

```bash
sudo sysctl -p
```

---

### 18. **Kiểm thử security tổng quan**

```bash
ss -tulpn
```

Đảm bảo chỉ có:

- 22
- 80
- 443  

Kiểm tra SSH:

```bash
ssh -v yourserver
```

Test brute-force protection:

```bash
fail2ban-client status sshd
```

---

### 19. **Automation lại toàn bộ**

Dùng:

- Ansible
    
- Terraform + cloud-init
    
- bash script
    

Sản xuất không ai setup tay hoài được.

---

### 20. **Viết tài liệu 1 trang về server**

- OS version
    
- Dịch vụ đang chạy
    
- User có quyền sudo
    
- Port mở
    
- Backup location
    
- Cách restart service
    
- SSH key location
    

Cực hữu ích khi giao server cho team khác.

---

### Bunus: Scripts tự động setup cơ bản

**SERVER-BASELINE.SH**

```bash
sudo bash server-baseline.sh
```
---

**server-baseline.sh**

```bash
#!/bin/bash

set -e

USERNAME="nagih"
PUBKEY="ssh-ed25519 AAAA...YOUR_KEY_HERE"

echo "[1/10] Creating user..."
if ! id "$USERNAME" >/dev/null 2>&1; then
    adduser --disabled-password --gecos "" "$USERNAME"
    usermod -aG sudo "$USERNAME"
else
    echo "User already exists, skipping."
fi

echo "[2/10] Installing SSH key..."
mkdir -p /home/$USERNAME/.ssh
echo "$PUBKEY" > /home/$USERNAME/.ssh/authorized_keys
chmod 700 /home/$USERNAME/.ssh
chmod 600 /home/$USERNAME/.ssh/authorized_keys
chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh

echo "[3/10] SSH Hardening..."
SSHCONF="/etc/ssh/sshd_config"
sed -i 's/#\?PasswordAuthentication .*/PasswordAuthentication no/' $SSHCONF
sed -i 's/#\?PermitRootLogin .*/PermitRootLogin no/' $SSHCONF
sed -i 's/#\?X11Forwarding .*/X11Forwarding no/' $SSHCONF
sed -i 's/#\?AllowAgentForwarding .*/AllowAgentForwarding no/' $SSHCONF
sed -i 's/#\?AllowTcpForwarding .*/AllowTcpForwarding no/' $SSHCONF

# Thêm AllowUsers nếu chưa có
if ! grep -q "AllowUsers" $SSHCONF; then
    echo "AllowUsers $USERNAME" >> $SSHCONF
fi

systemctl reload sshd

echo "[4/10] Updating system..."
apt update && apt upgrade -y

echo "[5/10] Installing essential tools..."
apt install -y unattended-upgrades fail2ban ufw htop curl

echo "[6/10] Enabling auto security updates..."
dpkg-reconfigure --priority=low unattended-upgrades

echo "[7/10] Configuring UFW firewall..."
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "[8/10] Configuring Fail2ban..."
cat >/etc/fail2ban/jail.local <<EOF
[sshd]
enabled = true
maxretry = 5
bantime = 1h
EOF
systemctl restart fail2ban

echo "[9/10] Setting timezone to Asia/Ho_Chi_Minh..."
timedatectl set-timezone Asia/Ho_Chi_Minh

echo "[10/10] Cleaning up..."
apt autoremove -y

echo
echo "======================================"
echo " Baseline complete!"
echo " Login using: ssh $USERNAME@your-server"
echo "======================================"
```

---
1.  Thay SSH key
	
	Trong script:
	
	```bash
	PUBKEY="ssh-ed25519 AAAA...YOUR_KEY_HERE"
	```
	
	Dán public key của bạn vào.
	
2. Lưu file, chạy:
	
	```bash
	chmod +x server-baseline.sh
	sudo ./server-baseline.sh
	```

---
