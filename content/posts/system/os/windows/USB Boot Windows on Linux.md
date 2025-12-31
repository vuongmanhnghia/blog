---
title: Hướng dẫn tạo USB Boot Windows trên Linux
date: 2025-10-04
image:
categories:
  - system
  - os
tags:
  - windows
draft: false
---

Có một số cách để tạo USB boot Windows trên Linux. Đây là phương pháp phổ biến nhất:

<!--more-->

---

## Sử dụng WoeUSB-ng

### Cài đặt

```bash
# Ubuntu/Debian
sudo apt install git p7zip-full python3-pip python3-wxgtk4.0
sudo pip3 install WoeUSB-ng

# Fedora
sudo dnf install WoeUSB-ng
```

### Sử dụng

```bash
sudo woeusb --device /đường/dẫn/tới/Windows.iso /dev/sdX
```

*(Thay `/dev/sdX` bằng USB của bạn, ví dụ `/dev/sdb`)*

## Cách nhận biết tên thiết bị USB trên Linux

### 1. Command `lsblk`

```bash
lsblk
```

Kết quả sẽ hiển thị dạng:

```bash
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0 238.5G  0 disk 
├─sda1   8:1    0   512M  0 part /boot/efi
└─sda2   8:2    0   238G  0 part /
sdb      8:16   1  14.9G  0 disk           <-- Đây là USB
└─sdb1   8:17   1  14.9G  0 part /media/user/USB
```

**Nhận biết:** USB thường có `RM` = 1 (removable), dung lượng nhỏ hơn ổ cứng chính.

### 2. Command `sudo fdisk -l`

```bash
sudo fdisk -l
```

Tìm thiết bị có nhãn như "USB" hoặc dung lượng khớp với USB của bạn.

---