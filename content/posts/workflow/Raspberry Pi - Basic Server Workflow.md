---
title: Hướng dẫn setup môi trường server cơ bản chạy web và các dịch vụ nền cho Raspberry Pi (Debian)
date: 2025-10-15
image:
categories:
  - server
  - workflow
tags:
draft: false
---

<!--more-->

---
## Phase 1: Server Initialization & Basic Configuration
### 1. First Connect

```bash
ssh root@your_server_ip
```

### 2. Create new User

```bash
# add user
adduser your_username

# sudo authorization
usermod -aG sudo your_username
```

### 3. FW - Uncomplicated Firewall

```bash
# Install ufw if not available
sudo apt install ufw

# Allow ssh connection
sudo ufw allow OpenSSH

 # Activate firewall
sudo ufw enable                   
```

### 4. Update System

```bash
apt update & apt upgrade -y
```

### 5. Re-Login

```bash
ssh your_username@your_server_ip
```

---

## Phase 2: Setup Environment

### Docker & Docker Compose

```bash
# Install Docker
curl -sSL https://get.docker.com | sh

# Add user to docker group
sudo usermod -aG docker $USER

# Re-Login to Apply changes
```

### Kích hoạt memory cgroups trên nếu cần

```bash
docker info

# Cần kích hoạt nếu xuất hiện logs dưới đây:
WARNING: No memory limit support  
WARNING: No swap limit support
```

1. **Mở tệp `cmdline.txt` **

	```bash
	sudo nano /boot/firmware/cmdline.txt
	```

2. **Thêm các tham số cấu hình**

```bash
# Thêm các tham số sau vào cùng một dòng với các nội dung hiện có, không xuống dòng mới
cgroup_enable=memory cgroup_memory=1
```

3. **Save và Reboot**

```bash
sudo reboot
```

### [Cloudflared Tunnel Workflow](posts/workflow/cloudflared-tunnel-workflow)
