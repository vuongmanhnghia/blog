---
title: Hướng dẫn setup K8S Cluster on Premise
date: 2025-12-31
image:
categories:
  - linux
  - server
tags:
  - k8s
draft: false
---
Đây là một bài toán thực tế rất thú vị (thường gọi là **Bare-metal Kubernetes**). Khi chuyển từ môi trường ảo hóa (VM) sang 3 thiết bị vật lý thật

<!--more-->

---

Đây là một bài toán thực tế rất thú vị (thường gọi là **Bare-metal Kubernetes**). Khi chuyển từ môi trường ảo hóa (VM) sang 3 thiết bị vật lý thật (ví dụ: 3 chiếc Laptop cũ, hoặc 1 PC + 2 Laptop, hoặc Raspberry Pi) kết nối qua Wi-Fi, thách thức lớn nhất không phải là cài đặt K8s, mà là **Mạng (Networking)**.

Dưới đây là hướng dẫn nâng cao để xử lý các vấn đề đặc thù khi chạy K8s trên Wi-Fi.

---

### THÁCH THỨCC

1.  **IP Động (DHCP):** Wi-Fi thường cấp IP ngẫu nhiên mỗi khi khởi động lại. K8s sẽ "chết" nếu IP của Node thay đổi.
	
2.  **Độ trễ (Latency):** Wi-Fi không ổn định bằng dây LAN. Database của K8s (Etcd) rất nhạy cảm với độ trễ, nếu mạng lag quá, cluster sẽ tự vỡ (crash).
	
3.  **DNS:** Các máy không tự biết tên nhau (ví dụ: máy Master không biết `worker-1` là ai).

---

### QUY HOẠCH MẠNG (Ví dụ)

Giả sử dải mạng Wi-Fi nhà bạn là `192.168.1.x`. Chúng ta sẽ chọn 3 IP cố định (tránh dải DHCP của Router cấp cho điện thoại để khỏi trùng).

*   **Master Node:** `192.168.1.100` (Hostname: `k8s-master`)
	
*   **Worker 1:** `192.168.1.101` (Hostname: `k8s-worker1`)
	
*   **Worker 2:** `192.168.1.102` (Hostname: `k8s-worker2`)

---

### BƯỚC 1: CẤU HÌNH IP TĨNH (QUAN TRỌNG NHẤT)

*Làm trên từng máy tương ứng.*

Trên Ubuntu Server (bản mới), mạng được quản lý bởi **Netplan**.

1.  **Kiểm tra tên card mạng Wi-Fi:**
    ```bash
    ip a
    ```
    Tìm cái tên bắt đầu bằng `w` (ví dụ: `wlan0` hoặc `wlp2s0`). Giả sử là `wlan0`.

2.  **Tạo file cấu hình Netplan:**
    Chúng ta sẽ dùng lệnh `tee` để tạo file config mới.
    *(Lưu ý: Thay thế `SSID-WIFI` và `PASSWORD` bằng thông tin wifi nhà bạn).*

    ```bash
    # Trên máy MASTER (đặt IP .100)
    cat <<EOF | sudo tee /etc/netplan/01-netcfg.yaml
    network:
      version: 2
      renderer: networkd
      wifis:
        wlan0:
          dhcp4: no
          addresses:
            - 192.168.1.100/24
          routes:
            - to: default
              via: 192.168.1.1
          nameservers:
            addresses: [8.8.8.8, 1.1.1.1]
          access-points:
            "TEN_WIFI_NHA_BAN":
              password: "MAT_KHAU_WIFI"
    EOF
    ```
    *(Làm tương tự cho Worker 1 (.101) và Worker 2 (.102) - chỉ sửa dòng `addresses`).*
    
3.  **Apply cấu hình:**
    ```bash
    sudo netplan apply
    ```
    *Nếu mất kết nối SSH, hãy SSH lại vào IP mới.*

---

### BƯỚC 2: ĐỒNG BỘ DANH BẠ (FILE HOSTS)
Vì không có DNS Server nội bộ, ta phải khai báo thủ công để các máy gọi nhau bằng tên.

**Thực hiện trên CẢ 3 MÁY:**

1.  **Đặt Hostname cho đúng chuẩn:**
    ```bash
    # Trên máy Master
    sudo hostnamectl set-hostname k8s-master

    # Trên máy Worker 1
    sudo hostnamectl set-hostname k8s-worker1

    # Trên máy Worker 2
    sudo hostnamectl set-hostname k8s-worker2
    ```

2.  **Sửa file `/etc/hosts`:**
    Dùng `tee -a` để thêm vào cuối file hosts trên **TẤT CẢ CÁC MÁY**:

    ```bash
    cat <<EOF | sudo tee -a /etc/hosts
    192.168.1.100 k8s-master
    192.168.1.101 k8s-worker1
    192.168.1.102 k8s-worker2
    EOF
    ```

---

### BƯỚC 3: CẤU HÌNH TƯỜNG LỬA (FIREWALL)
Các máy vật lý thường bật sẵn tường lửa (UFW). Để đơn giản cho việc học (Lab), ta nên tắt nó đi để tránh việc các Node không ping thấy nhau.

**Trên cả 3 máy:**
```bash
sudo ufw disable
```
*(Nếu bạn muốn bảo mật hơn, hãy comment, mình sẽ đưa list các port cần mở).*

---

### BƯỚC 4: CÀI ĐẶT K8S (NHƯ BÀI TRƯỚC)

Thực hiện lại các bước ở bài trước trên cả 3 máy:

1.  Tắt Swap.
	
2.  Load module kernel (`overlay`, `br_netfilter`).
	
3.  Cài `containerd` (nhớ sửa `SystemdCgroup = true`).
	
4.  Cài `kubeadm`, `kubelet`, `kubectl`.

---

### BƯỚC 5: KHỞI TẠO CLUSTER (TỐI ƯU CHO WI-FI)

Đây là bước nâng cao. Vì Wi-Fi có độ trễ, ta cần cấu hình để K8s "kiên nhẫn" hơn, không đánh dấu Node là chết (NotReady) quá sớm khi mạng lag nhẹ.

**Trên Master Node:**

1.  **Tạo file config cho kubeadm:**
    Thay vì chạy `kubeadm init` ngay, ta tạo file config để tinh chỉnh.

    ```bash
    cat <<EOF | tee kubeadm-config.yaml
    apiVersion: kubeadm.k8s.io/v1beta3
    kind: ClusterConfiguration
    kubernetesVersion: v1.29.0
    controlPlaneEndpoint: "k8s-master:6443"
    networking:
      podSubnet: 192.168.0.0/16
    ---
    apiVersion: kubelet.config.k8s.io/v1beta1
    kind: KubeletConfiguration
    cgroupDriver: systemd
    shutdownGracePeriod: 30s
    shutdownGracePeriodCritical: 10s
    EOF
    ```

2.  **Chạy Init với file config:**
    ```bash
    sudo kubeadm init --config kubeadm-config.yaml
    ```

3.  **Cài đặt Network Plugin (Calico):**
    (Thực hiện như bài trước).

---

### BƯỚC 6: JOIN WORKER VÀ KIỂM TRA

1.  Lấy lệnh join từ Master và chạy trên 2 Worker (như bài trước).
2.  Trên Master, kiểm tra:
    ```bash
    kubectl get nodes -o wide
    ```
    *Lưu ý cột `INTERNAL-IP` phải đúng là 192.168.1.100, .101, .102. Nếu nó hiện IP lạ (ví dụ IP của Docker bridge), cluster sẽ lỗi.*

---

### MẸO NÂNG CAO (PRO TIPS) CHO MÔ HÌNH NÀY

#### 1. Điều khiển Cluster từ Laptop cá nhân (Remote Access)
Bạn không muốn lúc nào cũng phải SSH vào máy Master để gõ lệnh `kubectl`. Bạn muốn gõ lệnh ngay trên Laptop Windows/Mac của mình.

*   **Trên máy Master:**
    Copy nội dung file config:
    ```bash
    cat ~/.kube/config
    ```
*   **Trên Laptop cá nhân:**
    1.  Cài `kubectl` cho Windows/Mac.
    2.  Tạo file `~/.kube/config` và paste nội dung vừa copy vào.
    3.  Mở file đó ra, tìm dòng `server: https://192.168.1.100:6443`. Đảm bảo IP đúng là IP của máy Master (vì đôi khi nó để là 127.0.0.1).
    4.  Giờ bạn có thể ngồi sofa điều khiển cluster.

#### 2. Xử lý lỗi Etcd do Wi-Fi lag
Nếu thấy cluster hay bị mất kết nối, bạn cần tăng thời gian timeout của Etcd.
Sửa file `/etc/kubernetes/manifests/etcd.yaml` trên máy **Master**.
Thêm dòng sau vào phần `command`:
```yaml
    - --heartbeat-interval=500
    - --election-timeout=5000
```
*(Mặc định là 100ms và 1000ms. Tăng lên giúp nó chịu được mạng lag tốt hơn).*

**3. Tiết kiệm băng thông**

Khi bạn deploy một ứng dụng, cả 3 máy sẽ cùng kéo Image từ Internet về qua Wi-Fi. Điều này sẽ làm mạng rất lag.

**Giải pháp:** Kéo image trên 1 máy, sau đó dùng lệnh `ctr` (của containerd) để export image và copy sang các máy kia (hoặc dựng một Local Registry - nhưng cái này để bài sau nhé).