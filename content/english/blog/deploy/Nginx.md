---
title: Nginx Overview
date: 2025-08-16
draft: false
tags:
  - deploy
---
Nginx - Từ C10k Đến Containers
<!--more-->

## Phần 1: Nền Tảng Hiệu Năng: "Tại Sao" và "Cái Gì" của Nginx

Phần này thiết lập bối cảnh cơ bản về sự tồn tại và triết lý thiết kế cốt lõi của Nginx. Khám phá vấn đề lịch sử mà Nginx được thiết kế để giải quyết và phân tích các lựa chọn kiến trúc đã biến nó thành một nền tảng của cơ sở hạ tầng web hiện đại.

### 1.1. Nguồn Gốc của Nginx: Giải Quyết Vấn Đề 10,000 Kết Nối

Nginx ra đời không phải là một sự cải tiến gia tăng, mà là một sự thay đổi mô hình trong kiến trúc máy chủ web, một phản ứng trực tiếp trước những hạn chế kiến trúc cơ bản của các máy chủ tiền nhiệm, vốn không còn phù hợp với sự phát triển bùng nổ của Internet.

Vào đầu những năm 2000, khi Internet phát triển với tốc độ chóng mặt, một thách thức kỹ thuật mới đã xuất hiện, được gọi là **vấn đề C10k**. Thuật ngữ này, do kỹ sư Dan Kegel đặt ra vào năm 1999, mô tả bài toán xử lý 10,000 kết nối đồng thời trên một máy chủ duy nhất.1 Vấn đề này không chỉ đơn thuần là về tốc độ xử lý yêu cầu (throughput), mà là về khả năng quản lý hiệu quả một số lượng lớn các kết nối đang mở cùng một lúc. Các máy chủ web phổ biến thời bấy giờ, như Apache, với mô hình xử lý một tiến trình hoặc một luồng cho mỗi kết nối, đã gặp phải giới hạn nghiêm trọng. Mỗi kết nối tiêu tốn một lượng tài nguyên CPU và bộ nhớ đáng kể, tạo ra một rào cản về khả năng mở rộng khi số lượng người dùng tăng vọt.

Trong bối cảnh đó, Igor Sysoev, một kỹ sư hệ thống người Nga làm việc tại Rambler, đã bắt đầu phát triển Nginx vào năm 2002. Ban đầu, ông đã cố gắng cải thiện hiệu suất của Apache thông qua các module như

`mod_accel`, nhưng nhanh chóng nhận ra rằng cần một cách tiếp cận hoàn toàn mới. Nginx không được tạo ra để trở thành "một Apache nhanh hơn", mà là để định nghĩa lại cách một máy chủ web xử lý I/O và quản lý kết nối. Phần mềm được phát hành công khai vào năm 2004 dưới dạng mã nguồn mở miễn phí, theo giấy phép BSD 2 điều khoản.

Thành công của kiến trúc mới này đã được chứng minh nhanh chóng. Đến tháng 9 năm 2008, Nginx đã phục vụ 500 triệu yêu cầu mỗi ngày cho cổng thông tin và công cụ tìm kiếm Rambler. Năm 2011, Nginx, Inc. được thành lập để cung cấp các sản phẩm thương mại và hỗ trợ (NGINX Plus), và sau đó được F5 Networks mua lại vào năm 2019.

### 1.2. Kiến Trúc của Tốc Độ: Hướng Sự Kiện, I/O Bất Đồng Bộ Không Chặn

Chìa khóa cho hiệu suất và khả năng mở rộng vượt trội của Nginx nằm ở kiến trúc **bất đồng bộ, hướng sự kiện và I/O không chặn** (asynchronous, event-driven, non-blocking I/O). Đây là yếu tố cốt lõi giúp Nginx giải quyết vấn đề C10k.

Nginx hoạt động theo mô hình **master-worker**. Một tiến trình

`master` duy nhất chịu trách nhiệm cho các tác vụ quản trị: đọc và xác thực cấu hình, liên kết với các cổng mạng, và tạo ra một số lượng tiến trình `worker` (thường là một worker cho mỗi lõi CPU). Các tiến trình

`worker` này mới là nơi xử lý các yêu cầu của client.

Mỗi tiến trình `worker` là **đơn luồng** (single-threaded) và chạy một **vòng lặp sự kiện** (event loop). Vòng lặp này sử dụng các cơ chế hiệu quả của hệ điều hành như `epoll` (trên Linux) hoặc `kqueue` (trên FreeBSD) để giám sát hàng ngàn kết nối cùng lúc cho các sự kiện (ví dụ: có dữ liệu mới để đọc, bộ đệm sẵn sàng để ghi). Khi một sự kiện xảy ra, một hàm gọi lại (callback) được kích hoạt để xử lý nó. Vì tất cả các hoạt động I/O đều là

**không chặn** (non-blocking), tiến trình worker không bao giờ phải chờ đợi các hoạt động chậm chạp như đọc/ghi đĩa hoặc mạng. Thay vào đó, nó khởi tạo hoạt động và ngay lập tức chuyển sang xử lý các sự kiện khác. Khi hoạt động I/O hoàn tất, hệ điều hành sẽ thông báo cho vòng lặp sự kiện, và kết quả sẽ được xử lý.

Mô hình này mang lại hai lợi ích to lớn. Thứ nhất, nó loại bỏ hoàn toàn chi phí tạo ra một tiến trình hoặc luồng mới cho mỗi kết nối. Thứ hai, nó tránh được việc **chuyển đổi ngữ cảnh** (context switching) tốn kém, một vấn đề lớn của các mô hình truyền thống khi tải cao. Kết quả là Nginx có thể xử lý hàng ngàn kết nối với chi phí bộ nhớ cực thấp (chỉ khoảng 100KB đến 1MB mỗi kết nối) và đạt được thông lượng rất cao, có thể lên tới 100,000 yêu cầu mỗi giây cho mỗi worker.

Kiến trúc master-worker không chỉ mang lại hiệu suất mà còn là nền tảng cho sự ổn định vận hành và các tính năng quan trọng như cập nhật cấu hình không gián đoạn (zero-downtime reloads). Khi cần thay đổi cấu hình, một tín hiệu `reload` được gửi đến tiến trình master. Master sẽ xác thực cấu hình mới và tạo ra một _bộ worker mới_ với cấu hình cập nhật. Các worker cũ sẽ được tắt một cách nhẹ nhàng: chúng ngừng chấp nhận kết nối mới nhưng tiếp tục xử lý các kết nối hiện có cho đến khi hoàn tất. Khi tất cả các kết nối cũ đã đóng, các worker cũ sẽ tự kết thúc. Toàn bộ quá trình này diễn ra mà không làm mất bất kỳ kết nối nào của client, cho phép **cập nhật không thời gian chết**, một yêu cầu tối quan trọng trong các hoạt động DevOps hiện đại.

---

## Phần 2: "Con Dao Đa Năng" của Thụy Sĩ - Các Trường Hợp Sử Dụng Cốt Lõi của Nginx

Từ lý thuyết đến thực tiễn, phần này sẽ trình bày sự linh hoạt của Nginx thông qua các vai trò phổ biến nhất của nó. Mỗi tiểu mục sẽ bao gồm các ví dụ cấu hình được chú thích chi tiết.

### 2.1. Máy Chủ Web Hiệu Năng Cao (cho Nội Dung Tĩnh)

Nhờ kiến trúc hướng sự kiện hiệu quả, Nginx vượt trội trong việc phục vụ nội dung tĩnh như các tệp HTML, CSS, JavaScript và hình ảnh. Trong các bài kiểm tra hiệu năng, Nginx luôn cho thấy hiệu suất cao hơn đáng kể so với Apache trong lĩnh vực này.

Một cấu hình cơ bản để phục vụ một trang web tĩnh rất đơn giản. Khối `server` định nghĩa một máy chủ ảo, chỉ thị `listen` xác định cổng lắng nghe, `server_name` chỉ định tên miền, `root` là đường dẫn đến thư mục chứa tệp của trang web, và `index` xác định tệp mặc định sẽ được phục vụ.

Một mô hình triển khai phổ biến là thiết lập kết hợp, trong đó Nginx đóng vai trò là "người gác cổng" phía trước Apache. Trong mô hình này, Nginx nhận tất cả các yêu cầu, phục vụ trực tiếp các tệp tĩnh với tốc độ tối đa, và chuyển tiếp các yêu cầu nội dung động (như PHP) đến Apache để xử lý.

**Ví dụ cấu hình:**

Nginx

```
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/html;
    index index.html index.htm;

    # Tối ưu hóa việc phục vụ file tĩnh
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 365d; # Yêu cầu trình duyệt lưu cache tài sản tĩnh trong 1 năm
        add_header Cache-Control "public";
    }
}
```

### 2.2. Người Bảo Vệ: Nginx trong vai trò Reverse Proxy

Reverse proxy là một máy chủ trung gian nằm giữa client và các máy chủ backend. Nó nhận yêu cầu từ client và chuyển tiếp chúng đến máy chủ phù hợp. Vai trò này mang lại nhiều lợi ích: che giấu kiến trúc của hệ thống backend, tăng cường bảo mật bằng cách tạo ra một điểm vào duy nhất, có thể chấm dứt SSL/TLS, và là nền tảng cho cân bằng tải và caching.

Chỉ thị cốt lõi cho chức năng này là `proxy_pass`, dùng để chỉ định địa chỉ của máy chủ backend hoặc một nhóm `upstream`. Một yếu tố cực kỳ quan trọng là sử dụng chỉ thị

`proxy_set_header` để chuyển tiếp các thông tin quan trọng của client (như `Host` gốc, `X-Real-IP`, và `X-Forwarded-For`) đến máy chủ backend. Nếu không, máy chủ backend sẽ chỉ thấy địa chỉ IP của proxy, làm mất thông tin về client gốc.

Nginx cũng có cơ chế đệm phản hồi (`proxy_buffering`). Khi được bật (mặc định), Nginx sẽ lưu phản hồi từ máy chủ backend vào bộ đệm và chỉ gửi cho client khi đã nhận đủ. Điều này giúp tối ưu hóa hiệu suất với các client có kết nối chậm, cho phép máy chủ backend xử lý yêu cầu nhanh chóng và giải phóng tài nguyên, trong khi Nginx từ từ gửi dữ liệu về cho client.

**Ví dụ cấu hình:**

Nginx

```
location /app/ {
    proxy_pass http://backend_server:8080;

    # Chuyển tiếp các header quan trọng đến backend
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 2.3. Người Điều Phối Giao Thông: Nginx trong vai trò Load Balancer

Cân bằng tải là một trong những ứng dụng phổ biến nhất của reverse proxy, giúp phân phối lưu lượng truy cập qua nhiều máy chủ backend để cải thiện hiệu suất, khả năng mở rộng và độ tin cậy của hệ thống.

Cấu hình này được thực hiện thông qua khối `upstream`, nơi định nghĩa một nhóm các máy chủ backend. Sau đó, chỉ thị

`proxy_pass` sẽ trỏ đến tên của nhóm `upstream` này. Nginx mã nguồn mở hỗ trợ các thuật toán cân bằng tải sau:

- **Round Robin (Mặc định):** Các yêu cầu được phân phối lần lượt đến từng máy chủ trong nhóm. Có thể sử dụng tham số `weight` để gán trọng số, giúp các máy chủ mạnh hơn nhận được nhiều lưu lượng hơn.
    
- **Least Connections (`least_conn`):** Yêu cầu tiếp theo được gửi đến máy chủ có số lượng kết nối đang hoạt động ít nhất. Thuật toán này rất hiệu quả khi thời gian xử lý các yêu cầu không đồng đều.
    
- **IP Hash (`ip_hash`):** Máy chủ được chọn dựa trên một hàm băm từ địa chỉ IP của client. Điều này đảm bảo rằng các yêu cầu từ cùng một client sẽ luôn được chuyển đến cùng một máy chủ. Đây là một cách đơn giản để thực hiện "sticky sessions" (phiên cố định), rất quan trọng cho các ứng dụng cần duy trì trạng thái phiên.
    

NGINX Plus cung cấp các phương pháp nâng cao hơn như `least_time` và các tính năng duy trì phiên phức tạp hơn như `sticky cookie` và `sticky route`.

**Ví dụ cấu hình:**

Nginx

```
upstream backend_pool {
    # ip_hash; # Bỏ comment để bật sticky sessions
    # least_conn; # Bỏ comment để dùng thuật toán least connections
    server backend1.example.com weight=3;
    server backend2.example.com;
    server backend3.example.com backup; # Chỉ sử dụng khi các server khác lỗi
}

server {
    listen 80;
    location / {
        proxy_pass http://backend_pool;
    }
}
```

### 2.4. Người Gác Cổng: Nginx trong vai trò API Gateway

Trong các kiến trúc microservices hiện đại, API Gateway đóng vai trò là một điểm vào duy nhất cho tất cả các yêu cầu API. Sự phát triển của Nginx thành một API Gateway là một sự mở rộng tự nhiên từ các khả năng cốt lõi của nó như một reverse proxy hiệu năng cao. Một reverse proxy về cơ bản là chặn, kiểm tra và chuyển tiếp yêu cầu. Một API Gateway cũng làm điều tương tự nhưng thêm vào đó các logic phức tạp hơn như định tuyến dựa trên đường dẫn API, xác thực thông tin đăng nhập và thực thi các chính sách sử dụng. Các khối

`location` mạnh mẽ của Nginx cung cấp khả năng định tuyến dựa trên URI, module `limit_req` cung cấp giới hạn tốc độ, và khả năng kiểm tra header cho phép xác thực. Do đó, các khối xây dựng cơ bản cho một API Gateway đã có sẵn trong Nginx.

Các tính năng chính của một API Gateway dựa trên Nginx bao gồm:

- **Định tuyến (Routing):** Chuyển hướng yêu cầu đến microservice backend phù hợp dựa trên URI.
    
- **Xác thực (Authentication):** Xác thực API key hoặc JSON Web Tokens (JWT).
    
- **Giới hạn tốc độ (Rate Limiting):** Áp dụng giới hạn tốc độ để ngăn chặn lạm dụng và đảm bảo sử dụng công bằng.
    
- **Chấm dứt SSL/TLS (SSL/TLS Termination):** Giảm tải việc mã hóa/giải mã từ các dịch vụ backend.
    

Có nhiều cách để triển khai điều này: sử dụng các tính năng gốc của Nginx, mở rộng với Lua/OpenResty, hoặc sử dụng sản phẩm thương mại NGINX Plus API Gateway. Một dự án hiện đại đáng chú ý là NGINX Gateway Fabric, một triển khai của Gateway API dành cho Kubernetes, sử dụng Nginx làm data plane.

### 2.5. Người Tăng Tốc: Caching Nâng Cao với Nginx

Nginx có thể lưu trữ (cache) các phản hồi từ máy chủ backend, giúp cải thiện đáng kể hiệu suất và giảm tải cho máy chủ gốc.

Việc cấu hình `proxy_cache` được thực hiện thông qua các chỉ thị chính sau:

- `proxy_cache_path`: Định nghĩa vị trí lưu trữ cache trên đĩa, vùng bộ nhớ chia sẻ cho các khóa (`keys_zone`), kích thước tối đa (`max_size`), và thời gian không hoạt động (`inactive`).
    
- `proxy_cache`: Kích hoạt một vùng cache cụ thể trong một khối `location` hoặc `server`.
    
- `proxy_cache_valid`: Thiết lập thời gian cache mặc định cho các mã trạng thái HTTP khác nhau (ví dụ: cache phản hồi `200 OK` trong 60 phút, `404 Not Found` trong 1 phút).
    
- `proxy_cache_key`: Định nghĩa chuỗi được sử dụng để tạo khóa duy nhất cho mỗi mục được cache (mặc định là `$scheme$proxy_host$request_uri`).
    

Để gỡ lỗi và theo dõi, việc thêm một header tùy chỉnh (`X-Cache-Status`) với giá trị của biến `$upstream_cache_status` là vô giá. Header này sẽ cho biết một yêu cầu là `HIT` (tìm thấy trong cache), `MISS` (không tìm thấy), `EXPIRED` (hết hạn), `BYPASS` (bỏ qua cache), v.v..

Các khái niệm nâng cao bao gồm việc phục vụ nội dung cũ khi backend gặp sự cố (`proxy_cache_use_stale`) và bỏ qua cache cho các yêu cầu nhất định (`proxy_cache_bypass`).

**Ví dụ cấu hình:**

Nginx

```
# Trong khối http
proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=my_cache:10m max_size=10g inactive=60m;

# Trong khối server
server {
    #...
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_pass http://my_upstream;

        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

---

## Phần 3: Nginx trong Hệ Sinh Thái Hiện Đại - Một Phân Tích So Sánh

Phần này cung cấp một so sánh cân bằng và chi tiết giữa Nginx và các đối thủ chính của nó, giúp các kỹ sư đưa ra quyết định kiến trúc sáng suốt dựa trên yêu cầu dự án cụ thể.

### 3.1. Cuộc Đối Đầu Kinh Điển: Nginx vs. Apache HTTP Server

Sự lựa chọn giữa Nginx và Apache không còn đơn thuần là câu hỏi "cái nào nhanh hơn", mà là sự lựa chọn về triết lý kiến trúc. Nginx ưu tiên hiệu suất thô và hiệu quả thông qua một mô hình tập trung, cứng nhắc, trong khi Apache ưu tiên sự linh hoạt và kiểm soát phân tán, thường phải trả giá bằng hiệu suất.

- **Kiến trúc:** Nginx sử dụng mô hình hướng sự kiện với các worker đơn luồng, trong khi Apache sử dụng mô hình hướng tiến trình/luồng (với các MPM như `prefork`, `worker`, `event`).
    
- **Hiệu năng:** Nginx nhanh hơn đáng kể khi phục vụ nội dung tĩnh và vượt trội dưới tải đồng thời cao do sử dụng ít tài nguyên hơn.12 Apache, với các module động như
    
    `mod_php`, có thể xử lý nội dung động hiệu quả hơn _bên trong chính máy chủ_, mặc dù các thiết lập hiện đại thường sử dụng PHP-FPM, làm cho sự khác biệt này ít rõ rệt hơn.
    
- **Cấu hình:** Nginx sử dụng một tệp cấu hình tập trung. Apache cung cấp cấu hình ở cấp thư mục thông qua các tệp `.htaccess`, mang lại sự linh hoạt cho người dùng trong môi trường hosting chia sẻ nhưng có thể làm giảm hiệu suất vì máy chủ phải quét hệ thống tệp cho các tệp này trên mỗi yêu cầu. Trong các môi trường DevOps hiện đại, nơi cơ sở hạ tầng thường được quản lý tập trung thông qua tự động hóa (IaC), khả năng kiểm soát phân tán của
    
    `.htaccess` có thể trở thành một gánh nặng hơn là một tính năng, làm cho cấu hình tập trung và có thể dự đoán của Nginx trở nên hấp dẫn hơn.
    
- **Modules:** Apache có một hệ sinh thái module động khổng lồ. Các module Nginx truyền thống cần được biên dịch vào tệp nhị phân, mặc dù việc tải module động đã được hỗ trợ từ năm 2016.
    

### 3.2. Chuyên Gia: Nginx vs. HAProxy

- **Nguồn gốc & Trọng tâm:** Nginx bắt đầu như một máy chủ web và phát triển thành một công cụ đa năng. HAProxy được thiết kế từ đầu như một bộ cân bằng tải và reverse proxy hiệu suất cao cho lưu lượng TCP và HTTP.
    
- **Tính năng Layer 7:** Cả hai đều là những bộ cân bằng tải Layer 7 (HTTP) xuất sắc. Nginx có lợi thế là một máy chủ web đầy đủ tính năng, có thể phục vụ trực tiếp các tệp tĩnh, điều mà HAProxy không thể làm.
    
- **Hiệu năng & Chuyên môn hóa:** HAProxy thường được coi là một chuyên gia với hiệu suất vượt trội và các tính năng nâng cao hơn dành riêng cho việc cân bằng tải, chẳng hạn như kiểm tra sức khỏe mạnh mẽ hơn và khả năng quan sát tốt hơn ngay từ đầu trong phiên bản mã nguồn mở của nó.
    
- **Vận hành:** HAProxy được khen ngợi vì khả năng tải lại nóng không gián đoạn (hot reloads) và mô hình vận hành đơn giản hơn cho các thay đổi trực tiếp, trong khi Nginx OSS yêu cầu tải lại hoàn toàn, có thể làm mất kết nối trong giây lát.
    
- **Mô hình phổ biến:** Một kiến trúc mạnh mẽ và phổ biến là sử dụng cả hai: Nginx ở biên (edge) để chấm dứt SSL và phục vụ nội dung tĩnh, sau đó chuyển tiếp lưu lượng đến một HAProxy nội bộ để cân bằng tải phức tạp qua các dịch vụ backend.
    

### 3.3. Thách Thức Mới: Nginx vs. Caddy

Caddy đại diện cho một sự thay đổi triết lý hướng tới "bảo mật mặc định" và trải nghiệm của nhà phát triển. Nó đánh đổi khả năng tùy chỉnh vô hạn của Nginx để lấy các mặc định tự động, hợp lý, bao phủ phần lớn các trường hợp sử dụng, làm cho nó trở thành một sự thay thế hiện đại hấp dẫn.

- **Dễ dàng cấu hình:** Caddy nổi tiếng với tệp cấu hình `Caddyfile` đơn giản, dễ đọc, thường ngắn gọn hơn nhiều so với cấu hình Nginx tương đương.
    
- **HTTPS tự động:** Đây là tính năng "sát thủ" của Caddy. Nó tích hợp sẵn với Let's Encrypt để tự động cấp phát và gia hạn chứng chỉ TLS cho tất cả các trang web được cấu hình, một quá trình đòi hỏi một công cụ riêng biệt như Certbot với Nginx.
    
- **Kiến trúc & Hiệu năng:** Caddy được viết bằng Go và tận dụng mô hình đồng thời của Go. Nó rất hiệu quả, mặc dù Nginx vẫn có thể có lợi thế trong các kịch bản lưu lượng cực cao với các cấu hình được tinh chỉnh kỹ lưỡng.
    
- **Hệ sinh thái:** Nginx có một cộng đồng và hệ sinh thái module lớn hơn và trưởng thành hơn nhiều. Caddy nhỏ hơn nhưng đang phát triển nhanh chóng.
    

### 3.4. Bảng Phân Tích So Sánh

Bảng dưới đây cung cấp một cái nhìn tổng quan, giúp các kỹ sư nhanh chóng so sánh các công cụ dựa trên các tiêu chí DevOps quan trọng.

|Tiêu chí|Nginx|Apache|HAProxy|Caddy|
|---|---|---|---|---|
|**Kiến trúc**|Hướng sự kiện, bất đồng bộ|Hướng tiến trình/luồng|Hướng sự kiện, bất đồng bộ|Hướng sự kiện, bất đồng bộ (Go)|
|**Trường hợp sử dụng chính**|Web server, Reverse Proxy, Cân bằng tải, API Gateway|Web server, Hosting chia sẻ|Cân bằng tải, Reverse Proxy (TCP/HTTP)|Web server, Reverse Proxy|
|**Hiệu năng nội dung tĩnh**|Xuất sắc|Tốt|Không áp dụng|Rất tốt|
|**Mô hình cấu hình**|Tập trung|Phân tán (`.htaccess`)|Tập trung|Tập trung (Caddyfile)|
|**Xử lý SSL/TLS**|Thủ công (cần Certbot)|Thủ công (cần Certbot)|Rất hiệu quả (chấm dứt TLS)|Tự động (tích hợp Let's Encrypt)|
|**Hệ sinh thái & Mở rộng**|Rất lớn, trưởng thành|Lớn nhất, nhiều module động|Chuyên biệt, tập trung|Đang phát triển|
|**Kịch bản lý tưởng**|Hệ thống hiệu năng cao, được quản lý tập trung|Hosting chia sẻ, cần sự linh hoạt ở cấp người dùng|Cân bằng tải chuyên dụng, yêu cầu độ tin cậy cao|Ưu tiên sự đơn giản, HTTPS tự động, trải nghiệm nhà phát triển|

---

## Phần 4: Làm Chủ Cấu Hình Nginx

Phần này đi sâu vào ngôn ngữ cấu hình của Nginx, từ cấu trúc cấp cao đến logic chi tiết điều khiển quá trình xử lý yêu cầu.

### 4.1. Giải Phẫu Tệp `nginx.conf`

Tệp cấu hình chính của Nginx thường nằm ở `/etc/nginx/nginx.conf`. Cấu trúc của nó được tổ chức theo các khối phân cấp được gọi là

**context** (ví dụ: `main`, `events`, `http`, `server`, `location`). Các chỉ thị trong một context cha sẽ được kế thừa bởi các context con nhưng có thể bị ghi đè.

- **`main`/Global:** Định nghĩa các chỉ thị cốt lõi như `user` và `worker_processes`.
    
- **`events`:** Cấu hình các tham số xử lý kết nối, như `worker_connections` (số kết nối tối đa cho mỗi worker).
    
- **`http`:** Chứa các chỉ thị để xử lý lưu lượng HTTP, bao gồm các khối `server` và `upstream`.
    

Một thực hành tốt nhất là sử dụng chỉ thị `include` để mô-đun hóa cấu hình, thường bằng cách bao gồm các tệp từ `/etc/nginx/conf.d/*.conf` và `/etc/nginx/sites-enabled/*`. Mặc dù điều này thúc đẩy sự tổ chức, nó cũng có thể làm cho việc gỡ lỗi trở nên phức tạp nếu không được quản lý cẩn thận. Một chỉ thị trong

`nginx.conf` có thể bị ghi đè bởi một chỉ thị trong `conf.d/global.conf`, và sau đó lại bị ghi đè bởi một chỉ thị trong `sites-enabled/mysite.conf`. Do đó, một kỹ năng quan trọng đối với kỹ sư DevOps là hiểu rõ logic kế thừa và bao gồm này. Các công cụ như `nginx -T` trở nên cần thiết để xem cấu hình được lắp ráp đầy đủ.

### 4.2. Lưu Trữ Nhiều Trang Web: Server Blocks (Virtual Hosts)

Nginx sử dụng các khối `server` để định nghĩa các máy chủ ảo (virtual hosts), cho phép một phiên bản Nginx duy nhất lưu trữ nhiều trang web. Nginx quyết định khối

`server` nào sẽ xử lý một yêu cầu dựa trên các chỉ thị `listen` (IP:port) và `server_name` (tên miền từ header `Host`).

Trên các hệ thống Debian/Ubuntu, quy trình chuẩn là:

1. Tạo một tệp cấu hình cho mỗi trang web trong `/etc/nginx/sites-available/`.
    
2. Tạo một liên kết tượng trưng (symbolic link) từ tệp đó đến `/etc/nginx/sites-enabled/` để kích hoạt trang web. Điều này cho phép bật hoặc tắt các trang web một cách dễ dàng mà không cần xóa tệp cấu hình.
    

### 4.3. Nghệ Thuật Định Tuyến: Logic Khớp Khối Location

Khối `location` được sử dụng để kiểm soát cách xử lý các yêu cầu cho các URI khác nhau trong một máy chủ.36 Việc làm chủ logic khớp của nó là rất quan trọng. Thứ tự xử lý, thường là một nguồn gây nhầm lẫn, như sau:

1. **Khớp chính xác (`=`):** `location = /path` - Nếu URI khớp chính xác, khối này được sử dụng ngay lập tức và việc tìm kiếm dừng lại. Ưu tiên cao nhất.
    
2. **Khớp tiền tố ưu tiên (`^~`):** `location ^~ /path` - Nginx tìm kiếm tiền tố khớp dài nhất. Nếu đây là khớp dài nhất, Nginx sẽ sử dụng nó và _không_ kiểm tra các khối regex. Đây là một cơ chế tối ưu hóa hiệu suất có chủ ý, cho phép quản trị viên bỏ qua các đánh giá regex tốn kém cho các đường dẫn phổ biến.
    
3. **Khớp Regex (`~`, `~*`):** `location ~ \.php$` (phân biệt chữ hoa/thường) hoặc `location ~* \.(jpg|png)$` (không phân biệt). Chúng được kiểm tra theo thứ tự xuất hiện trong tệp cấu hình. Khớp đầu tiên sẽ thắng.
    
4. **Khớp tiền tố dài nhất (không có modifier):** `location /path` - Nếu không có regex nào khớp, tiền tố khớp dài nhất được tìm thấy trước đó sẽ được sử dụng. Ưu tiên thấp nhất.
    

Điều quan trọng cần lưu ý là các khối `location` chỉ khớp với đường dẫn URI, không phải chuỗi truy vấn (query string). Để định tuyến dựa trên tham số truy vấn, có thể sử dụng một giải pháp thay thế bằng câu lệnh

`if` và biến `$args` hoặc `$query_string`.

---

## Phần 5: Nginx trong Thế Giới Container với Docker

Phần này cung cấp hướng dẫn thực tế, từng bước để triển khai và quản lý Nginx trong một môi trường container hiện đại.

### 5.1. Bắt Đầu: Chạy Image Nginx Chính Thức

Bắt đầu với những điều cơ bản về việc sử dụng image Nginx chính thức từ Docker Hub. Một container đơn giản có thể được chạy, ánh xạ cổng với

`-p 8080:80` và mount một thư mục nội dung tĩnh từ máy chủ vào thư mục gốc web mặc định của container (`/usr/share/nginx/html`) bằng cách sử dụng volume mount: `-v /path/on/host:/usr/share/nginx/html:ro`.

### 5.2. Tùy Chỉnh Container Nginx của Bạn

Có ba phương pháp chính để tùy chỉnh container Nginx:

1. **Mount tệp cấu hình tùy chỉnh:** Cách đơn giản nhất là mount tệp `nginx.conf` của riêng bạn hoặc một tệp vào `/etc/nginx/conf.d/` để ghi đè lên các mặc định: `-v /path/to/my.conf:/etc/nginx/conf.d/default.conf:ro`.
    
2. **Xây dựng Image tùy chỉnh với `Dockerfile`:** Đối với các tùy chỉnh phức tạp hơn, có thể tạo một `Dockerfile` bắt đầu bằng `FROM nginx:latest` và sử dụng `COPY` để thêm các tệp cấu hình và nội dung tĩnh trực tiếp vào image. Lệnh
    
    `CMD` cần bao gồm `-g 'daemon off;'` để giữ Nginx chạy ở nền trước, cho phép Docker quản lý tiến trình.
    
3. **Sử dụng biến môi trường và template:** Image Nginx chính thức hỗ trợ một cơ chế templating. Các tệp có đuôi `.template` trong `/etc/nginx/templates/` sẽ được thay thế các biến môi trường (như `${NGINX_HOST}`) trước khi được ghi vào `/etc/nginx/conf.d/`. Đây là một mẫu mạnh mẽ cho cấu hình động trong các đường ống CI/CD.
    

### 5.3. Điều Phối với Docker Compose: Một Ví Dụ Reverse Proxy Thực Tế

Docker Compose là công cụ tiêu chuẩn để định nghĩa và chạy các ứng dụng Docker đa container. Một ví dụ

`docker-compose.yaml` hoàn chỉnh sẽ định nghĩa hai dịch vụ: một ứng dụng backend `node` và một dịch vụ `nginx` hoạt động như một reverse proxy.

Sự kỳ diệu làm cho mô hình reverse proxy Nginx hoạt động liền mạch trong môi trường container chính là mạng Docker. Docker Compose tạo ra một mạng tùy chỉnh cho các dịch vụ được định nghĩa trong tệp. Docker cung cấp một dịch vụ DNS nội bộ trên mạng này. Mỗi container có thể được truy cập bởi các container khác trên cùng một mạng bằng tên dịch vụ của nó (ví dụ:

`node`). Do đó, cấu hình Nginx có thể sử dụng

`proxy_pass http://node:8181;` mà không cần biết địa chỉ IP thực tế của container backend. Điều này cho phép tạo ra một ngăn xếp ứng dụng di động, tự chứa và linh hoạt, có thể được triển khai ở bất cứ đâu có Docker.

**Ví dụ `docker-compose.yaml`:**

YAML

```
version: "3.8"
services:
  node:
    build:
      context:./api
      target: dev
    volumes:
      -./api/index.js:/src/index.js
  nginx:
    restart: always
    image: nginx:1-alpine
    ports:
      - "8089:80"
    volumes:
      -./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - node
```

---

## Phần 6: Bảo Mật Máy Chủ Nginx - Danh Sách Kiểm Tra Cứng Hóa

Phần này cung cấp một danh sách kiểm tra toàn diện các thực hành bảo mật tốt nhất, biến một cài đặt Nginx mặc định thành một máy chủ được cứng hóa, sẵn sàng cho môi trường sản xuất.

### 6.1. Mã Hóa Mọi Thứ: SSL/TLS với Let's Encrypt

HTTPS là điều không thể thiếu cho các ứng dụng web hiện đại. Let's Encrypt cung cấp chứng chỉ TLS miễn phí và đáng tin cậy. Hướng dẫn từng bước sử dụng client

**Certbot** và plugin Nginx của nó (`python3-certbot-nginx`) sẽ được cung cấp. Chạy `certbot --nginx` sẽ tự động lấy và cài đặt chứng chỉ, sửa đổi khối `server` liên quan để bật SSL và thiết lập chuyển hướng từ HTTP sang HTTPS. Việc thiết lập cronjob tự động gia hạn mà Certbot tạo ra là rất quan trọng.

### 6.2. Điều Tiết Lưu Lượng: Giới Hạn Tốc Độ Nâng Cao

Giới hạn tốc độ là một biện pháp phòng thủ quan trọng chống lại các cuộc tấn công brute-force, DDoS và lạm dụng API Nginx sử dụng thuật toán

**leaky bucket** (xô rò rỉ). Cấu hình được thực hiện với hai chỉ thị:

- `limit_req_zone`: Được định nghĩa trong context `http`, nó thiết lập vùng bộ nhớ chia sẻ. Các tham số chính là `key` (ví dụ: `$binary_remote_addr` để giới hạn theo IP), tên và kích thước `zone`, và `rate` (ví dụ: `10r/s`).
    
- `limit_req`: Được sử dụng trong một khối `location` để áp dụng giới hạn của một vùng cụ thể.
    

Các tham số quan trọng `burst` và `nodelay` cũng cần được giải thích. `burst=20` cho phép một loạt 20 yêu cầu được xếp hàng và xử lý theo tốc độ đã định. `nodelay` cho phép loạt yêu cầu đó được xử lý ngay lập tức mà không bị điều tiết, nhưng các yêu cầu tiếp theo sẽ bị từ chối nếu tốc độ vẫn bị vượt quá.

### 6.3. Các Header Bảo Mật Thiết Yếu

Các HTTP Security Header hướng dẫn trình duyệt kích hoạt các tính năng bảo mật, cung cấp một lớp phòng thủ bổ sung. Chúng có thể được triển khai bằng chỉ thị

`add_header`:

- **`Strict-Transport-Security (HSTS)`:** `add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;` - Buộc trình duyệt sử dụng HTTPS.
    
- **`X-Frame-Options`:** `add_header X-Frame-Options "SAMEORIGIN";` - Ngăn chặn clickjacking.
    
- **`X-Content-Type-Options`:** `add_header X-Content-Type-Options "nosniff";` - Ngăn chặn các cuộc tấn công MIME-sniffing.
    
- **`X-XSS-Protection`:** `add_header X-XSS-Protection "1; mode=block";` - Kích hoạt bộ lọc XSS tích hợp của trình duyệt.
    

### 6.4. Lớp WAF: ModSecurity và các Lựa Chọn Thay Thế

Một Tường lửa Ứng dụng Web (WAF) bảo vệ chống lại các cuộc tấn công lớp ứng dụng phổ biến như SQL injection và XSS.

**ModSecurity** từ lâu đã là WAF mã nguồn mở tiêu chuẩn, có sẵn dưới dạng module Nginx.56

Tuy nhiên, một thông tin quan trọng là F5 đã thông báo **Kết thúc vòng đời (End-of-Life) cho module NGINX ModSecurity WAF vào ngày 31 tháng 3 năm 2024**.57 Điều này đánh dấu một bước ngoặt quan trọng trong bối cảnh bảo mật Nginx, buộc cộng đồng phải đánh giá và áp dụng các công nghệ WAF mới hơn.

Các lựa chọn thay thế hiện đại bao gồm:

- **NAXSI (Nginx Anti XSS & SQL Injection):** Một WAF nhẹ, dành riêng cho Nginx, sử dụng hệ thống tính điểm đơn giản thay vì các quy tắc regex phức tạp. Nó nhanh hơn và dễ bảo trì hơn nhưng kém linh hoạt hơn ModSecurity.
    
- **open-appsec:** Một WAF hiện đại dựa trên AI/ML, hoàn toàn tương thích với Nginx. Nó tập trung vào việc phát hiện mối đe dọa một cách chủ động mà không dựa vào các chữ ký truyền thống, làm cho nó trở thành một ứng cử viên sáng giá để thay thế ModSecurity.
    

### 6.5. Danh Sách Kiểm Tra Cứng Hóa Chung

Một danh sách kiểm tra cuối cùng các kỹ thuật cứng hóa thiết yếu bao gồm:

- **Ẩn phiên bản Nginx:** Sử dụng `server_tokens off;` để ngăn rò rỉ thông tin.
    
- **Vô hiệu hóa các phương thức HTTP không cần thiết:** Sử dụng `limit_except GET POST HEAD { deny all; }` để chỉ cho phép các phương thức cần thiết.
    
- **Hạn chế truy cập vào các tệp nhạy cảm:** Sử dụng khối `location` để từ chối truy cập vào các tệp như `.git`, `.env`.
    
- **Ngăn chặn DoS với Timeouts:** Cấu hình thời gian chờ client hợp lý (`client_body_timeout`, `client_header_timeout`) để ngăn chặn các cuộc tấn công kiểu Slowloris.
    
- **Cấu hình bộ mã hóa SSL/TLS mạnh:** Cung cấp một bộ mã hóa hiện đại, an toàn.
    
- **Chạy với người dùng không phải root:** Đảm bảo chỉ thị `user` trong `nginx.conf` được đặt thành một người dùng không có đặc quyền.
    

---

## Phần 7: Vượt Ra Ngoài những Điều Cơ Bản - Mở Rộng Nginx

Phần cuối cùng này sẽ đề cập ngắn gọn đến sức mạnh của hệ sinh thái module của Nginx, cung cấp một ví dụ thực tế về một module của bên thứ ba có giá trị.

### 7.1. Sức Mạnh của Modules: Nén Brotli

Chức năng của Nginx có thể được mở rộng thông qua các module, có thể được biên dịch tĩnh hoặc tải động.

**Brotli** là một thuật toán nén hiện đại do Google phát triển, cung cấp tỷ lệ nén tốt hơn Gzip, giúp trang web tải nhanh hơn.

Module `ngx_brotli` có thể được thêm vào bằng cách biên dịch Nginx từ nguồn hoặc, trên nhiều hệ thống, bằng cách cài đặt một gói module động đã được biên dịch sẵn (ví dụ: `nginx-module-brotli`).

**Ví dụ cấu hình:**

Nginx

```
# Trong context chính (cho module động)
load_module modules/ngx_http_brotli_filter_module.so;
load_module modules/ngx_http_brotli_static_module.so;

# Trong context http, server, hoặc location
brotli on;
brotli_comp_level 6;
brotli_types text/plain text/css application/json...;
brotli_static on; # Phục vụ các tệp.br nếu tồn tại
```

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*