---
title: Tất cả các commands quản lý quan trọng trên linux
date: 2025-11-14
image:
categories:
  - system
  - manage
  - server
tags:
  - user
draft: false
---

<!--more-->

---
## 1. **User** management command

### **useradd**

Tạo user mới.

```bash
sudo useradd nagih
sudo useradd -m -s /bin/bash nagih
```
	
- `-m` tạo home
- `-s` set shell.

### **adduser** (wrapper dễ dùng hơn)

Ubuntu thường dùng cái này.

```bash
sudo adduser nagih
```

### **userdel**

Xoá user.

```bash
sudo userdel nagih
sudo userdel -r nagih   # xoá cả home
```

### **usermod**

Sửa thông tin user.

```bash
# thêm user vào group
sudo usermod -aG docker nagih

# đổi shell   
sudo usermod -s /bin/zsh nagih

# đổi home directory
sudo usermod -d /new/home nagih  
```

### **passwd**

Đổi mật khẩu user.

```bash
sudo passwd nagih

# lock password
sudo passwd -l nagih   

# unlock
sudo passwd -u nagih   
```

### **chage**

Quản lý tuổi mật khẩu (password aging).

```bash
sudo chage -l nagih
sudo chage -E 2025-01-01 nagih
```

### **id**

Xem UID/GID của user.

```bash
id nagih
```

### **whoami**

Xem user hiện tại.

```bash
whoami
```

### **last / lastlog**

Xem lịch sử login.

```bash
last
lastlog
```

### **su**

Switch user.

```bash
su - nagih
```

### **loginctl**

Nếu dùng systemd – quản lý session của user.

```bash
loginctl list-sessions
loginctl show-user nagih
```

---

## 2. **Group** management command

### **groupadd**

Tạo group.

```bash
sudo groupadd devops
sudo groupadd -g 1500 customgroup
```
	
- `-g` **GID** flag (Group ID)

### **groupdel**

Xoá group.

```bash
sudo groupdel devops
```

### **groupmod**

Sửa group.

```bash
sudo groupmod -n newname oldname
sudo groupmod -g 1600 devops
```
	
- `-n` change group name
- `-g` GID

### **gpasswd**

Quản lý member của group.

```bash
sudo gpasswd -a nagih docker
sudo gpasswd -d nagih docker
```
	
- `-a` add `member` to `group`
- `-d` delete `member` from `group`

### **newgrp**

Switch group tạm thời.

```bash
newgrp docker
```
	
- Tạo **một shell mới**.
    
- Shell này dùng **docker** như nhóm chính (effective GID).
    
- Các quyền file và lệnh yêu cầu group `docker` hoạt động ngay lập tức.
    
- Khi bạn `exit`, bạn quay lại shell cũ (vẫn chưa có quyền).

---

## 3. Important user related files

Không phải command nhưng bạn luôn gặp:

```bash
# danh sách user
/etc/passwd

# danh sách group
/etc/group       

# mật khẩu (hash)
/etc/shadow     

# quyền sudo 
/etc/sudoers     
```

Xem file:

```bash
cat /etc/passwd
cat /etc/group
sudo visudo
```

---

## 4. Tool to check what user is running

### **who / w**

Ai đang đăng nhập.

```bash
who
w
```

### **finger** (nếu cài)

Thông tin user.

```bash
finger nagih
```

---

## 5.  Permission control tool

### **chown**

Đổi chủ sở hữu file.

```bash
sudo chown nagih:devops file.txt
```

### **chmod**

Đổi permission.

```bash
chmod 755 script.sh
```

---

## 6. Bonus: command DevOps thường dùng liên quan user trong container

### **useradd trong Dockerfile**

```bash
RUN groupadd -g 1000 app && useradd -u 1000 -g app -m app
USER app
```

### **id trong container**

```bash
docker exec app id
```

---