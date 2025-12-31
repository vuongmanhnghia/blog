---
title: Hướng dẫn sửa lỗi Docker Stats không hiển thị mức sử dụng memory
date: 2025-11-02
image:
categories:
  - docker
tags:
draft: false
---

Việc lệnh `docker stats` không hiển thị thông tin về bộ nhớ (MEM USAGE / LIMIT) cho các container là một sự cố khá phổ biến. Nguyên nhân chính thường liên quan đến tính năng theo dõi bộ nhớ của `cgroups` chưa được kích hoạt.

<!--more-->

---

Việc lệnh `docker stats` không hiển thị thông tin về bộ nhớ (MEM USAGE / LIMIT) cho các container là một sự cố khá phổ biến. Nguyên nhân chính thường liên quan đến tính năng theo dõi bộ nhớ của `cgroups` chưa được kích hoạt.

### Bước 1: Kiểm tra cấu hình Docker

```bash
docker info
```

Nếu tính năng này bị thiếu, bạn có thể sẽ thấy các cảnh báo ở cuối kết quả, tương tự như sau:  
WARNING: No memory limit support  
WARNING: No swap limit support

### Bước 2: Kích hoạt Memory Cgroup cho Kernel

- **Mở file cmdline.txt**
	
	```bash
	sudo nano /boot/cmdline.txt
	```
	
- **Thêm các tham số cấu hình**
	
	```bash
	cgroup_enable=memory cgroup_memory=1
	```
	
	**Lưu ý:** Tệp cmdline.txt chứa tất cả các tham số trên một dòng duy nhất. Hãy chắc chắn rằng bạn chỉ thêm các tham số này vào cuối dòng đó, cách nhau bởi dấu cách.
	
- **Lưu và khởi động lại**
	
	```bash
	sudo reboot
	```

---