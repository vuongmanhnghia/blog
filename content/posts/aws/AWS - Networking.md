---
title: AWS - Networking
date: 2025-12-16
image:
categories:
  - aws
  - network
  - internet
  - security
tags:
draft: false
---
Hệ thống mạng (Networking) **đầy đủ, bảo mật và chuẩn doanh nghiệp (Enterprise-grade)** trên AWS

<!--more-->

---

### 1. Core Infrastructure
	
*   **VPC (Virtual Private Cloud):** Mạng ảo riêng biệt của bạn trên đám mây AWS. Đây là container chứa tất cả các tài nguyên mạng khác.
	
*   **Subnets (Mạng con):** Chia nhỏ VPC thành các mạng nhỏ hơn. Một kiến trúc chuẩn thường chia làm 3 tầng (3-tier architecture) trên mỗi Availability Zone (AZ):
	
    *   **Public Subnet:** Chứa các resource cần truy cập trực tiếp từ Internet (Load Balancer, Bastion Host, NAT Gateway).
		
    *   **Private Subnet (App):** Chứa các ứng dụng backend. Có thể ra Internet qua NAT nhưng không nhận kết nối trực tiếp từ ngoài vào.
		
    *   **Database/Isolated Subnet:** Chứa Database. Hoàn toàn cô lập, không có đường ra Internet (chỉ nhận kết nối từ App Subnet).
	
*   **CIDR Block:** Dải địa chỉ IP cho VPC và Subnets (VD: `10.0.0.0/16`).

### 2. Internet Connectivity

Để các resource giao tiếp với thế giới bên ngoài:

*   **Internet Gateway (IGW):** Cổng kết nối giúp Public Subnet giao tiếp 2 chiều với Internet.
	
*   **NAT Gateway (Network Address Translation):** Đặt tại Public Subnet. Giúp các instance trong **Private Subnet** đi ra Internet (để tải update, patch) nhưng chặn Internet truy cập ngược vào trong.
	
*   **Egress-only Internet Gateway:** Tương tự NAT Gateway nhưng dành cho **IPv6**.

### 3. Routing & Traffic Management

Điều hướng dòng chảy của dữ liệu:

*   **Route Tables:** Bảng chỉ đường. Mỗi Subnet phải liên kết với một Route Table để biết traffic đi đâu (VD: Traffic `0.0.0.0/0` trỏ về IGW hay NAT Gateway).
	
*   **Elastic Load Balancer (ELB):** Phân phối tải.
	
    *   **ALB (Application Load Balancer):** Layer 7 (HTTP/HTTPS), xử lý routing thông minh dựa trên path, host.
		
    *   **NLB (Network Load Balancer):** Layer 4 (TCP/UDP), hiệu năng cực cao, độ trễ thấp.
	
*   **Route 53:** Dịch vụ DNS của AWS. Dùng để phân giải tên miền và health check.

### 4. Security

*   **Security Groups (SG):** Firewall cấp độ **Instance** (Stateful). Bạn quy định port nào được mở (VD: Chỉ cho phép port 80 từ Load Balancer vào Web Server).
	
*   **Network ACLs (NACLs):** Firewall cấp độ **Subnet** (Stateless). Dùng để chặn (Deny) các IP cụ thể hoặc làm lớp bảo vệ thô.
	
*   **AWS WAF (Web Application Firewall):** Bảo vệ ứng dụng web khỏi các cuộc tấn công phổ biến (SQL Injection, XSS) - thường gắn vào ALB hoặc CloudFront.
	
*   **AWS Network Firewall:** Firewall cao cấp cho toàn bộ VPC, hỗ trợ Deep Packet Inspection (IPS/IDS) và lọc domain.
	
*   **AWS Shield:** Chống tấn công DDoS.

### 5. Private Connectivity

Kết nối các dịch vụ AWS hoặc các VPC với nhau mà không đi qua Internet công cộng:

*   **VPC Endpoints (AWS PrivateLink):**
	
    *   **Interface Endpoint:** Giúp EC2 trong Private Subnet kết nối tới các dịch vụ AWS (như CloudWatch, SNS, Systems Manager) qua mạng nội bộ AWS, không cần NAT Gateway.
		
    *   **Gateway Endpoint:** Dành riêng cho **S3** và **DynamoDB** (miễn phí và hiệu năng cao hơn).
	
*   **VPC Peering:** Kết nối trực tiếp 2 VPC với nhau (như thể chúng cùng 1 mạng).
	
*   **Transit Gateway (TGW):** "Hub" trung tâm để kết nối hàng trăm VPC và mạng On-premise với nhau. Đây là giải pháp thay thế VPC Peering khi hệ thống lớn.

### 6. Hybrid Connectivity

Kết nối AWS với Data Center vật lý hoặc văn phòng:

*   **Site-to-Site VPN:** Kết nối qua đường truyền Internet nhưng được mã hóa (IPsec).
	
*   **AWS Direct Connect (DX):** Đường dây cáp vật lý riêng nối từ Data Center của bạn thẳng đến AWS (băng thông cao, ổn định, bảo mật).
	
*   **Client VPN:** Cho phép nhân viên kết nối từ xa vào VPC (như OpenVPN).

### 7. Monitoring & Observability

Để biết chuyện gì đang xảy ra trong mạng:

*   **VPC Flow Logs:** Ghi lại thông tin về traffic đi vào/ra các network interface (cho biết IP nào đang kết nối, port nào bị chặn...).
	
*   **Traffic Mirroring:** Sao chép traffic mạng để gửi tới các công cụ phân tích bảo mật (IDS) hoặc giám sát chuyên sâu.

---

**p/s:** *Nếu bạn đang viết Terraform, mỗi gạch đầu dòng trên sẽ tương ứng với một `resource` hoặc `module` trong code của bạn.*