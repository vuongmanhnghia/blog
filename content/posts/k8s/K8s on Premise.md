---
title: Hướng dẫn setup K8S Cluster
date: 2025-12-31
image:
categories:
  - linux
  - server
tags:
  - k8s
draft: false
---

Hướng dẫn chi tiết sử dụng **`kubeadm`** để dựng một cluster trên **Ubuntu (20.04 hoặc 22.04)**. Sử dụng **Containerd** làm Container Runtime (thay thế cho Docker đã cũ).

<!--more-->

---

Hướng dẫn chi tiết sử dụng **`kubeadm`** để dựng một cluster trên **Ubuntu (20.04 hoặc 22.04)**. Sử dụng **Containerd** làm Container Runtime (thay thế cho Docker đã cũ).

## Mô hình Lab
	
*   **1 Master Node** (Control Plane): Điều khiển cluster.
	
*   **2 Worker Nodes**: Nơi chạy các ứng dụng (Pod).
	
*   **Yêu cầu phần cứng:** Tối thiểu 2 CPU, 2GB RAM mỗi node.

---

## PHẦN 1: CẤU HÌNH CHUNG (Thực hiện trên TẤT CẢ các Node)

*Làm các bước này trên cả Master và Worker.*

### Bước 1: Tắt Swap Memory
Kubernetes yêu cầu tắt Swap để hoạt động ổn định.
```bash
sudo swapoff -a
sudo sed -i /swap/d /etc/fstab
```
> **Giải thích:** K8s Scheduler cần biết chính xác lượng RAM khả dụng để phân phối Pod. Nếu dùng Swap (RAM ảo trên ổ cứng), hiệu năng sẽ giảm và K8s không tính toán được tài nguyên thực tế, dẫn đến crash.

### Bước 2: Cấu hình Kernel Module và Network
Load các module cần thiết và cấu hình IP forwarding.
```bash
# Load module overlay và br_netfilter
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

sudo modprobe overlay
sudo modprobe br_netfilter

# Cấu hình sysctl
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

sudo sysctl --system
```
> **Giải thích:**
> *   `br_netfilter`: Cho phép traffic đi qua cầu nối mạng (bridge) được xử lý bởi iptables (tường lửa Linux). Điều này cần thiết để K8s quản lý mạng giữa các Pod.
> *   `ip_forward`: Cho phép Linux chuyển tiếp gói tin IP, biến server thành một router mềm để Pods có thể giao tiếp với bên ngoài.

### Bước 3: Cài đặt Container Runtime (Containerd)
K8s cần một phần mềm để chạy các container. Chúng ta dùng `containerd`.

1.  **Cài đặt containerd:**
    ```bash
    # Cài đặt các gói phụ thuộc
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg

    # Thêm Docker GPG key (Containerd nằm trong repo của Docker)
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    # Thêm repository
    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # Cài đặt containerd
    sudo apt-get update
    sudo apt-get install -y containerd.io
    ```

2.  **Cấu hình Cgroup cho Containerd (RẤT QUAN TRỌNG):**
    ```bash
    # Tạo file config mặc định
    sudo mkdir -p /etc/containerd
    sudo containerd config default | sudo tee /etc/containerd/config.toml

    # Sửa SystemdCgroup = true
    sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/g' /etc/containerd/config.toml

    # Restart containerd
    sudo systemctl restart containerd
    ```
> **Giải thích:**
> *   **Cgroup (Control Group):** Là tính năng Linux để giới hạn tài nguyên (CPU/RAM) cho process.
> *   **Tại sao phải sửa config?** Ubuntu dùng `systemd` để quản lý init system. Nếu Containerd dùng `cgroupfs` (mặc định) còn Kubelet dùng `systemd`, sẽ xảy ra xung đột quản lý tài nguyên. Ta phải ép cả 2 cùng dùng `systemd`.

### Bước 4: Cài đặt kubeadm, kubelet và kubectl

*   `kubeadm`: Tool để dựng cluster.
	
*   `kubelet`: Agent chạy trên mọi node để quản lý container.
	
*   `kubectl`: Tool dòng lệnh để user điều khiển cluster.

```bash
# Cài đặt các gói cần thiết
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# Download public signing key của Kubernetes
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Thêm repository K8s
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

# Cài đặt
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
```
> **Giải thích:** `apt-mark hold` dùng để khóa phiên bản, ngăn không cho lệnh `apt upgrade` tự động nâng cấp K8s, vì việc nâng cấp K8s cần quy trình riêng thủ công để tránh sập hệ thống.

---

## PHẦN 2: KHỞI TẠO MASTER NODE (Chỉ làm trên Master)

### Bước 1: Khởi tạo Cluster
Chạy lệnh sau trên Master Node.

```bash
sudo kubeadm init
```

*Quá trình này mất vài phút. Nó sẽ tải các image của K8s (API Server, Etcd, Scheduler...) về và chạy chúng.*

### Bước 2: Cấu hình kubectl cho user hiện tại
Sau khi lệnh trên chạy xong, nó sẽ hiện ra hướng dẫn. Bạn cần chạy 3 lệnh này để có thể dùng lệnh `kubectl`:

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
> **Giải thích:** `admin.conf` chứa "chìa khóa" (certificate) để truy cập vào API Server với quyền admin cao nhất.

### Bước 3: Cài đặt Network Plugin (CNI)
Cluster đã chạy nhưng các Pod chưa thể nói chuyện với nhau. Ta cần cài CNI. Ở đây dùng **Cilium**.

```bash
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
```

```bash
cilium install \
  --version <latest-version> \
  --set kubeProxyReplacement=true \
  --set k8sServiceHost=<IP control-plane> \
  --set k8sServicePort=6443
```

```bash
# Kiểm tra
cilium status --wait
kubectl get nodes
```

> **Giải thích:**
> *   K8s không tự cung cấp mạng cho Pod, nó chỉ đưa ra chuẩn CNI (Container Network Interface).
> *   Cilium là một plugin thực thi chuẩn đó, giúp tạo ra mạng ảo (Overlay Network) để Pod ở Node A có thể ping thấy Pod ở Node B.

---

## PHẦN 3: JOIN WORKER NODES (Làm trên các Worker)

### Bước 1: Lấy lệnh Join
Khi chạy `kubeadm init` ở Phần 2 xong, dòng cuối cùng của output sẽ là lệnh join. Nếu lỡ quên hoặc xóa mất, hãy chạy lệnh này trên **Master** để lấy lại:

```bash
kubeadm token create --print-join-command
```

### Bước 2: Thực thi trên Worker
Copy lệnh output ở trên và dán vào terminal của các máy **Worker Node**. Ví dụ:

```bash
sudo kubeadm join <MASTER_IP>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash>
```

> **Giải thích:**
> *   Lệnh này giúp Worker Node xác thực với Master Node thông qua Token.
> *   Sau khi xác thực, Kubelet trên Worker sẽ nhận chỉ đạo từ Master.

---

## PHẦN 4: KIỂM TRA (Verify)

Quay lại **Master Node**, chạy lệnh:

```bash
kubectl get nodes
```

**Kết quả mong đợi:**
```text
NAME       STATUS   ROLES           AGE     VERSION
master     Ready    control-plane   10m     v1.29.0
worker-1   Ready    <none>          2m      v1.29.0
worker-2   Ready    <none>          2m      v1.29.0
```

*   Nếu trạng thái là `NotReady`: Chờ khoảng 1-2 phút để CNI khởi động xong.
*   Nếu vẫn `NotReady`: Kiểm tra lại bước tắt Swap hoặc file config của containerd.

## Tổng kết kiến trúc:
1.  **OS Layer:** Ubuntu + Tắt Swap + IP Forwarding.
	
2.  **Runtime Layer:** Containerd (quản lý container).
	
3.  **K8s Layer:** Kubelet (giao tiếp với Master), Kube-proxy (quản lý mạng).
	
4.  **Network Layer:** Cilium (kết nối các Pod).

## BÀI VIẾT LIÊN QUAN

- [Hướng dẫn setup K8S Cluster Bare-metal](setup-k8s-cluster-bare-metal) 