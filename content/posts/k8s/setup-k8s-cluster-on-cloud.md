---
title: Hướng dẫn setup K8S Cluster on Cloud
date: 2026-01-16
image:
categories:
  - cloud
  - k8s
tags:
  - cilium
draft: false
---
Hướng dẫn chi tiết dựng một cluster **on Cloud**. Sử dụng **Containerd** làm Container Runtime (thay thế cho Docker đã cũ).

<!--more-->

---

## Giả định ban đầu

- 3 EC2 instances Ubuntu 22.04 LTS
	
- 1 Master node: `10.0.1.10`
	
- 2 Worker nodes: `10.0.1.20`, `10.0.2.20`
	
- Tất cả trong cùng VPC và Subnet
	
- Security Group đã cấu hình đúng (all traffic giữa các nodes)
	
- SSH access vào tất cả nodes

---

## PHẦN 1: CHUẨN BỊ HỆ THỐNG (Trên tất cả 3 nodes)

### Bước 1.1: Cập nhật hệ thống

```bash
sudo apt-get update && sudo apt-get upgrade -y
```

### Bước 1.2: Set hostname và cập nhật /etc/hosts

**Master node:**

```bash
sudo hostnamectl set-hostname k8s-master
```

**Worker 1:**

```bash
sudo hostnamectl set-hostname k8s-worker-1
```

**Worker 2:**

```bash
sudo hostnamectl set-hostname k8s-worker-2
```

**Trên tất cả 3 nodes, cập nhật /etc/hosts:**

```bash
sudo tee -a /etc/hosts << EOF
10.0.1.10 k8s-master
10.0.1.20 k8s-worker-1
10.0.2.20 k8s-worker-2
EOF
```

**Verify:**

```bash
hostname
ping -c 2 k8s-master
ping -c 2 k8s-worker-1
ping -c 2 k8s-worker-2
```

### Bước 1.3: Tắt Swap

```bash
# Tắt swap ngay lập tức
sudo swapoff -a

# Tắt swap vĩnh viễn (comment dòng swap trong fstab)
sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

# Verify swap đã tắt
free -h
# Dòng Swap phải hiển thị: 0B
```

**Giải thích**:

- Kubernetes yêu cầu swap phải tắt
	
- **Lý do**:
	
    - Swap làm giảm performance của containers
		
    - K8s scheduler dựa vào memory limits để schedule pods
		
    - Nếu swap bật, containers có thể dùng swap → OOM killer không hoạt động đúng
		
    - Pods có thể bị chậm không đoán trước được

### Bước 1.4: Load kernel modules cần thiết

```bash
# Tạo file config để load modules khi boot
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

# Load modules ngay lập tức
sudo modprobe overlay
sudo modprobe br_netfilter

# Verify modules đã được load
lsmod | grep overlay
lsmod | grep br_netfilter
```

**Giải thích từng module**:

**1. overlay module - Hỗ trợ OverlayFS filesystem**
	
- Container runtime (containerd) sử dụng overlay2 storage driver
	
- OverlayFS cho phép layer filesystem của container images
	
- Mỗi container image có nhiều layers (base image, app layer, config layer...)
	
- OverlayFS merge các layers này thành một filesystem duy nhất
	
- Hiệu quả hơn về storage và performance so với copy toàn bộ filesystem

**2. br_netfilter module - Cho phép iptables xem và xử lý traffic đi qua Linux bridge**
	
- **Tại sao cần**:
	
    - K8s sử dụng Linux bridge để connect containers
		
    - Traffic giữa pods phải đi qua bridge
		
    - Iptables rules cần inspect traffic này để:
		
        - Implement network policies
			
        - Load balancing (Services)
			
        - NAT cho traffic ra ngoài cluster
		
    - Nếu không có module này, iptables không thấy traffic qua bridge → network policies không work
	
- **Cụ thể**:
	
    - Pod A (10.244.1.5) → Pod B (10.244.2.8)
		
    - Traffic đi qua cni0 bridge
		
    - `br_netfilter` cho phép iptables rules apply lên traffic này
		
    - VD: NetworkPolicy block Pod A → Pod B sẽ không work nếu không có module này

**Tại sao phải load modules này?**

- Mặc định Ubuntu không load tự động
	
- K8s và CNI (Cilium) cần modules này để hoạt động
	
- Load vào `/etc/modules-load.d/` để tự động load khi reboot

### Bước 1.5: Configure sysctl parameters

```bash
# Tạo file sysctl config cho K8s
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# Apply sysctl params ngay lập tức
sudo sysctl --system

# Verify các settings
sysctl net.bridge.bridge-nf-call-iptables
sysctl net.bridge.bridge-nf-call-ip6tables
sysctl net.ipv4.ip_forward
# Tất cả phải = 1
```

**Giải thích từng parameter**:

**1. net.bridge.bridge-nf-call-iptables = 1**

- **Chức năng**: Cho phép iptables xử lý traffic qua bridge
	
- **Tại sao cần**:
	
    - Khi packets đi qua Linux bridge (cni0), chúng cần được iptables filter
		
    - K8s Services sử dụng iptables rules để load balance
		
    - NetworkPolicies sử dụng iptables để enforce rules
		
    - Nếu = 0, traffic qua bridge sẽ bypass iptables → Services không work
- **Ví dụ cụ thể**:
    
    ```
    Client → Service ClusterIP (10.96.0.100:80)
    ↓
    iptables DNAT rule: 10.96.0.100:80 → Pod IP (10.244.1.5:8080)
    ↓
    Traffic qua bridge cni0
    ↓
    Đến PodNếu net.bridge.bridge-nf-call-iptables = 0 => Traffic qua bridge không đi qua iptables DNAT => Service ClusterIP không work
    ```
    

**2. net.bridge.bridge-nf-call-ip6tables = 1**

- **Chức năng**: Tương tự như trên nhưng cho IPv6
	
- **Tại sao cần**:
	
    - Nếu cluster support dual-stack (IPv4 + IPv6)
		
    - IPv6 traffic cũng cần đi qua ip6tables rules
		
    - Best practice là enable cả hai

**3. net.ipv4.ip_forward = 1**

- **Chức năng**: Enable IP forwarding (routing)
	
- **Tại sao cần**:
	
    - Node phải forward packets giữa các interfaces
		
    - Packets từ Pod A → Pod B trên node khác phải được forward
		
    - Nếu = 0, node chỉ nhận packets destined cho chính nó
	
- **Ví dụ chi tiết**:
    
    ```
    Scenario: Pod trên Worker-1 muốn nói chuyện với Pod trên Worker-2
    
    Worker-1:
    - Pod A (10.244.1.5) gửi packet đến Pod B (10.244.2.8)
    - Packet từ Pod A → cni0 bridge → eth0 → ra ngoài node
    - Nếu ip_forward = 0 => Kernel DROP packet vì destination không phải Worker-1
    - Nếu ip_forward = 1 => Kernel forward packet qua eth0 ra ngoài
      
    Worker-2:
    - Packet đến eth0 → cni0 bridge → Pod B
    - Cũng cần ip_forward = 1 để accept và forward packet
    ```
    

**Tóm lại tại sao cần 3 settings này**:

- **bridge-nf-call-iptables**: Để Services và NetworkPolicies hoạt động
	
- **ip_forward**: Để pods trên các nodes khác nhau có thể communicate
	
- Nếu thiếu bất kỳ setting nào → cluster networking sẽ broken

### Bước 1.6: Disable UFW firewall (nếu có)

```bash
# Check UFW status
sudo ufw status

# Nếu active, disable nó
sudo ufw disable

# Verify
sudo ufw status
# Output: Status: inactive
```

**Giải thích**:

- UFW (Uncomplicated Firewall) là frontend cho iptables trên Ubuntu
	
- K8s và Cilium quản lý iptables rules riêng
	
- UFW có thể conflict với K8s networking rules
	
- **Tại sao disable**:
	
    - K8s tạo hàng trăm iptables rules động
		
    - UFW có thể block những rules này
		
    - Security Group của AWS đã handle security ở network level
	
- **Production**: Nên rely vào Security Group + K8s NetworkPolicies thay vì UFW

---

## PHẦN 2: CÀI ĐẶT CONTAINER RUNTIME (Trên tất cả 3 nodes)

### Bước 2.1: Cài đặt containerd

```bash
# Add Docker's official GPG key
sudo apt-get install -y ca-certificates curl gnupg lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update apt và install containerd
sudo apt-get update
sudo apt-get install -y containerd.io
```

**Giải thích**:

- **containerd**: Container runtime cho K8s (thay thế Docker)
	
- **Tại sao dùng containerd**:
	
    - K8s đã deprecate Docker runtime (dockershim removed từ v1.24)
		
    - containerd là industry standard (CNCF project)
		
    - Nhẹ hơn Docker (không có Docker daemon overhead)
		
    - Native support cho K8s CRI (Container Runtime Interface)
	
- **Docker repository**: containerd được distribute qua Docker repos
	
- **GPG key**: Verify package authenticity để tránh install malicious packages

**Architecture so sánh**:

```
Docker (cũ):
kubelet → dockershim → Docker Engine → containerd → runc → container

Containerd (mới):
kubelet → CRI Plugin → containerd → runc → container

→ Giảm 2 layers, hiệu quả hơn
```

### Bước 2.2: Configure containerd

```bash
# Generate default config
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
```

**Giải thích**:

- `config default`: Generate default configuration
	
- File config ở `/etc/containerd/config.toml` định nghĩa:
	
    - Plugins enabled
		
    - Storage locations
		
    - Registry mirrors
		
    - Runtime options
		
    - Networking config

**Critical: Enable SystemdCgroup**

```bash
# Enable SystemdCgroup trong config
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
```

**Giải thích SystemdCgroup**:

- **Cgroup (Control Group)**: Linux kernel feature để limit resources (CPU, memory, I/O)
    
- **Hai loại cgroup drivers**:
    
    1. **cgroupfs**: Traditional cgroup management
		
    2. **systemd**: Systemd quản lý cgroups
	
- **Tại sao phải dùng systemd cgroup driver**:
    
    - K8s kubelet mặc định dùng systemd cgroup driver
		
    - Containerd phải dùng cùng driver với kubelet
		
    - Nếu mismatch (kubelet dùng systemd, containerd dùng cgroupfs):
	
        - Hai systems quản lý cgroups riêng biệt
			
        - Resource accounting không chính xác
			
        - OOM killer có thể kill sai process
			
        - Pods có thể restart không rõ lý do

**Ví dụ vấn đề khi mismatch**:

```
Scenario: Pod request 100Mi memory

Kubelet (systemd cgroup):
- Tạo cgroup: /sys/fs/cgroup/memory/kubepods/pod123/
- Set limit: 100Mi

Containerd (cgroupfs):
- Tạo cgroup khác: /sys/fs/cgroup/memory/default/pod123/
- Không thấy limit của kubelet
- Container có thể dùng > 100Mi
- Kubelet nghĩ pod đang OOM nhưng thực ra không
```

**Verify config**:

```bash
grep SystemdCgroup /etc/containerd/config.toml
# Output phải là: SystemdCgroup = true
```

### Bước 2.3: Restart và enable containerd

```bash
sudo systemctl restart containerd
sudo systemctl enable containerd

sudo systemctl status containerd
# Phải thấy: active (running)

# Verify containerd hoạt động
sudo ctr version
```

**Troubleshooting nếu containerd failed**:

```bash
# Xem logs
sudo journalctl -u containerd -n 50 --no-pager

# Check config syntax
containerd config dump

# Common issues:
# - Syntax error trong config.toml
# - Conflicting cgroup settings
# - Missing kernel modules
```

---

## PHẦN 3: CÀI ĐẶT KUBERNETES COMPONENTS (Trên tất cả 3 nodes)

### Bước 3.1: Cài đặt kubeadm, kubelet, kubectl

```bash
# Add Kubernetes GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.29/deb/Release.key | \
  sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

# Add Kubernetes repository
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /' | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list

# Update apt và install packages
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl

# Hold packages để prevent auto-upgrade
sudo apt-mark hold kubelet kubeadm kubectl

# Verify installation
kubelet --version
kubeadm version
kubectl version --client
```

### Bước 3.2: Enable kubelet service

```bash
# Enable kubelet để auto-start
sudo systemctl enable kubelet

# Check status (sẽ fail lúc này là bình thường)
sudo systemctl status kubelet
```

**Giải thích**:

- Kubelet sẽ fail/crashloop lúc này vì chưa có cluster
	
- **Tại sao fail**: Kubelet cần config từ kubeadm init
	
- After kubeadm init: kubelet sẽ tự start và work
	
- Enable ngay để nó auto-start sau khi init

---

## PHẦN 4: INITIALIZE KUBERNETES MASTER NODE (Chỉ trên Master)

### Bước 4.1: Pre-flight checks

```bash
# Verify tất cả prerequisites
echo "=== Checking Prerequisites ==="

# 1. Check swap is disabled
echo "Swap status:"
free -h | grep Swap

# 2. Check required ports are available
echo -e "\nChecking required ports:"
sudo netstat -tlnp | grep -E '6443|2379|2380|10250|10251|10252'
# Không nên thấy output gì (ports phải available)

# 3. Check containerd is running
echo -e "\nContainerd status:"
sudo systemctl is-active containerd

# 4. Check kernel modules
echo -e "\nKernel modules:"
lsmod | grep -E 'overlay|br_netfilter'

# 5. Check sysctl settings
echo -e "\nSysctl settings:"
sysctl net.bridge.bridge-nf-call-iptables net.ipv4.ip_forward

# 6. Check hostname resolution
echo -e "\nHostname resolution:"
ping -c 1 k8s-master
ping -c 1 k8s-worker-1
ping -c 1 k8s-worker-2
```

**Giải thích**: Pre-flight checks đảm bảo môi trường ready cho kubeadm init

### Bước 4.2: Initialize cluster với kubeadm

```bash
sudo kubeadm init \
  --pod-network-cidr=10.244.0.0/16 \
  --apiserver-advertise-address=10.0.1.10 \
  --skip-phases=addon/kube-proxy \
  --v=5
```

**Giải thích chi tiết từng parameter**:

**1. --pod-network-cidr=10.244.0.0/16**

- **Chức năng**: Define IP range cho pod network
	
- **Tại sao cần**:
	
    - Mỗi pod cần một unique IP address
		
    - CIDR này chia subnet cho từng node
		
    - CNI plugin (Cilium) sẽ allocate IPs từ range này
	
- **Cách hoạt động**:
    
    ```
    Cluster CIDR: 10.244.0.0/16 (65,536 IPs)
    ↓
    Node 1: 10.244.0.0/24 (256 IPs cho pods trên node này)
    Node 2: 10.244.1.0/24 (256 IPs cho pods trên node này)
    Node 3: 10.244.2.0/24 (256 IPs cho pods trên node này)...
    
    Pod trên Node 1: 10.244.0.5
    Pod trên Node 2: 10.244.1.8
    ```
    
- **Quan trọng**: CIDR này KHÔNG được overlap với:
	
    - VPC CIDR (10.0.0.0/16)
		
    - Service CIDR (default: 10.96.0.0/12)
		
    - Các networks khác
	
- **Tại sao dùng 10.244.0.0/16**:
	
    - Convention phổ biến
		
    - /16 cho phép 256 subnets (/24), mỗi subnet 256 IPs
		
    - Đủ lớn cho hầu hết clusters
	
**2. --apiserver-advertise-address=10.0.1.10**

- **Chức năng**: IP address mà API server listen và advertise
	
- **Tại sao cần specify**:
	
    - Master node có thể có nhiều IPs (public IP, private IP)
		
    - Phải chỉ rõ IP nào dùng cho cluster communication
		
    - Worker nodes sẽ dùng IP này để connect đến API server
	
- **Phải dùng private IP**:
	
    - Cluster communication nên qua private network
		
    - Faster và không bị charge bandwidth
		
    - Secure hơn (không expose API server qua internet)
	
- **Ví dụ**:
    
    ```
    Master node có:
    - Public IP: 54.123.45.67
    - Private IP: 10.0.1.10
    
    Nếu không specify:
    → kubeadm có thể pick public IP→ Workers phải connect qua internet→ Slow và expensive
    
    Với --apiserver-advertise-address=10.0.1.10:
    → Workers connect qua private IP→ Fast và free
    ```
    

**3. --skip-phases=addon/kube-proxy**

- **Chức năng**: Skip cài đặt kube-proxy
	
- **Tại sao skip**:
	
    - Cilium sẽ thay thế kube-proxy
		
    - Cilium implement Service load balancing bằng eBPF
		
    - Hiệu quả hơn kube-proxy (dùng iptables)
	
- **kube-proxy làm gì**:
    
    ```
    Traditional (kube-proxy):
    Client → Service ClusterIP (10.96.0.100:80)
    ↓
    kube-proxy tạo iptables rules:
    DNAT 10.96.0.100:80 
    → Pod1 (10.244.1.5:8080) 33%
    → Pod2 (10.244.2.8:8080) 33%
    → Pod3 (10.244.1.9:8080) 34%
    ↓
    Traffic đến Pod
    
    Với Cilium (eBPF):
    Client → Service ClusterIP
    ↓
    eBPF program trong kernel:
    - Lookup service endpoints
    - Load balance
    - Direct forward đến Pod
    ↓
    Nhanh hơn vì không qua iptables
    ```
    
- **Performance difference**:
	
    - iptables: O(n) với n là số rules
		
    - eBPF: O(1) lookup
		
    - Với 1000+ services, eBPF nhanh hơn rất nhiều

**4. --v=5**

- **Chức năng**: Verbosity level cho logging
	
- **Levels**:
	
    - 0: Errors only
		
    - 1: Warnings
		
    - 2: Info
		
    - 5: Debug (chi tiết hơn)
		
    - 10: Trace (rất chi tiết)
	
- **Tại sao dùng v=5**: Để debug nếu init fail

**Quá trình kubeadm init**:

```
Step 1: [preflight] Pre-flight checks
- Check swap disabled
- Check ports available
- Check containerd running
- Check required images

Step 2: [certs] Generate certificates
- /etc/kubernetes/pki/ca.crt (CA certificate)
- /etc/kubernetes/pki/apiserver.crt (API server cert)
- /etc/kubernetes/pki/etcd/ca.crt (etcd CA)
- ... và nhiều certs khác

Step 3: [kubeconfig] Generate kubeconfig files
- /etc/kubernetes/admin.conf (admin user)
- /etc/kubernetes/kubelet.conf (kubelet)
- /etc/kubernetes/controller-manager.conf
- /etc/kubernetes/scheduler.conf

Step 4: [control-plane] Start control plane components
- Static pods: API server, Controller Manager, Scheduler
- Manifests: /etc/kubernetes/manifests/
  - kube-apiserver.yaml
  - kube-controller-manager.yaml
  - kube-scheduler.yaml
  - etcd.yaml

Step 5: [etcd] Start etcd
- etcd là distributed key-value store
- Store tất cả cluster state

Step 6: [upload-config] Upload kubelet/kubeadm configs
- ConfigMaps chứa cluster configuration

Step 7: [mark-control-plane] Mark master node
- Taint master: node-role.kubernetes.io/control-plane:NoSchedule
- Nghĩa là: Không schedule workload pods lên master

Step 8: [bootstrap-token] Generate join token
- Token để workers join cluster
- Có thời hạn 24h

Step 9: [addons] Install addons
- CoreDNS (DNS server cho cluster)
- Skip kube-proxy (do --skip-phases)
```

**Output quan trọng**:

```
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run:
  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Then you can join any number of worker nodes by running:
kubeadm join 10.0.1.10:6443 --token abc123... \
    --discovery-token-ca-cert-hash sha256:xyz789...
```

**LƯU Ý QUAN TRỌNG**:

- **Save join command** vào file text
	
- Token expires sau 24h
	
- Nếu mất, có thể generate token mới

### Bước 4.3: Setup kubeconfig

```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Verify kubectl hoạt động
kubectl get nodes
```

**Giải thích kubeconfig**:

- **File config**: `~/.kube/config` chứa:
	
    - Cluster information (API server URL, CA cert)
		
    - User credentials (client cert, client key)
		
    - Context (cluster + user + namespace)

**Structure của kubeconfig**:

```yaml
apiVersion: v1
kind: Config
clusters:
- cluster:
    certificate-authority-data: <base64-encoded-ca-cert>
    server: https://10.0.1.10:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
users:
- name: kubernetes-admin
  user:
    client-certificate-data: <base64-encoded-client-cert>
    client-key-data: <base64-encoded-client-key>
```

**Tại sao cần kubeconfig**:

- kubectl cần authenticate với API server
	
- TLS mutual authentication:
	
    - Server cert: kubectl verify server
		
    - Client cert: server verify kubectl
	
- Without kubeconfig: `kubectl get nodes` → connection refused

**Verify kubectl**:

```bash
kubectl get nodes
# Output:
# NAME         STATUS     ROLES           AGE   VERSION
# k8s-master   NotReady   control-plane   1m    v1.34.3

# NotReady là bình thường vì chưa có CNI plugin
```

### Bước 4.4: Verify control plane pods

```bash
# Check control plane pods
kubectl get pods -n kube-system

# Hoặc xem chi tiết hơn
kubectl get pods -n kube-system -o wide

# Check static pod manifests
ls -la /etc/kubernetes/manifests/
```

**Giải thích**:

- Control plane components chạy như **static pods**
	
- **Static pods**: Managed trực tiếp bởi kubelet, không qua API server
	
- Manifests ở `/etc/kubernetes/manifests/`
	
- Kubelet watch directory này và ensure pods luôn chạy

**Expected output**:

```
NAME                                 READY   STATUS    RESTARTS
coredns-xxx                         0/1     Pending   0
etcd-k8s-master                     1/1     Running   0
kube-apiserver-k8s-master           1/1     Running   0
kube-controller-manager-k8s-master  1/1     Running   0
kube-scheduler-k8s-master           1/1     Running   0
```

**Giải thích từng component**:

**1. etcd:**

- Distributed key-value database
	
- Store ALL cluster state:
		
    - Pods, Services, ConfigMaps, Secrets
		
    - Node information
		
    - Cluster configuration
	
- High availability: Có thể chạy multiple etcd instances
	
- Sử dụng Raft consensus algorithm

**2. kube-apiserver:**

- Frontend của control plane
	
- Expose K8s API (REST)
	
- All cluster operations go through API server
	
- Authenticate, authorize, validate requests
	
- Ghi data vào etcd

**3. kube-controller-manager:**

- Chạy các controllers:
	
    - Node Controller: Monitor nodes
		
    - Replication Controller: Ensure đúng số replicas
		
    - Endpoints Controller: Populate Endpoints objects
		
    - Service Account Controller: Tạo default ServiceAccounts
		
    - ... và nhiều controllers khác

**4. kube-scheduler:**

- Watch for new pods không có node assigned
	
- Select node phù hợp nhất cho pod
	
- Factors: Resource requirements, affinity/anti-affinity, taints/tolerations

**5. coredns:**

- DNS server cho cluster
	
- Resolve service names thành ClusterIPs
	
- Status: Pending (chờ CNI plugin)

**Tại sao coredns Pending**:

- CoreDNS pods cần network để start
	
- Chưa có CNI plugin → không có pod network → Pending

---

## PHẦN 5: CÀI ĐẶT CILIUM CNI (Chỉ trên Master)

### Bước 5.1: Download và install Cilium CLI

```bash
# Get latest Cilium CLI version
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)

# Set architecture
CLI_ARCH=amd64

# Download Cilium CLI
curl -L --fail --remote-name-all \
  https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

# Verify checksum
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum

# Extract và install
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin

# Cleanup
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

# Verify
cilium version --client
```

**Giải thích**:

- **Cilium CLI**: Tool để install và manage Cilium
	
- Install vào `/usr/local/bin/` để available globally
	
- Checksum verification để ensure file integrity

### Bước 5.2: Install Cilium vào cluster

```bash
cilium install \
  --version 1.18.5 \
  --set ipam.mode=kubernetes \
  --set routingMode=tunnel \ 
  --set tunnelProtocol=vxlan \
  --set ipv4NativeRoutingCIDR=10.0.0.0/16 \
  --set bpf.masquerade=true \
  --set kubeProxyReplacement=true
```

**Giải thích chi tiết từng parameter**:

**1. --version 1.18.5**

- Specify Cilium version
	
- Version stability và features

**2. --set ipam.mode=kubernetes**

- **IPAM (IP Address Management)**: Cách allocate IPs cho pods
	
- **Modes available**:
	
    - `kubernetes`: K8s allocate IPs (default)
		
    - `cluster-pool`: Cilium manage IP pool
		
    - `eni`: AWS ENI mode
	
- **Mode kubernetes**:
	
    - K8s controller-manager allocate pod CIDR cho mỗi node
		
    - Cilium chỉ assign IPs trong CIDR đó
		
    - Đơn giản và work với mọi cloud provider

**Ví dụ**:

```
Cluster pod-network-cidr: 10.244.0.0/16

K8s allocate:
Node k8s-master:   10.244.0.0/24
Node k8s-worker-1: 10.244.1.0/24
Node k8s-worker-2: 10.244.2.0/24

Cilium trên mỗi node:
- Nhận pod CIDR từ K8s
- Assign IPs cho pods trên node đó
- VD: Pod1 trên worker-1 → 10.244.1.5
```

**3. --set tunnel=vxlan**

- **Tunnel mode**: Cách pods trên các nodes khác nhau communicate
	
- **Options**:
	
    - `disabled`: Native routing (no encapsulation)
		
    - `vxlan`: VXLAN overlay (default)
		
    - `geneve`: Geneve overlay
	
- **VXLAN (Virtual Extensible LAN)**:
	
    - Encapsulate pod traffic trong UDP packets
		
    - Tạo overlay network trên top của existing network

**Cách hoạt động**:

```
Pod A (10.244.1.5) trên Worker-1 → Pod B (10.244.2.8) trên Worker-2

Without VXLAN (native routing):
Pod A → eth0 Worker-1 → AWS VPC routing → eth0 Worker-2 → Pod B
Problem: AWS VPC không biết route 10.244.x.x

With VXLAN:
Pod A → Cilium agent encapsulate trong VXLAN
↓
Original packet: 
  src: 10.244.1.5
  dst: 10.244.2.8
↓
Encapsulated packet:
  Outer header:
    src: 10.0.1.11 (Worker-1 IP)
    dst: 10.0.1.12 (Worker-2 IP)
    UDP port: 8472
  Inner header:
    src: 10.244.1.5
    dst: 10.244.2.8
↓
AWS VPC route bình thường (knows 10.0.1.x)
↓
Worker-2 nhận, Cilium decapsulate
↓
Pod B nhận original packet
```

**Tại sao dùng VXLAN trên AWS**:

- AWS VPC không support custom routing cho pod IPs
	
- VXLAN "hide" pod IPs bên trong node IPs
	
- Alternative: AWS ENI mode (phức tạp hơn, cần IAM permissions)

**4. --set ipv4NativeRoutingCIDR=10.0.0.0/16**

- **Chức năng**: Define CIDR cho native routing (không encapsulate)
	
- **Tại sao cần**:
	
    - Traffic trong VPC CIDR (10.0.0.0/16) không cần encapsulate
		
    - Hiệu quả hơn cho pod-to-node communication
		
    - Node-to-node trong VPC có thể communicate directly

**Ví dụ**:

```
VPC CIDR: 10.0.0.0/16
Pod CIDR: 10.244.0.0/16

Traffic từ Pod (10.244.1.5) → Node (10.0.1.12):
- Destination trong ipv4NativeRoutingCIDR
- Không encapsulate
- Direct routing

Traffic từ Pod (10.244.1.5) → Pod khác (10.244.2.8):
- Destination KHÔNG trong ipv4NativeRoutingCIDR
- Encapsulate với VXLAN
```

**5. --set bpf.masquerade=true**

- **Masquerade (NAT)**: Change source IP khi traffic ra ngoài cluster
	
- **eBPF masquerade**: Implement NAT trong eBPF (fast)

**Tại sao cần**:

```
Scenario: Pod muốn access internet

Pod IP: 10.244.1.5 (private, không routable qua internet)
↓
Cilium eBPF masquerade:
  Change src IP: 10.244.1.5 → 10.0.1.11 (node IP)
↓
Packet ra internet với src = node IP
↓
Response về node IP
↓
Cilium unmasquerade: dst = node IP → 10.244.1.5
↓
Pod nhận response
```

**Traditional (iptables) vs eBPF masquerade**:

```
iptables:
- Rules trong POSTROUTING chain
- O(n) với n là số rules
- Slow với nhiều pods

eBPF:
- Program trong kernel
- O(1) lookup
- Much faster
```

**6. --set kubeProxyReplacement=true**

- **Chức năng**: Cilium thay thế kube-proxy hoàn toàn
	
- **Implementation**: Service load balancing với eBPF

**Traditional kube-proxy**:

```
Client → Service ClusterIP
↓
kube-proxy (iptables rules):
  - 1000s của rules
  - DNAT để forward đến pod
  - Load balance round-robin
↓
Pod
```

**Cilium replacement**:

```
Client → Service ClusterIP
↓
Cilium eBPF program:
  - Hash map lookup (O(1))
  - Load balance (consistent hashing, least connections, ...)
  - Direct forward
↓
Pod

Benefits:
- Faster (no iptables overhead)
- More load balancing algorithms
- Better scalability
- Source IP preservation
```

### Bước 5.3: Wait for Cilium to be ready

```bash
# Wait for Cilium installation
cilium status --wait --wait-duration=5m
```

**Giải thích**:

- `--wait`: Block until Cilium ready
	
- `--wait-duration=5m`: Timeout after 5 minutes
	
- Command check:
	
    - Cilium pods running
		
    - Cilium agents connected
		
    - eBPF programs loaded
	
**Expected output**:

```
    /¯¯\
 /¯¯\__/¯¯\    Cilium:         OK
 \__/¯¯\__/    Operator:       OK
 /¯¯\__/¯¯\    Hubble:         disabled
 \__/¯¯\__/    ClusterMesh:    disabled
    \__/

DaemonSet         cilium             Desired: 3, Ready: 3/3, Available: 3/3
Deployment        cilium-operator    Desired: 2, Ready: 2/2, Available: 2/2
Containers:       cilium             Running: 3
                  cilium-operator    Running: 2
Cluster Pods:     3/3 managed by Cilium
```

### Bước 5.4: Verify Cilium installation

```bash
# Check Cilium pods
kubectl get pods -n kube-system -l k8s-app=cilium -o wide

# Check Cilium DaemonSet
kubectl get ds -n kube-system cilium

# View Cilium status
cilium status

# Check Cilium version
cilium version
```

**Giải thích**:

- **Cilium runs as DaemonSet**: 1 pod trên mỗi node
	
- **Cilium agent**: Manage networking trên node đó
	
- **Cilium operator**: Manage cluster-wide resources

**Architecture**:

```
Master node:
- cilium-xxxxx (agent pod)
- Manage networking cho master
- Load eBPF programs

Worker-1:
- cilium-yyyyy (agent pod)
- Manage networking cho worker-1
- Handle pod connectivity

Worker-2:
- cilium-zzzzz (agent pod)
- Manage networking cho worker-2
- Handle pod connectivity

Cilium Operator (Deployment, 2 replicas):
- Manage CiliumNetworkPolicies
- Garbage collection
- Syncing
```

### Bước 5.5: Verify node status

```bash
# Check nodes - should be Ready now
kubectl get nodes

# Expected output:
# NAME           STATUS   ROLES           AGE   VERSION
# k8s-master     Ready    control-plane   10m   v1.29.x
```

**Giải thích**:

- Sau khi Cilium installed, node chuyển từ NotReady → Ready
	
- **Tại sao**:
	
    - kubelet check network plugin available
		
    - Cilium provide CNI plugin
		
    - Node có thể schedule pods

### Bước 5.6: Verify CoreDNS pods

```bash
# Check CoreDNS - should be Running now
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Expected output:
# NAME                      READY   STATUS    RESTARTS   AGE
# coredns-xxx               1/1     Running   0          10m
# coredns-yyy               1/1     Running   0          10m
```

**Giải thích**:

- CoreDNS pods trước đó Pending (no network)
	
- Sau khi Cilium installed → có network → Running
	
- CoreDNS provide DNS service cho cluster

---

## PHẦN 6: JOIN WORKER NODES (Trên Worker-1 và Worker-2)

### Bước 6.1: Lấy join command từ Master

**Trên Master node:**

```bash
# Generate new join command (nếu mất command từ kubeadm init)
kubeadm token create --print-join-command
```

**Output example**:

```bash
kubeadm join 10.0.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:1234567890abcdef...
```

**Giải thích join command**:

- **10.0.1.10:6443**: API server address (master private IP + API port)
- **--token**: Bootstrap token để authenticate join request
- **--discovery-token-ca-cert-hash**: SHA256 hash của CA cert để verify API server

**Security của join process**:

```
Worker → Master: "Tôi muốn join với token XYZ"
↓
Master verify token
↓
Master gửi CA certificate
↓
Worker verify CA cert hash
↓
Worker trust CA
↓
Mutual TLS established
↓
Worker download cluster info
↓
Worker start kubelet
↓
Worker registered trong cluster
```

**Tại sao cần CA cert hash**:

- Prevent man-in-the-middle attacks
	
- Worker verify đang nói chuyện với đúng master
	
- Without hash: Attacker có thể fake master và steal credentials

### Bước 6.2: Join workers vào cluster

**Trên Worker-1 và Worker-2:**

```bash
# Run join command với sudo
sudo kubeadm join 10.0.1.10:6443 \
  --token abcdef.0123456789abcdef \
  --discovery-token-ca-cert-hash sha256:1234567890abcdef... \
  --v=5
```

**Giải thích quá trình join**:

```
Step 1: [preflight] Pre-flight checks
- Check swap disabled
- Check required ports
- Check containerd running

Step 2: [discovery] Discover cluster info
- Connect to API server
- Verify CA certificate hash
- Download cluster CA certificate

Step 3: [kubelet-start] Configure kubelet
- Generate kubelet.conf with cluster info
- Start kubelet service

Step 4: [kubelet-finalize] Finalize kubelet
- Download cluster config
- Register node với API server

Step 5: Bootstrap TLS
- Generate node certificate
- Submit CertificateSigningRequest (CSR)
- API server auto-approve CSR
- Download signed certificate
```

**Expected output**:

```
[preflight] Running pre-flight checks
[discovery] Downloading cluster info
[kubelet-start] Writing kubelet configuration to file
[kubelet-start] Starting the kubelet
[kubelet-finalize] Updating kubelet configuration
This node has joined the cluster:
* Certificate signing request was sent to apiserver
* Kubelet was informed of the new secure connection details
```

**Troubleshooting nếu join failed**:

```bash
# Common errors:

# 1. Token expired (24h)
# Error: "invalid token"
# Solution: Generate new token trên master

# 2. Cannot connect to API server
# Error: "connection refused"
# Solution: Check Security Group, verify API server running

# 3. CA cert hash mismatch
# Error: "invalid discovery token CA certificate hash"
# Solution: Get correct hash từ master

# 4. Node already joined
# Error: "node already exists"
# Solution: kubeadm reset trước, rồi join lại
```

### Bước 6.3: Verify join success trên Master

**Trên Master node:**

```bash
# Check tất cả nodes
kubectl get nodes

# Expected output:
# NAME           STATUS   ROLES           AGE   VERSION
# k8s-master     Ready    control-plane   20m   v1.34.3
# k8s-worker-1   Ready    <none>          2m    v1.34.3
# k8s-worker-2   Ready    <none>          2m    v1.34.3

# Check với details
kubectl get nodes -o wide
```

**Output với details**:

```
NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP   OS-IMAGE             KERNEL-VERSION
k8s-master     Ready    control-plane   20m   v1.34.3   10.0.1.10     Ubuntu 22.04.3 LTS   5.15.0-xxx
k8s-worker-1   Ready    <none>          2m    v1.34.3   10.0.1.20     Ubuntu 22.04.3 LTS   5.15.0-xxx
k8s-worker-2   Ready    <none>          2m    v1.34.3   10.0.2.20     Ubuntu 22.04.3 LTS   5.15.0-xxx
```

**Giải thích columns**:

- **STATUS**: Ready = node healthy và ready to schedule pods
	
- **ROLES**: control-plane cho master, none cho workers
	
- **INTERNAL-IP**: Private IP dùng cho cluster communication
	
- **VERSION**: K8s version running trên node

### Bước 6.4: Verify Cilium agents trên workers

```bash
# Check Cilium pods trên tất cả nodes
kubectl get pods -n kube-system -l k8s-app=cilium -o wide

# Expected output:
# NAME          READY   STATUS    NODE
# cilium-xxxxx  1/1     Running   k8s-master
# cilium-yyyyy  1/1     Running   k8s-worker-1
# cilium-zzzzz  1/1     Running   k8s-worker-2
```

**Giải thích**:

- Cilium DaemonSet tự động deploy pods lên workers mới
	
- Mỗi worker có 1 Cilium agent pod
	
- Agent manage networking trên node đó

---

## PHẦN 7: VERIFY VÀ TEST CLUSTER (KHÔNG LÀM CŨNG ĐƯỢC)

### Bước 7.1: Verify cluster health

**Trên Master node:**

```bash
# Check component status
kubectl get componentstatuses

# Check all pods trong kube-system
kubectl get pods -n kube-system

# Check all nodes
kubectl get nodes -o wide

# Check Cilium status
cilium status

# Check Cilium connectivity
cilium connectivity test
```

**componentstatuses output**:

```
NAME                 STATUS    MESSAGE
scheduler            Healthy   ok
controller-manager   Healthy   ok
etcd-0               Healthy   {"health":"true"}
```

**Giải thích**:

- Tất cả components phải Healthy
	
- Nếu có Unhealthy: Check logs của component đó

### Bước 7.2: Deploy test nginx application

```bash
# Create nginx deployment
kubectl create deployment nginx --image=nginx --replicas=3

# Verify deployment
kubectl get deployments

# Check pods được schedule
kubectl get pods -o wide

# Expected output:
# NAME                     READY   STATUS    NODE
# nginx-xxx                1/1     Running   k8s-worker-1
# nginx-yyy                1/1     Running   k8s-worker-2
# nginx-zzz                1/1     Running   k8s-worker-1
```

**Giải thích**:

- **replicas=3**: 3 pod instances
	
- Scheduler distribute pods across workers
	
- Pods có IPs từ pod CIDR (10.244.x.x)

### Bước 7.3: Expose nginx service

```bash
# Expose deployment as NodePort service
kubectl expose deployment nginx --port=80 --type=NodePort

# Get service details
kubectl get svc nginx

# Output:
# NAME    TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
# nginx   NodePort   10.96.123.45    <none>        80:32456/TCP   1m
```

**Giải thích Service types**:

- **ClusterIP** (default): Only accessible within cluster
	
- **NodePort**: Accessible via any node IP + NodePort
	
- **LoadBalancer**: Cloud provider load balancer (AWS ELB)

**NodePort hoạt động**:

```
Client → Node IP:NodePort (10.0.1.11:32456)
↓
Cilium eBPF load balance đến một trong 3 nginx pods:
  - nginx-xxx (10.244.1.5:80) 33%
  - nginx-yyy (10.244.2.8:80) 33%
  - nginx-zzz (10.244.1.9:80) 34%
↓
Pod process request
↓
Response về client
```

### Bước 7.4: Test service connectivity

**Test từ trong cluster:**

```bash
# Test với ClusterIP
kubectl run test-pod --image=busybox --rm -it --restart=Never -- \
  wget -O- http://nginx

# Test với service DNS name
kubectl run test-pod --image=busybox --rm -it --restart=Never -- \
  wget -O- http://nginx.default.svc.cluster.local
```

**Giải thích DNS trong K8s**:

- **Service DNS format**: `<service-name>.<namespace>.svc.cluster.local`
	
- **nginx.default.svc.cluster.local**:
	
    - nginx: service name
		
    - default: namespace
		
    - svc.cluster.local: cluster domain
	
- CoreDNS resolve service name → ClusterIP

**Test từ bên ngoài cluster (từ laptop):**

```bash
# Get NodePort
NODEPORT=$(kubectl get svc nginx -o jsonpath='{.spec.ports[0].nodePort}')

# Get worker node public IP
WORKER_IP=$(kubectl get nodes k8s-worker-1 -o jsonpath='{.status.addresses[?(@.type=="ExternalIP")].address}')

# Test với curl
curl http://$WORKER_IP:$NODEPORT

# Expected output: nginx welcome page HTML
```

**Giải thích**:

- Connect đến bất kỳ node IP nào với NodePort
	
- Cilium forward request đến pod (có thể trên node khác)
	
- Response route back qua node nhận request

### Bước 7.5: Test pod-to-pod connectivity

```bash
# Get pod IPs
kubectl get pods -o wide

# Exec vào một pod
POD1=$(kubectl get pods -l app=nginx -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD1 -- /bin/bash

# Trong pod, test connectivity đến pod khác
# Get IP của pod khác
POD2_IP=$(kubectl get pods -l app=nginx -o jsonpath='{.items[1].status.podIP}')

# Ping pod khác
ping -c 3 $POD2_IP

# Curl đến pod khác
curl http://$POD2_IP

# Exit pod
exit
```

**Giải thích**:

- Test direct pod-to-pod connectivity
	
- Verify Cilium overlay network hoạt động
	
- Pods trên different nodes phải communicate được

### Bước 7.6: Test DNS resolution

```bash
# Create test pod
kubectl run dnstest --image=busybox --rm -it --restart=Never -- sh

# Trong pod, test DNS
nslookup kubernetes.default
nslookup nginx.default.svc.cluster.local
nslookup google.com

# Exit
exit
```

**Giải thích**:

- **kubernetes.default**: Built-in service để access API server
	
- **nginx.default.svc.cluster.local**: Service tạo ở bước trước
	
- **google.com**: External DNS (verify outbound connectivity)

**DNS resolution flow**:

```
Pod query: nginx.default.svc.cluster.local
↓
Send DNS query đến CoreDNS (10.96.0.10:53)
↓
CoreDNS lookup service:
  - Check services trong namespace default
  - Find nginx service
  - Return ClusterIP: 10.96.123.45
↓
Pod nhận ClusterIP
↓
Pod connect đến ClusterIP
↓
Cilium eBPF intercept, load balance đến pod
```

### Bước 7.7: Verify Cilium network policies (Optional)

```bash
# Cilium connectivity test (comprehensive)
cilium connectivity test

# Test sẽ:
# - Deploy test pods
# - Test pod-to-pod connectivity
# - Test pod-to-service connectivity
# - Test pod-to-external connectivity
# - Test network policies
# - Clean up test resources

# Mất khoảng 5-10 phút
```

**Giải thích**:

- `cilium connectivity test` là comprehensive test suite
	
- Verify tất cả aspects của cluster networking
	
- Nếu pass: Cluster networking hoàn toàn functional

### Bước 7.8: Check cluster resource usage

```bash
# Check node resources
kubectl top nodes
# Requires metrics-server (optional)

# Check pod resources
kubectl top pods -A

# Describe node
kubectl describe node k8s-worker-1

# Check allocatable resources
kubectl get nodes -o json | \
  jq '.items[] | {name: .metadata.name, capacity: .status.capacity, allocatable: .status.allocatable}'
```

**Giải thích**:

- **Capacity**: Total resources trên node
	
- **Allocatable**: Resources available cho pods (capacity - system reserved)
	
- **top commands**: Requires metrics-server addon

---

## PHẦN 8: CLEANUP VÀ TROUBLESHOOTING

### Bước 8.1: Cleanup test resources

```bash
# Delete nginx deployment và service
kubectl delete deployment nginx
kubectl delete service nginx

# Verify cleanup
kubectl get pods
kubectl get svc
```

### Bước 8.2: Common troubleshooting commands

**Node issues:**

```bash
# Describe node để xem events
kubectl describe node <node-name>

# Check kubelet logs
sudo journalctl -u kubelet -f

# Check kubelet status
sudo systemctl status kubelet

# Restart kubelet nếu cần
sudo systemctl restart kubelet
```

**Pod issues:**

```bash
# Describe pod
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>

# Get previous pod logs (nếu pod restart)
kubectl logs <pod-name> --previous

# Exec vào pod
kubectl exec -it <pod-name> -- /bin/bash
```

**Networking issues:**

```bash
# Check Cilium status
cilium status

# Check Cilium pods
kubectl get pods -n kube-system -l k8s-app=cilium

# Cilium agent logs
kubectl logs -n kube-system <cilium-pod-name>

# Check connectivity
cilium connectivity test

# Verify eBPF maps
cilium bpf endpoint list
```

**DNS issues:**

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system -l k8s-app=kube-dns

# CoreDNS logs
kubectl logs -n kube-system <coredns-pod-name>

# Test DNS từ pod
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup kubernetes.default
```

**Certificate issues:**

```bash
# Check certificate expiration
sudo kubeadm certs check-expiration

# Renew certificates (nếu cần)
sudo kubeadm certs renew all
```

### Bước 8.3: Reset cluster (nếu cần start over)

**Trên tất cả nodes:**

```bash
# Reset kubeadm
sudo kubeadm reset -f

# Clean up
sudo rm -rf /etc/cni/net.d
sudo rm -rf /var/lib/cni/
sudo rm -rf /var/lib/etcd
sudo rm -rf /var/lib/kubelet
sudo rm -rf /etc/kubernetes
sudo rm -rf ~/.kube

# Clean Cilium
sudo rm -rf /var/run/cilium
sudo rm -rf /var/lib/cilium
sudo rm -rf /sys/fs/bpf/cilium

# Delete Cilium interfaces
sudo ip link delete cilium_host 2>/dev/null || true
sudo ip link delete cilium_net 2>/dev/null || true
sudo ip link delete cilium_vxlan 2>/dev/null || true

# Flush iptables
sudo iptables -F && sudo iptables -t nat -F && sudo iptables -t mangle -F && sudo iptables -X

# Restart services
sudo systemctl restart containerd
sudo systemctl restart kubelet

# Reboot (recommended)
sudo reboot
```

**Sau khi reboot, có thể init cluster lại từ đầu**

---

## PHẦN 9: POST-SETUP RECOMMENDATIONS

### Bước 9.1: Label nodes (Optional nhưng recommended)

```bash
# Label workers với role
kubectl label node k8s-worker-1 node-role.kubernetes.io/worker=worker
kubectl label node k8s-worker-2 node-role.kubernetes.io/worker=worker

# Verify
kubectl get nodes

# Output sẽ show roles:
# NAME           ROLES           
# k8s-master     control-plane   
# k8s-worker-1   worker          
# k8s-worker-2   worker          
```

**Giải thích**:

- Labels giúp organize và select nodes
	
- Role labels purely cosmetic nhưng helpful
	
- Có thể dùng trong nodeSelector, affinity rules

### Bước 9.2: Setup kubectl autocompletion (Quality of life)

```bash
# For bash
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc
source ~/.bashrc

# Test
k get nodes  # Should work
```

### Bước 9.3: Install metrics-server (For resource monitoring)

```bash
# Install metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Patch metrics-server để work với self-signed certs
kubectl patch deployment metrics-server -n kube-system --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

# Wait for metrics-server ready
kubectl rollout status deployment metrics-server -n kube-system

# Test
kubectl top nodes
kubectl top pods -A
```

**Giải thích**:

- metrics-server collect resource metrics từ kubelets
	
- Enable `kubectl top` commands
	
- Required cho Horizontal Pod Autoscaler (HPA)

### Bước 9.4: Setup Helm (Package manager for K8s)

```bash
# Download và install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verify
helm version

# Add popular repos
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Bước 9.5: Backup cluster config

```bash
# Backup admin kubeconfig
cp ~/.kube/config ~/kubeconfig-backup-$(date +%Y%m%d).yaml

# Backup etcd (important!)
sudo ETCDCTL_API=3 etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key \
  snapshot save /tmp/etcd-backup-$(date +%Y%m%d).db

# Download backup về laptop
scp ubuntu@<master-ip>:/tmp/etcd-backup-*.db ./
```

---

## TÓM TẮT WORKFLOW

```
1. CHUẨN BỊ (Tất cả nodes)
   - Update system
   - Set hostname và /etc/hosts
   - Tắt swap
   - Load kernel modules
   - Configure sysctl
   - Disable firewall

2. CONTAINER RUNTIME (Tất cả nodes)
   - Install containerd
   - Configure containerd với SystemdCgroup
   - Start containerd

3. K8S COMPONENTS (Tất cả nodes)
   - Install kubeadm, kubelet, kubectl
   - Enable kubelet

4. INIT MASTER (Master only)
   - kubeadm init với proper flags
   - Setup kubeconfig
   - Verify control plane

5. INSTALL CILIUM (Master only)
   - Install Cilium CLI
   - cilium install với proper config
   - Verify Cilium ready
   - Nodes chuyển Ready

1. JOIN WORKERS (Workers only
   - Get join command từ master
   - kubeadm join
   - Verify nodes joined

7. VERIFY CLUSTER
   - Check nodes Ready
   - Deploy test app
   - Test connectivity
   - Test DNS
   - Cilium connectivity test

8. POST-SETUP
   - Label nodes
   - Setup autocompletion
   - Install metrics-server
   - Backup config
```