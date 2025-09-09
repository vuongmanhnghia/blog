
version: '3.8'

services:
  # Tên service PostgreSQL
  postgres:
    # Docker image sử dụng - phiên bản cụ thể để đảm bảo tính nhất quán
    image: postgres:15.4-alpine
    
    # Tên container khi chạy
    container_name: postgres_db
    
    # Restart policy - container sẽ tự động restart khi bị lỗi hoặc Docker daemon restart
    restart: unless-stopped
    
    # Biến môi trường cấu hình PostgreSQL
    environment:
      # Tên database mặc định sẽ được tạo
      POSTGRES_DB: myapp_db
      
      # Username cho superuser (mặc định là postgres)
      POSTGRES_USER: postgres
      
      # Password cho superuser (BẮT BUỘC phải set)
      POSTGRES_PASSWORD: your_secure_password_here
      
      # Timezone cho container
      TZ: Asia/Ho_Chi_Minh
      
      # Locale settings
      LC_ALL: C.UTF-8
      POSTGRES_INITDB_ARGS: "--encoding=UTF-8 --lc-collate=C --lc-ctype=C"
    
    # Port mapping: host_port:container_port
    ports:
      - "5432:5432"  # Expose port 5432 ra ngoài host
    
    # Volume mounts để persist data và cấu hình
    volumes:
      # Persist PostgreSQL data
      - postgres_data:/var/lib/postgresql/data
      
      # Custom PostgreSQL config (tùy chọn)
      - ./config/postgresql.conf:/etc/postgresql/postgresql.conf
      
      # Custom pg_hba.conf cho authentication (tùy chọn)
      - ./config/pg_hba.conf:/etc/postgresql/pg_hba.conf
      
      # Thư mục chứa init scripts (tùy chọn)
      - ./init-scripts:/docker-entrypoint-initdb.d
      
      # Thư mục backup (tùy chọn)
      - ./backups:/backups
    
    # Command override (tùy chọn) - sử dụng config file custom
    # command: postgres -c config_file=/etc/postgresql/postgresql.conf
    
    # Networks - nếu muốn tách riêng network
    networks:
      - postgres_network
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2.0'        # Giới hạn 2 CPU cores
          memory: 2G         # Giới hạn 2GB RAM
        reservations:
          cpus: '0.5'        # Đặt trước tối thiểu 0.5 CPU core
          memory: 512M       # Đặt trước tối thiểu 512MB RAM
    
    # Health check để kiểm tra container có hoạt động không
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d myapp_db"]
      interval: 30s          # Kiểm tra mỗi 30 giây
      timeout: 10s           # Timeout sau 10 giây
      retries: 3             # Retry 3 lần trước khi coi là unhealthy
      start_period: 60s      # Đợi 60s trước khi bắt đầu health check
    
    # Logging configuration
    logging:
      driver: "json-file"
      options:
        max-size: "10m"      # Giới hạn kích thước file log
        max-file: "3"        # Giữ tối đa 3 file log

  # Service pgAdmin (tùy chọn) - Web interface để quản lý PostgreSQL
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin4
    restart: unless-stopped
    
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin_password
      PGADMIN_LISTEN_PORT: 80
    
    ports:
      - "8080:80"
    
    volumes:
      - pgadmin_data:/var/lib/pgadmin
    
    networks:
      - postgres_network
    
    # Phụ thuộc vào PostzgreSQL service
    depends_on:
      postgres:
        condition: service_healthy

# Định nghĩa volumes
volumes:
  # Named volume cho PostgreSQL data
  postgres_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ./data/postgres  # Thư mục trên host
  
  # Named volume cho pgAdmin data
  pgadmin_data:
    driver: local

# Định nghĩa networks
networks:
  postgres_network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16