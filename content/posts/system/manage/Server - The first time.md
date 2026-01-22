---
title: Quy trình chuẩn khi nhận server lần đầu
date: 2025-11-14
image:
categories:
  - system
  - server
tags:
  - tips
draft: true
---
SSH thẳng vào root nghe tiện, nhưng nó giống kiểu bạn để chìa khóa nhà trước cửa rồi bảo “đã khoá rồi mà”. Tạo user mới rồi dùng sudo an toàn và kiểm soát được hơn nhiều

<!--more-->

---

## Tại sao **không nên SSH root trực tiếp**?

1. **Root không có history phân biệt người dùng**
	
	- Nếu bạn cho nhiều người SSH root → không biết ai làm gì.  
	Audit = bằng 0.
		
	- SSH vào user thường rồi sudo → mỗi hành động đều gắn với identity.
	
2. **Brute-force root quá dễ**
	
	- 90% botnet ngoài kia quét **port 22** và spam login “root” liên tục.
		
	- Disable SSH root login là chặn được cả rừng tấn công rác.
	
3. **Lỡ tay một phát là đi cả server**
	
	- Root không có giới hạn. Một command ngu kiểu:
		
		```
		rm -rf /
		```
		
		hoặc
		
		```
		chown -R root:root /
		```
		
		Có thể bốc hơi cả hệ thống.
		
	- Dùng user thường + sudo → giảm rủi ro chết server chỉ vì typo.
	
4. **Privilege escalation khó hơn**

	- Nếu attacker có account user thường → vẫn phải vượt qua sudo password, sudoers rule.
		
	- Nếu attacker vào root luôn → xong phim.
	
5. **Best practice của mọi distro / cloud provider**

	- AWS, GCP, Azure, DigitalOcean, Hetzner → **đều không cho SSH root mặc định**.  
	- Họ luôn yêu cầu:
		
		- login bằng user thường (ubuntu, ec2-user, admin…)
			
		- dùng sudo khi cần quyền cao.
		
	
---

## Quy trình chuẩn khi nhận server lần đầu

1. **SSH vào root (chỉ lần đầu)**
    
2. **Tạo user mới**
    
    ```bash
    # Nhớ thay thành tên của bạn =))
    adduser nagih
    usermod -aG sudo nagih
    ```
    
	- `-a` append
		
	- `-G` group
    
3. **Copy SSH key sang**
    
    ```bash
    rsync -av /root/.ssh /home/nagih/
    chown -R nagih:nagih /home/nagih/.ssh
    ```
	
	- `-a` archive mode (Là combo “một nút làm hết” của rsync, copy toàn bộ bao gồm cả cấu hình)
		
	- `-v` verbose
	
4. **Disable SSH root login**  
	
    `/etc/ssh/sshd_config`:
    
    ```bash
    PermitRootLogin no
    ```
    
    Rồi reload:
    
    ```bash
    systemctl reload sshd
    ```
    
5. **Logout → SSH bằng user mới → sudo su** nếu cần.
    

---

# Vậy có trường hợp nào **nên** SSH root không?

Có vài trường hợp hiếm:

- server rescue mode
    
- container không có user thường (Alpine base quá nhỏ)
    
- máy lab/test local
    
- troubleshooting kernel/boot
    

Nhưng với **production server**, đặc biệt là máy deploy app hoặc server internet-facing → luôn dùng user thường.

---

# Tóm gọn dễ nhớ

SSH root trực tiếp = cửa chính mở toang.  
User thường + sudo = có chìa khóa nhưng vẫn cần “thêm một lớp xác nhận” khi làm việc quan trọng.

Trong DevOps, điều này giúp bạn an toàn, audit được, và tránh “tai nạn nghề nghiệp”.

---

Nếu bạn muốn mình làm cho bạn một checklist đầy đủ khi chuẩn bị một server production (tạo user, ssh-hardening, firewall, fail2ban, unattended-upgrades, secure sysctl…) thì mình viết luôn cho bạn một bản chuẩn hóa.