---
title: Kĩ thuật backup dữ liệu Database định kỳ
date: 2025-10-19
image:
categories:
  - database
tags:
  - backup
draft: false
---

Kỹ thuật backup database định kỳ là một kỹ năng cực kỳ quan trọng đối với bất kỳ ai làm DevOps. Một chiến lược backup tốt sẽ giúp bạn cứu sống cả hệ thống khi có sự cố.

<!--more-->

---

## I. Các Nguyên Tắc Vàng

### 1. RPO & RTO
	
- **RPO (Recovery Point Objective):** Lượng dữ liệu tối đa chấp nhận mất. RTO là 1h có nghĩa là nếu hệ thống sập, bạn có thể khôi phục trạng thái của nó cách đây 1h. Hay có thể được gọi là **Tần suất backup**
	
- **RTO (Recovery Time Objective):** Thời gian tối đa để hệ thống hoạt động trở lại sau sự cố. Quyết định **Tốc độ** và **Mức độ** tự động hóa
	
### 2. Backup Types
	
- **Full Backup:** Sao lưu toàn bộ database. Đơn giản để khôi phục nhưng tốn tài nguyên và thời gian
	
- **Differential Backup:** Backup những gì thay đổi của lần **Full Backup** cuối cùng
	
- **Incremential Backup:** Backup những gì thay đổi từ lần backup gần nhất. Tốc độ nhất nhưng cũng phức tạp nhất
	
### 3. Quy Tắc 3-2-1
	
- **3 Bản copies:** Luôn có 3 bản backup dữ liệu
	
- **2 Loại Media:** Lưu trữ trên ít nhất 2 thiết bị lưu trữ khác nhau
	
- **1 Bản off-site:** Giữ ít nhất 1 bản sao ở địa điểm vật lý khác
	
### 4. Bảo mật và Mã hóa
    
-  Luôn mã hóa file backup, cả khi đang truyền đi (in-transit) và khi đã lưu trữ (at-rest).
    
- Quản lý chặt chẽ quyền truy cập vào các file backup.
	
### 5. Quan trọng nhất: KIỂM TRA RESTORE!
    
- Một bản backup chưa được kiểm tra khôi phục thành công thì không được coi là một bản backup.
    
- Hãy lên lịch kiểm tra restore định kỳ (ví dụ: hàng quý) trên một môi trường staging để đảm bảo các file backup của bạn thực sự hoạt động.

---

## II. Kỹ Thuật
### 1. Cron Job & Shell Script
	
- **Bước 1:** Viết Shell Script backup (`backup.sh`)
	
	```bash
	#!/bin/bash
	
	# --- Cấu hình ---
	# Thông tin kết nối Database
	DB_USER="your_db_user"
	DB_PASSWORD="your_db_password"
	DB_HOST="localhost"
	DB_NAME="your_db_name"
	
	# Thư mục lưu trữ backup trên server
	BACKUP_DIR="/path/to/your/backups"
	
	# --- Logic Backup ---
	
	# Tạo thư mục backup nếu chưa tồn tại
	mkdir -p ${BACKUP_DIR}
	
	# Tạo tên file backup với định dạng ngày-tháng-năm
	DATE=$(date +%Y-%m-%d_%H-%M-%S)
	FILE_NAME="${DB_NAME}_${DATE}.sql.gz"
	BACKUP_FILE="${BACKUP_DIR}/${FILE_NAME}"
	
	# Đặt biến môi trường để pg_dump không hỏi mật khẩu
	export PGPASSWORD=${DB_PASSWORD}
	
	# Thực hiện backup bằng pg_dump, nén bằng gzip và lưu vào file
	# -U: user, -h: host, -d: database name
	# | gzip > : pipe output của pg_dump vào gzip để nén
	echo "Dang bat dau backup database: ${DB_NAME}..."
	pg_dump -U ${DB_USER} -h ${DB_HOST} -d ${DB_NAME} | gzip > ${BACKUP_FILE}
	
	# Xóa biến môi trường PGPASSWORD để bảo mật
	unset PGPASSWORD
	
	# Kiểm tra xem backup có thành công không
	if [ $? -eq 0 ]; then
	  echo "Backup thanh cong: ${BACKUP_FILE}"
	else
	  echo "Backup that bai!"
	  exit 1
	fi
	
	# Xóa các file backup cũ hơn 7 ngày
	echo "Xoa cac file backup cu hon 7 ngay..."
	find ${BACKUP_DIR} -type f -name "*.sql.gz" -mtime +7 -delete
	
	echo "Hoan tat."
	```
		
- **Bước 2:** Cấp quyền thực thi cho script
	
	```bash
	chmod +x backup.sh
	```
	
- **Bước 3:** Lên lịch auto run với Cron
	
	Mở crontab để chỉnh sửa
	
	```bash
	crontab -e
	```
	
	Thêm dòng sau vào cuối file để chạy script vào lúc 2 giờ sáng mỗi ngày
	
	```bash
	# Chạy backup vào 2:00 AM hàng ngày 
	0 2 * * * /path/to/your/backup.sh >> /path/to/your/logs/backup.log 2>&1
	```
	
	- **0 2 * * * :** Cú pháp cron cho "0 phút, 2 giờ, mỗi ngày, mỗi tháng, mỗi ngày trong tuần".
	    
	- **>> /path/to/your/logs/backup.log 2>&1:** Ghi lại output (cả standard output và error) vào một file log để bạn có thể kiểm tra lại.
	
### 2. Backup Database trong Docker

**Giả sử bạn có một container PostgreSQL đang chạy tên là `my_postgres_container`**

**Cách 1:** Dùng docker exec và Cron trên máy Host

- Script `backup_docker.sh` sẽ được sửa lại một chút:
	
	```bash
	#!/bin/bash
	
	# --- Cấu hình ---
	CONTAINER_NAME="my_postgres_container"
	DB_USER="your_db_user"
	DB_NAME="your_db_name"
	BACKUP_DIR="/path/on/host/to/backups" # Thư mục trên máy host
	
	# --- Logic Backup ---
	mkdir -p ${BACKUP_DIR}
	
	DATE=$(date +%Y-%m-%d_%H-%M-%S)
	FILE_NAME="${DB_NAME}_${DATE}.sql.gz"
	BACKUP_FILE="${BACKUP_DIR}/${FILE_NAME}"
	
	echo "Dang bat dau backup database từ container: ${CONTAINER_NAME}..."
	
	# Dùng 'docker exec' để chạy pg_dump BÊN TRONG container
	# Output sẽ được chuyển ra máy host và nén lại
	docker exec ${CONTAINER_NAME} pg_dump -U ${DB_USER} -d ${DB_NAME} | gzip > ${BACKUP_FILE}
	
	# ...(Phần kiểm tra và xóa file cũ tương tự như script trước) ...
	# Xóa biến môi trường PGPASSWORD để bảo mật
	unset PGPASSWORD
	
	# Kiểm tra xem backup có thành công không
	if [ $? -eq 0 ]; then
	  echo "Backup thanh cong: ${BACKUP_FILE}"
	else
	  echo "Backup that bai!"
	  exit 1
	fi
	
	# Xóa các file backup cũ hơn 7 ngày
	echo "Xoa cac file backup cu hon 7 ngay..."
	find ${BACKUP_DIR} -type f -name "*.sql.gz" -mtime +7 -delete
	
	echo "Hoan tat."
	```
	
- Sau đó, bạn cũng dùng cron trên **máy host** để chạy script backup_docker.sh này.
	
**Cách 2:** Dùng một **Sidecar Container**
	
- Đây là một pattern nâng cao và rất phổ biến trong **Kubernetes**. Ý tưởng là bạn sẽ chạy một container riêng biệt chỉ để làm nhiệm vụ backup.
	
- Trong `docker-compose.yml` có thể định nghĩa một **service backup**:

```bash
services:
	db:
		image: postgres:13
	    container_name: my_postgres_container
	    environment:
		    - POSTGRES_USER=your_db_user
		    - POSTGRES_PASSWORD=your_db_password
		    - POSTGRES_DB=your_db_name
	    volumes:
		    - postgres_data:/var/lib/postgresql/data

	  # Service này không chạy liên tục, chỉ chạy khi được gọi
	  backup:
		image: postgres:13 # Dùng cùng image để có sẵn pg_dump
	    depends_on:
		    - db
	    volumes:
		    - ./backups:/backups # Gắn thư mục backups của host vào container
	    environment:
		    - PGPASSWORD=your_db_password
	    # Lệnh sẽ chạy khi container này được khởi động
	    command: >
	      bash -c "
	        pg_dump -h db -U your_db_user -d your_db_name | gzip > /backups/backup_$(date +%Y-%m-%d_%H-%M-%S).sql.gz
	      "

volumes:
	  postgres_data:
```

- Chạy backup
	
	```
	docker-compose run --rm backup
	```
	
- Bạn có thể kết hợp lệnh này với cron trên máy host để tự động hóa.

---

## III. Tích hợp với Cloud (DevOps Workflow hoàn chỉnh)

Một quy trình DevOps thực thụ sẽ không dừng lại ở việc lưu file backup trên cùng một server.

**Workflow nâng cao:**

1. **Tạo file backup:** Sử dụng một trong các kỹ thuật trên để tạo file .sql.gz.
    
2. **Tải lên Cloud Storage:** Dùng các công cụ **command-line** của nhà cung cấp cloud để đẩy file backup lên một nơi an toàn.
    
    - **AWS S3:** aws s3 cp /path/to/backup.sql.gz s3://your-backup-bucket/
        
    - **Google Cloud Storage:** gsutil cp /path/to/backup.sql.gz gs://your-backup-bucket/
        
    - **Azure Blob Storage:** az storage blob upload --file /path/to/backup.sql.gz --container-name your-container --name backup.sql.gz
        
3. **Xóa file backup local:** Sau khi đã tải lên cloud thành công, bạn có thể xóa file trên server để tiết kiệm dung lượng.
    
4. **Thiết lập Lifecycle Rules:** Cấu hình trên Cloud Storage để tự động xóa các bản backup cũ (ví dụ: chuyển sang lớp lưu trữ rẻ hơn sau 30 ngày và xóa hẳn sau 90 ngày).
    
5. **Giám sát và Cảnh báo (Monitoring & Alerting):**
    
    - Sử dụng các công cụ như Prometheus, Healthchecks.io, hoặc đơn giản là gửi email/thông báo Slack khi script backup chạy thành công hoặc thất bại.
        
6. **Tự động hóa việc Restore:** Viết script để tự động tải về bản backup mới nhất từ cloud và restore vào một môi trường staging. Chạy script này định kỳ (ví dụ: hàng tuần) để đảm bảo 100% rằng backup của bạn hoạt động.
    

**Ví dụ script tích hợp AWS S3:**

```bash
# ... (Phần tạo backup như trên) ...

# Kiểm tra backup thành công
if [ $? -eq 0 ]; then
  echo "Backup thanh cong: ${BACKUP_FILE}"
  
  # Tải lên S3
  echo "Tai file backup len AWS S3..."
  aws s3 cp ${BACKUP_FILE} s3://your-s3-bucket/database/
  
  if [ $? -eq 0 ]; then
    echo "Tai len S3 thanh cong. Xoa file local."
    rm ${BACKUP_FILE}
  else
    echo "Tai len S3 that bai!"
  fi
  
else
  echo "Backup failed!"
  # Gửi cảnh báo đến Slack/Email ở đây
  exit 1
fi

# ... (Phần xóa backup cũ trên S3 có thể dùng lifecycle rules) ...
```

---