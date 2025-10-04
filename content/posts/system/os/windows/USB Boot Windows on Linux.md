---
title: Hướng dẫn tạo USB Boot Windows trên Linux
date: 2025-10-04
image:
categories:
  - OS
  - system
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
