---
title: Hướng dẫn backup database postgres trong container và sử dụng trong server mới
date: 2025-11-21
image:
categories:
  - backup
  - database
tags:
  - postgres
draft: false
---

<!--more-->

---

## Bước 1: Backup Database tại Server cũ

Sử dụng `pg_dump`

```bash
docker exec -t my_postgres_container pg_dumpall -c -U postgres > ~/backup/my_db_backup.sql
```
	
- `pg_dumpall`: Lệnh backup toàn bộ các database có trong đó.
    
- `-c`: Thêm lệnh DROP DATABASE trước khi tạo lại (giúp làm sạch khi restore).
    
- `-U postgres`: Dùng user postgres để thực hiện.

---
## Bước 2: Di chuyển `my_db_backup.sql` sang Server mới

Có thể kéo trực tiếp từ server cũ sang server mới hoặc kéo về máy cá nhân sau đó đẩy lên server mới

---
## Bước 3: Restore tại Server mới

```bash
cat my_db_backup.sql | doker exec -i my_postgres_container -U postgres -d my_db
```