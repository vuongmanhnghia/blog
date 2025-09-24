---
title: Internet Protocol (IP)
date: 2025-08-13
image: /images/image-placeholder.png
categories:
  - devops
tags:
  - docker
draft: true
---

Mastering Internet Protocol Addresses

<!--more-->

Đối với một người dùng Linux, dù bạn là nhà phát triển, quản trị viên hệ thống hay chỉ là một người đam mê công nghệ, việc hiểu sâu và làm chủ địa chỉ IP không chỉ là một kỹ năng hữu ích mà còn là một yêu cầu thiết yếu.

Bài viết này sẽ là kim chỉ nam của bạn, dẫn dắt bạn đi từ những khái niệm cơ bản nhất như "Địa chỉ IP là gì?" đến các kỹ thuật nâng cao như cấu hình mạng, quét tìm thiết bị và thiết lập kết nối từ xa an toàn. Chúng ta sẽ cùng nhau "mổ xẻ" các lệnh, khám phá các công cụ và áp dụng chúng vào những kịch bản thực tế, giúp bạn tự tin điều hướng trong không gian mạng rộng lớn bằng sức mạnh của dòng lệnh Linux.

## Phần 1: Giải Phẫu Địa Chỉ IP

Trước khi đi sâu vào các câu lệnh và cấu hình, việc xây dựng một nền tảng kiến thức vững chắc về bản chất của địa chỉ IP là vô cùng quan trọng. Phần này sẽ giải mã các khái niệm cốt lõi, giúp bạn hiểu rõ "tại sao" và "như thế nào" trước khi học "làm gì".

### 1.1. Địa chỉ IP là gì? Hơn Cả những Con Số

**Vai trò Cốt lõi: "Địa chỉ Nhà Kỹ thuật số" của Thiết bị**

Về cơ bản, địa chỉ Giao thức Internet (Internet Protocol address), hay địa chỉ IP, là một định danh số duy nhất được gán cho mỗi thiết bị điện tử (như máy tính, điện thoại, máy chủ) khi tham gia vào một mạng máy tính sử dụng Giao thức Internet để giao tiếp. Hãy hình dung nó như một địa chỉ nhà trong thế giới thực; để một lá thư (dữ liệu) có thể được gửi đến đúng người nhận (thiết bị), nó cần một địa chỉ chính xác. Mục đích chính của địa chỉ IP là để nhận diện thiết bị và xác định vị trí của nó trên mạng, từ đó cho phép việc truyền và nhận dữ liệu diễn ra một cách chính xác.

Mọi dữ liệu di chuyển trên mạng đều được chia thành các đơn vị nhỏ hơn gọi là "gói tin" (packets). Mỗi gói tin này không chỉ chứa một phần dữ liệu mà còn mang theo một phần "tiêu đề" (header). Trong tiêu đề này, thông tin quan trọng nhất chính là địa chỉ IP của người gửi (nguồn) và địa chỉ IP của người nhận (đích). Cấu trúc này đảm bảo rằng dù các gói tin có thể đi theo những con đường khác nhau qua Internet, chúng vẫn sẽ đến được đúng đích và được tập hợp lại một cách chính xác.

Tuy nhiên, việc ví IP như một "địa chỉ nhà" chỉ là bước khởi đầu. Một sự tương đồng chính xác hơn cho người dùng kỹ thuật là: **địa chỉ IP giống như địa chỉ của _vị trí_ bạn đang kết nối mạng, trong khi địa chỉ MAC (Media Access Control) mới thực sự là số sê-ri định danh duy nhất của _thiết bị_ đó.** Địa chỉ MAC là một địa chỉ vật lý, được gán cứng vào card mạng của bạn bởi nhà sản xuất và không thay đổi. Ngược lại, địa chỉ IP của bạn có thể thay đổi. Khi bạn mang laptop từ nhà (kết nối vào mạng Wi-Fi gia đình) đến một quán cà phê (kết nối vào mạng Wi-Fi của quán), địa chỉ MAC của laptop vẫn giữ nguyên, nhưng nó sẽ được cấp một địa chỉ IP mới tương ứng với mạng của quán cà phê. Việc phân biệt rõ ràng giữa định danh thiết bị (MAC, Lớp 2) và định danh vị trí mạng (IP, Lớp 3) là chìa khóa để hiểu các khái niệm như DHCP, tính di động của mạng và cách các lớp khác nhau trong mô hình mạng tương tác với nhau.

**Cỗ máy Vận hành: Giao thức IP và Vị trí trong Chồng Giao thức TCP/IP**

Địa chỉ IP không tồn tại một mình; nó là một phần không thể tách rời của bộ giao thức TCP/IP, bộ khung xương sống của Internet hiện đại. TCP/IP là một mô hình phân tầng, trong đó Giao thức IP hoạt động ở Tầng Mạng (Network Layer), hay còn gọi là Tầng Internet, tương ứng với Lớp 3 trong mô hình tham chiếu OSI (Open Systems Interconnection).

Trong bộ đôi này, mỗi giao thức có một nhiệm vụ riêng biệt:

-   **IP (Internet Protocol):** Chịu trách nhiệm về việc **định địa chỉ và định tuyến**. Nó gắn địa chỉ IP vào các gói tin và quyết định con đường mà các gói tin đó sẽ đi qua mạng để đến đích. IP hoạt động theo nguyên tắc "nỗ lực tốt nhất" (best-effort), nghĩa là nó không đảm bảo các gói tin sẽ đến nơi, đến đúng thứ tự, hay không bị lỗi.
-   **TCP (Transmission Control Protocol):** Hoạt động ở tầng trên (Tầng Giao vận - Transport Layer), TCP bổ sung cho sự thiếu tin cậy của IP. Nó thiết lập một kết nối ổn định, đảm bảo rằng tất cả các gói tin đều đến đích một cách toàn vẹn và theo đúng thứ tự. Nếu một gói tin bị mất, TCP sẽ yêu cầu gửi lại.

Sự kết hợp giữa một hệ thống địa chỉ và định tuyến toàn cầu (IP) và một cơ chế đảm bảo truyền tải đáng tin cậy (TCP) chính là thứ đã tạo nên một Internet mạnh mẽ và linh hoạt như ngày nay.

**Hành trình của một Gói tin: Cách Dữ liệu Di chuyển trên Internet**

Hãy xem xét một hành động quen thuộc: bạn gõ `google.com` vào trình duyệt. Đây là những gì xảy ra đằng sau hậu trường:

1. **Phân giải DNS:** Máy tính của bạn không biết `google.com` ở đâu. Nó gửi một yêu cầu đến một Máy chủ Tên miền (DNS - Domain Name System) để hỏi: "Địa chỉ IP của `google.com` là gì?". Máy chủ DNS sẽ trả lời bằng một địa chỉ IP, ví dụ `172.217.24.238`.
2. **Đóng gói và Gửi đi:** Trình duyệt của bạn tạo một yêu cầu (ví dụ: HTTP GET) và chuyển nó xuống các tầng thấp hơn của mô hình TCP/IP. Dữ liệu được chia thành các gói tin, mỗi gói được gắn tiêu đề chứa IP nguồn (máy của bạn) và IP đích (máy chủ Google).
3. **Chặng đầu tiên:** Gói tin được gửi từ máy tính của bạn đến thiết bị mạng gần nhất, thường là bộ định tuyến (router) Wi-Fi ở nhà hoặc văn phòng của bạn.
4. **Định tuyến qua các Chặng:** Khi router nhận được gói tin, nó sẽ nhìn vào địa chỉ IP đích. Dựa trên thông tin trong **bảng chuyển tiếp** (forwarding table) của mình, nó sẽ quyết định "chặng kế tiếp" (next hop) tốt nhất để gửi gói tin đi—tức là một router khác gần với đích đến hơn. Bảng chuyển tiếp này không chứa mọi địa chỉ IP trên thế giới, mà chỉ chứa các đường dẫn đến các mạng lớn, được cập nhật liên tục thông qua các giao thức định tuyến như OSPF hay BGP.
5. **Lặp lại và Đến đích:** Quá trình này lặp đi lặp lại. Gói tin của bạn nhảy từ router này sang router khác, qua nhiều nhà cung cấp dịch vụ Internet, thậm chí qua các quốc gia khác nhau, cho đến khi nó đến được router cuối cùng kết nối trực tiếp với máy chủ của Google. Máy chủ này sau đó sẽ xử lý yêu cầu và gửi các gói tin phản hồi trở lại máy của bạn theo một quy trình tương tự.

### 1.2. "Bản đồ" Địa chỉ IP: Điều hướng trong Không gian Mạng

Không phải tất cả các địa chỉ IP đều được tạo ra như nhau. Chúng được phân loại dựa trên phạm vi và cách thức cấp phát để phục vụ các mục đích khác nhau.

**IP Công cộng (Public) vs. IP Riêng (Private): Cổng ra Internet và Mạng Nội bộ**

Đây là sự phân chia cơ bản nhất về phạm vi của địa chỉ IP.

-   **IP Riêng (Private IP):** Đây là các địa chỉ được sử dụng **bên trong một mạng cục bộ (LAN)**, chẳng hạn như mạng gia đình, văn phòng, hoặc trường học. Chúng không thể được truy cập trực tiếp từ Internet. Điều này cho phép hàng triệu mạng riêng trên khắp thế giới có thể sử dụng lại cùng một bộ địa chỉ mà không bị xung đột. Các dải địa chỉ IP riêng đã được tiêu chuẩn hóa và dành riêng cho mục đích này 3:
    -   Lớp A: `10.0.0.0` đến `10.255.255.255` (tiền tố `10.0.0.0/8`)
    -   Lớp B: `172.16.0.0` đến `172.31.255.255` (tiền tố `172.16.0.0/12`)
    -   Lớp C: `192.168.0.0` đến `192.168.255.255` (tiền tố `192.168.0.0/16`)
-   **IP Công cộng (Public IP):** Đây là địa chỉ **duy nhất trên toàn cầu**, được cấp phát bởi Nhà cung cấp dịch vụ Internet (ISP) của bạn. Đây chính là địa chỉ mà thế giới bên ngoài nhìn thấy khi bạn kết nối với Internet. Mọi trang web, máy chủ email, hoặc dịch vụ trực tuyến mà bạn truy cập đều có một địa chỉ IP công cộng.
-   **NAT (Network Address Translation):** Vậy làm thế nào mà hàng tỷ thiết bị với IP riêng có thể truy cập Internet chỉ với một số lượng hạn chế IP công cộng? Câu trả lời là NAT. Router của bạn đóng vai trò như một "phiên dịch viên". Khi một thiết bị trong mạng LAN của bạn (với IP riêng) muốn gửi dữ liệu ra Internet, router sẽ thay thế địa chỉ IP riêng trong gói tin bằng địa chỉ IP công cộng duy nhất của nó. Khi nhận được phản hồi, nó sẽ dịch ngược lại và gửi đến đúng thiết bị trong mạng LAN. NAT không chỉ giúp tiết kiệm địa chỉ IP công cộng mà còn tăng cường bảo mật bằng cách che giấu cấu trúc mạng nội bộ của bạn khỏi thế giới bên ngoài.

**Bảng 1: So sánh IP Công cộng và IP Riêng**

| Tiêu chí              | IP Công cộng (Public)                                                         | IP Riêng (Private)                                                             |
| --------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| **Phạm vi**           | Duy nhất trên toàn cầu, có thể định tuyến trên Internet.                      | Cục bộ, chỉ có ý nghĩa trong một mạng LAN, không thể định tuyến trên Internet. |
| **Cấp phát**          | Được cấp bởi Nhà cung cấp dịch vụ Internet (ISP) và các tổ chức quản lý mạng. | Được cấp bởi router (thông qua DHCP) hoặc quản trị viên mạng.                  |
| **Chi phí**           | Có phí, là một phần của gói dịch vụ Internet.                                 | Miễn phí, có thể sử dụng tự do trong các dải quy định.                         |
| **Khả năng truy cập** | Có thể được truy cập từ bất kỳ đâu trên Internet.                             | Chỉ có thể được truy cập bởi các thiết bị khác trong cùng mạng LAN.            |
| **Mục đích sử dụng**  | Cho phép các thiết bị kết nối và giao tiếp với Internet.                      | Cho phép các thiết bị trong một mạng nội bộ giao tiếp với nhau.                |

**IP Tĩnh (Static) vs. IP Động (Dynamic): Vĩnh viễn và Tạm thời**

Đây là sự phân loại dựa trên cách thức một địa chỉ IP được gán cho một thiết bị.

-   **IP Động (Dynamic IP):** Đây là phương pháp phổ biến nhất. Địa chỉ IP được cấp phát **tự động và tạm thời** cho một thiết bị khi nó kết nối vào mạng. Công việc này thường được thực hiện bởi một máy chủ DHCP (Dynamic Host Configuration Protocol), thường được tích hợp sẵn trong router của bạn. Khi bạn ngắt kết nối, địa chỉ IP đó sẽ được "trả lại" vào một "kho" chung để có thể cấp phát cho một thiết bị khác. Điều này giúp quản lý địa chỉ hiệu quả và dễ dàng.
-   **IP Tĩnh (Static IP):** Ngược lại với IP động, IP tĩnh được **cấu hình thủ công và gán cố định** cho một thiết bị. Nó sẽ không bao giờ thay đổi trừ khi quản trị viên mạng thay đổi nó. IP tĩnh rất quan trọng cho các thiết bị cần được truy cập một cách nhất quán từ xa, ví dụ như:
    -   Máy chủ Web, Email, Game: Để người dùng và các dịch vụ khác luôn biết cách tìm đến.
    -   Máy chủ VPN: Để nhân viên có thể kết nối từ xa vào mạng công ty.
    -   Camera an ninh, máy in mạng: Để các thiết bị khác trong mạng luôn có thể kết nối đến chúng một cách đáng tin cậy.

**Bảng 2: So sánh IP Tĩnh và IP Động**

| Tiêu chí               | IP Tĩnh (Static)                                                                             | IP Động (Dynamic)                                                                   |
| ---------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Cấp phát**           | Thủ công, được quản trị viên gán cố định cho một thiết bị.                                   | Tự động, được cấp phát tạm thời bởi máy chủ DHCP.                                   |
| **Độ ổn định**         | Cố định, không thay đổi theo thời gian. Rất đáng tin cậy cho các dịch vụ.                    | Thay đổi mỗi khi kết nối lại hoặc sau một khoảng thời gian nhất định.               |
| **Bảo mật**            | Có thể dễ bị nhắm mục tiêu hơn vì địa chỉ không đổi, cho tin tặc nhiều thời gian để thăm dò. | Khó theo dõi và tấn công hơn vì địa chỉ IP thay đổi liên tục.                       |
| **Chi phí**            | Thường yêu cầu trả thêm phí cho ISP (đối với IP công cộng tĩnh).                             | Thường được bao gồm miễn phí trong gói dịch vụ Internet.                            |
| **Trường hợp sử dụng** | Máy chủ (web, file, game), thiết bị mạng (router, switch), VPN, camera an ninh.              | Máy tính cá nhân, laptop, điện thoại thông minh, máy tính bảng của người dùng cuối. |

### 1.3. Tương lai của Kết nối: IPv4 vs. IPv6

Giao thức IP mà chúng ta đã thảo luận chủ yếu cho đến nay là IPv4 (Internet Protocol version 4). Tuy nhiên, nó có một người kế nhiệm đang dần được triển khai trên toàn cầu: IPv6.

**Tại sao cần IPv6: Sự cạn kiệt của IPv4**

IPv4 sử dụng một không gian địa chỉ 32-bit, cho phép tạo ra khoảng 232 (tức khoảng 4.3 tỷ) địa chỉ IP duy nhất. Vào thời điểm Internet ra đời, con số này có vẻ khổng lồ. Tuy nhiên, với sự bùng nổ của các thiết bị kết nối Internet—từ máy tính, điện thoại đến đồng hồ thông minh, tủ lạnh (Internet of Things - IoT)—không gian địa chỉ của IPv4 đã chính thức cạn kiệt.

IPv6 (Internet Protocol version 6) được tạo ra để giải quyết triệt để vấn đề này. Nó sử dụng không gian địa chỉ 128-bit, cung cấp một số lượng địa chỉ gần như vô hạn: 2128, hay khoảng 340 undecillion (340 nghìn tỷ tỷ tỷ tỷ) địa chỉ. Con số này đủ để cấp hàng tỷ địa chỉ cho mỗi mét vuông trên bề mặt Trái Đất.

**Những khác biệt Chính**

Ngoài không gian địa chỉ, IPv6 còn mang lại nhiều cải tiến quan trọng khác:

-   **Định dạng địa chỉ:** Địa chỉ IPv4 có dạng 4 cụm số thập phân, cách nhau bằng dấu chấm (ví dụ: `192.168.1.1`). Địa chỉ IPv6 có dạng 8 cụm số thập lục phân (hexadecimal), cách nhau bằng dấu hai chấm (ví dụ:
    `2001:0db8:85a3:0000:0000:8a2e:0370:7334`). Nó có thể được rút gọn bằng cách bỏ các số 0 đứng đầu và thay thế một chuỗi các số 0 liên tiếp bằng `::`.
-   **Bảo mật:** IPv6 được thiết kế với tư duy bảo mật ngay từ đầu. Nó tích hợp sẵn IPsec (Internet Protocol Security) như một thành phần bắt buộc, giúp mã hóa và xác thực lưu lượng mạng từ đầu đến cuối. Trong khi đó, IPsec là một tùy chọn bổ sung cho IPv4.
-   **Hiệu suất và Cấu hình:** IPv6 có cấu trúc tiêu đề (header) gói tin đơn giản và hiệu quả hơn, giúp các router xử lý gói tin nhanh hơn. Nó cũng giới thiệu tính năng Tự động cấu hình địa chỉ không trạng thái (SLAAC - Stateless Address Autoconfiguration), cho phép các thiết bị tự tạo địa chỉ IPv6 của riêng mình mà không cần đến máy chủ DHCP, giúp giảm lưu lượng quản lý trên mạng.
-   **Loại bỏ NAT:** Vì không gian địa chỉ của IPv6 là khổng lồ, mỗi thiết bị có thể có một địa chỉ IP công cộng duy nhất. Điều này loại bỏ sự cần thiết của NAT, cho phép kết nối trực tiếp từ đầu cuối (end-to-end) và đơn giản hóa việc phát triển các ứng dụng ngang hàng (peer-to-peer).

Mặc dù có những ưu điểm kỹ thuật vượt trội, quá trình chuyển đổi sang IPv6 diễn ra chậm chạp. Lý do chính không nằm ở công nghệ mà ở vấn đề kinh tế và logistics. IPv6 không tương thích ngược trực tiếp với IPv4. Điều này tạo ra một bài toán "con gà và quả trứng" kinh điển: các nhà cung cấp dịch vụ, nhà cung cấp nội dung và người dùng cuối đều do dự trong việc nâng cấp vì phần còn lại của hệ sinh thái chưa sẵn sàng. Việc này đòi hỏi một nỗ lực phối hợp toàn cầu để di cư toàn bộ Internet trong khi vẫn phải duy trì hoạt động của mạng IPv4. Đối với một quản trị viên Linux, điều này có một ý nghĩa thực tế quan trọng: trong tương lai gần, họ sẽ phải làm việc trong một môi trường

**song song (dual-stack)**, nơi các hệ thống phải được cấu hình và có khả năng xử lý cả hai giao thức IPv4 và IPv6. Do đó, việc thành thạo cả hai là một kỹ năng thiết yếu.

**Bảng 3: So sánh Chi tiết IPv4 và IPv6**

| Tiêu chí                   | IPv4                                                         | IPv6                                                                 |
| -------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------- |
| **Độ dài địa chỉ**         | 32-bit                                                       | 128-bit                                                              |
| **Định dạng**              | Số thập phân, ngăn cách bằng dấu chấm (ví dụ: `192.168.1.1`) | Số thập lục phân, ngăn cách bằng dấu hai chấm (ví dụ: `2001:db8::1`) |
| **Không gian địa chỉ**     | ~4.3 tỷ địa chỉ                                              | ~3.4 x 1038 địa chỉ                                                  |
| **Cấu hình địa chỉ**       | Thủ công hoặc qua DHCP                                       | Tự động cấu hình (SLAAC), DHCPv6                                     |
| **Bảo mật**                | IPsec là tùy chọn                                            | IPsec được tích hợp và là bắt buộc                                   |
| **NAT**                    | Thường xuyên cần thiết do thiếu hụt địa chỉ                  | Không cần thiết, cho phép kết nối đầu cuối thực sự                   |
| **Kích thước Header**      | 20-60 bytes, phức tạp hơn                                    | 40 bytes, cố định, đơn giản và hiệu quả hơn                          |
| **Phân mảnh gói tin**      | Thực hiện bởi cả máy gửi và router                           | Chỉ thực hiện bởi máy gửi                                            |
| **Truyền thông Multicast** | Hỗ trợ qua IGMP                                              | Là một phần cốt lõi của giao thức, sử dụng MLD                       |

## Phần 2: Bộ công cụ của Người dùng Linux: Tương tác với IP qua Dòng lệnh

Linux nổi tiếng với sức mạnh của giao diện dòng lệnh (CLI), và quản lý mạng cũng không ngoại lệ. Việc thành thạo một vài lệnh cơ bản sẽ giúp bạn nhanh chóng chẩn đoán và thu thập thông tin về hệ thống mạng của mình.

### 2.1. Tôi là ai trên Mạng? Tìm Địa chỉ IP của bạn

**Khám phá IP Private: Làm chủ `ip addr` và Ghi chú về `ifconfig`**

Để tìm địa chỉ IP riêng (private) của máy Linux, có một số lệnh bạn có thể sử dụng.

Công cụ hiện đại và được khuyến nghị nhất là lệnh `ip` từ bộ công cụ `iproute2`. Lý do cộng đồng Linux chuyển từ các công cụ cũ như `ifconfig` sang `ip` là vì `iproute2` được thiết kế để mạnh mẽ hơn, có cú pháp nhất quán hơn và có khả năng quản lý các khái niệm mạng hiện đại một cách hiệu quả hơn. Các công cụ cũ được tạo ra khi mạng còn đơn giản. Sự phát triển của ảo hóa, container, và các kịch bản định tuyến phức tạp đòi hỏi một bộ công cụ thống nhất và có năng lực hơn, và đó chính là

`iproute2`. Việc học cách sử dụng `ip` không chỉ là học một lệnh mới, mà là tiếp cận một mô hình quản lý mạng hiện đại và mạnh mẽ hơn trên Linux.

-   **Lệnh `ip addr` (hoặc `ip a`):** Đây là lệnh tiêu chuẩn để hiển thị thông tin về tất cả các giao diện mạng (network interfaces) và các địa chỉ IP được gán cho chúng.
    Bash
    ```
    $ ip addr show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
        link/ether 08:00:27:1a:2b:3c brd ff:ff:ff:ff:ff:ff
        inet 192.168.1.105/24 brd 192.168.1.255 scope global dynamic noprefixroute enp0s3
           valid_lft 85652sec preferred_lft 85652sec
        inet6 fe80::a00:27ff:fe1a:2b3c/64 scope link noprefixroute
           valid_lft forever preferred_lft forever
    ```
    Trong kết quả trên:
    -   `lo`: là giao diện loopback, luôn có địa chỉ `127.0.0.1`. Nó được dùng để máy tính "nói chuyện" với chính nó.
    -   `enp0s3`: là tên giao diện mạng vật lý (có thể là `eth0` trên các hệ thống cũ hơn).
    -   `inet 192.168.1.105/24`: Đây chính là địa chỉ IPv4 riêng của bạn. `/24` là ký hiệu CIDR cho biết netmask là `255.255.255.0`.
    -   `inet6 fe80::.../64`: Đây là địa chỉ IPv6 link-local.
-   **Lệnh `ifconfig`:** Đây là công cụ cũ từ bộ `net-tools`. Mặc dù đã lỗi thời và có thể không được cài đặt sẵn trên các bản phân phối mới, nó vẫn rất phổ biến và đáng để biết.
    Bash
    ```
    $ ifconfig enp0s3
    enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 192.168.1.105  netmask 255.255.255.0  broadcast 192.168.1.255
            inet6 fe80::a00:27ff:fe1a:2b3c  prefixlen 64  scopeid 0x20<link>
            ether 08:00:27:1a:2b:3c  txqueuelen 1000  (Ethernet)
           ...
    ```
-   **Lệnh `hostname -I`:** Đây là cách nhanh nhất để chỉ xem các địa chỉ IP của máy, không có thông tin thừa.
    Bash
    ```
    $ hostname -I
    192.168.1.105
    ```

**Hiển thị IP Public: Sử dụng `curl` và `wget`**

Địa chỉ IP công cộng của bạn được gán cho router, không phải cho máy tính của bạn trực tiếp. Do đó, bạn không thể tìm thấy nó bằng các lệnh nội bộ. Cách đơn giản nhất từ dòng lệnh là truy vấn một dịch vụ web bên ngoài được thiết kế để trả về địa chỉ IP của người yêu cầu.

-   **Sử dụng `curl`:**
    Bash
    ```
    $ curl https://icanhazip.com
    203.0.113.54
    ```
    Hoặc các dịch vụ tương tự như `ifconfig.me` hoặc `ipinfo.io/ip`.36
-   **Sử dụng `wget`:**
    Bash
    ```
    $ wget -qO- https://icanhazip.com
    203.0.113.54
    ```
    Tùy chọn `-q` (quiet) để không hiển thị thông tin tiến trình và `-O-` để xuất nội dung ra đầu ra chuẩn (màn hình terminal) thay vì lưu vào file.

### 2.2. Kiểm tra "Sức khỏe" Mạng: Lệnh `ping` và `traceroute`

**`ping`: Kiểm tra "Mạch đập" - Xác minh Kết nối và Độ trễ**

Lệnh `ping` (Packet Internet Groper) là công cụ chẩn đoán mạng cơ bản nhất. Nó gửi các gói tin ICMP ECHO_REQUEST đến một máy chủ đích và chờ đợi các gói tin ECHO_REPLY trả về. Nó giúp trả lời hai câu hỏi quan trọng: "Máy chủ đó có đang hoạt động và có thể kết nối được không?" và "Mất bao lâu để dữ liệu đi và về?".

-   **Kiểm tra kết nối đến một máy chủ từ xa:**
    Bash
    ```
    $ ping google.com
    PING google.com (142.250.199.14) 56(84) bytes of data.
    64 bytes from fra16s50-in-f14.1e100.net (142.250.199.14): icmp_seq=1 ttl=118 time=25.6 ms
    64 bytes from fra16s50-in-f14.1e100.net (142.250.199.14): icmp_seq=2 ttl=118 time=25.5 ms
    ```

```
--- google.com ping statistics ---

2 packets transmitted, 2 received, 0% packet loss, time 1002ms

rtt min/avg/max/mdev = 25.526/25.584/25.642/0.058 ms
```

(Nhấn Ctrl+C để dừng). Kết quả cho thấy kết nối thành công, không mất gói tin nào, và thời gian trễ trung bình (avg) là 25.584 ms.

-   **Các tùy chọn hữu ích:**
    -   **Giới hạn số lượng gói tin:** Sử dụng `-c` để lệnh tự dừng sau một số lượng gói nhất định.
        Bash
        ```
        $ ping -c 4 8.8.8.8
        ```
    -   **Kiểm tra mạng cục bộ:** `ping localhost` hoặc `ping 127.0.0.1` để đảm bảo card mạng và chồng giao thức TCP/IP của bạn đang hoạt động bình thường.

**`traceroute`: Vẽ Bản đồ Hành trình - Chẩn đoán Sự cố Định tuyến và "Nút cổ chai"**

Khi lệnh `ping` thất bại hoặc có độ trễ rất cao, câu hỏi tiếp theo là: "Sự cố xảy ra ở đâu trên đường đi?". Lệnh `traceroute` được sinh ra để trả lời câu hỏi này. Nó hiển thị từng "chặng" (hop)—tức là mỗi router—mà gói tin của bạn đi qua trên đường đến đích.

`traceroute` hoạt động một cách thông minh bằng cách lợi dụng một trường trong tiêu đề IP gọi là TTL (Time-To-Live). Nó gửi đi một loạt gói tin, bắt đầu với TTL=1. Router đầu tiên nhận được gói tin, giảm TTL xuống 0, và gửi lại một thông báo lỗi "Time Exceeded". `traceroute` ghi nhận địa chỉ của router này. Sau đó, nó gửi gói tin mới với TTL=2, gói tin này sẽ vượt qua router đầu tiên và chết ở router thứ hai, và cứ thế tiếp tục. Bằng cách này, nó vẽ ra toàn bộ bản đồ đường đi.

Bash

```
$ traceroute google.com
traceroute to google.com (142.250.199.14), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.1)  1.234 ms  1.567 ms  1.890 ms
 2  10.0.0.1 (10.0.0.1)  10.112 ms  10.345 ms  10.567 ms
 3  some.router.isp.net (203.0.113.1)  20.789 ms  20.912 ms  21.034 ms
...
12  fra16s50-in-f14.1e100.net (142.250.199.14)  25.456 ms  25.678 ms  25.890 ms
```

Kết quả này cho phép bạn thấy độ trễ tại mỗi chặng. Nếu bạn thấy độ trễ tăng đột biến hoặc các dấu `* * *` (nghĩa là không nhận được phản hồi) ở một chặng nào đó, đó có thể là nơi xảy ra sự cố mạng.

### 2.3. Dịch Tên thành Số: Truy vấn DNS với `dig`

**Tại sao `dig` là Tiêu chuẩn của Linux so với `nslookup`**

Cả `dig` và `nslookup` đều là các công cụ để truy vấn hệ thống DNS. Tuy nhiên, trong cộng đồng Linux và quản trị mạng, `dig` (Domain Information Groper) được ưa chuộng hơn hẳn. Lý do là

`dig` cung cấp đầu ra rất chi tiết, có cấu trúc rõ ràng và dễ dàng để phân tích bằng các script tự động, điều này cực kỳ quan trọng trong quản trị hệ thống.

`nslookup` cũ hơn, và mặc dù nó đã được "hồi sinh" và không còn bị coi là lỗi thời hoàn toàn, `dig` vẫn được xem là công cụ chuyên nghiệp, mạnh mẽ và linh hoạt hơn.

**Các Truy vấn DNS Thực tế: Tìm bản ghi A, MX và các bản ghi thiết yếu khác**

-   **Truy vấn cơ bản (tìm bản ghi A - địa chỉ IP):**
    Bash
    ```
    $ dig google.com
    ```
    Kết quả sẽ được chia thành các phần rõ ràng: `QUESTION SECTION` (câu hỏi bạn đã gửi) và `ANSWER SECTION` (câu trả lời từ máy chủ DNS).51
-   **Lấy câu trả lời ngắn gọn:** Để chỉ lấy địa chỉ IP, sử dụng tùy chọn `+short`.
    Bash
    ```
    $ dig +short google.com
    142.250.199.14
    ```
-   **Truy vấn một loại bản ghi cụ thể:** Bạn có thể chỉ định loại bản ghi bạn muốn tìm. Ví dụ, để tìm các máy chủ email (bản ghi MX - Mail Exchange) cho một tên miền:
    Bash
    ```
    $ dig google.com MX +short
    10 smtp.google.com.
    ```
-   **Truy vấn một máy chủ DNS cụ thể:** Mặc định, `dig` sử dụng máy chủ DNS được cấu hình trên hệ thống của bạn. Để truy vấn một máy chủ cụ thể (ví dụ: máy chủ DNS công cộng của Google), sử dụng ký hiệu `@`.
    Bash
    ```
    $ dig @8.8.8.8 fpt.vn
    ```
    Điều này rất hữu ích để chẩn đoán xem sự cố DNS có phải do máy chủ DNS của ISP của bạn hay không.

## Phần 3: Cấu hình Mạng Nâng cao: Gán IP Tĩnh

Trong khi IP động phù hợp cho hầu hết các thiết bị của người dùng cuối, có những trường hợp bạn cần một địa chỉ IP không bao giờ thay đổi. Đây là lúc cấu hình IP tĩnh trở nên cần thiết.

### 3.1. Tại sao và Khi nào nên Dùng IP Tĩnh?

Bạn nên sử dụng địa chỉ IP tĩnh khi một thiết bị cần được truy cập một cách nhất quán và đáng tin cậy bởi các thiết bị khác. Các kịch bản phổ biến bao gồm:

-   **Chạy Dịch vụ:** Nếu bạn đang lưu trữ một trang web, máy chủ file (FTP/SMB), máy chủ game, hoặc API trên máy Linux của mình, bạn cần một IP tĩnh để người dùng và các ứng dụng khác luôn biết cách kết nối đến nó.
-   **Truy cập Từ xa:** Đối với các kết nối như SSH hoặc VNC, việc có một IP tĩnh giúp bạn không phải tìm lại địa chỉ IP của máy chủ mỗi khi nó khởi động lại.
-   **Thiết bị Mạng Nội bộ:** Các thiết bị như máy in mạng, thiết bị lưu trữ NAS, hoặc camera an ninh nên được gán IP tĩnh để các máy tính trong mạng luôn có thể tìm thấy chúng một cách dễ dàng mà không bị gián đoạn.
-   **Port Forwarding:** Nếu bạn cần chuyển tiếp các port từ router đến một máy cụ thể trong mạng LAN, máy đó phải có IP tĩnh.

### 3.2. Hướng dẫn Cấu hình IP Tĩnh theo Từng Bản phân phối

Cách cấu hình mạng trên Linux đã có một sự tiến hóa đáng kể. Việc hiểu rõ sự khác biệt giữa các phương pháp không chỉ giúp bạn cấu hình đúng mà còn cho thấy triết lý quản lý hệ thống đang thay đổi. Chúng ta đã đi từ việc chỉnh sửa file trực tiếp và đơn giản trên Debian (`/etc/network/interfaces`), đến một phương pháp được quản lý bởi một dịch vụ trung tâm, năng động hơn trên CentOS (NetworkManager và `nmcli`), và cuối cùng là một cách tiếp cận "khai báo" và trừu tượng trên Ubuntu hiện đại (Netplan). Cách tiếp cận khai báo của Netplan cho phép bạn mô tả _trạng thái mong muốn_ của mạng trong một file YAML đơn giản, và Netplan sẽ tự động "dịch" nó thành cấu hình cho backend phù hợp (như NetworkManager hoặc systemd-networkd). Điều này phản ánh một xu hướng lớn hơn trong quản trị hệ thống: hướng tới tự động hóa, tính nhất quán và trừu tượng hóa sự phức tạp.

**Với Ubuntu (20.04+) và Netplan**

Các phiên bản Ubuntu hiện đại sử dụng `netplan` làm công cụ quản lý mạng mặc định. Các file cấu hình của nó là các file YAML nằm trong thư mục

`/etc/netplan/`.

1. **Xác định tên giao diện mạng:** Dùng lệnh `ip a` để tìm tên giao diện bạn muốn cấu hình (ví dụ: `enp0s3`, `eth0`).
2. **Chỉnh sửa file cấu hình Netplan:** Mở file YAML trong `/etc/netplan/` (tên file có thể là `00-installer-config.yaml` hoặc tương tự) bằng một trình soạn thảo văn bản như `nano` hoặc `vim`.

    Bash

    ```
    sudo nano /etc/netplan/00-installer-config.yaml
    ```

    **Lưu ý quan trọng:** Cú pháp YAML cực kỳ nhạy cảm với việc thụt lề. **Hãy sử dụng dấu cách (thường là 2 hoặc 4 dấu cách cho mỗi cấp), không bao giờ sử dụng phím Tab**.

3. **Cập nhật cấu hình:** Sửa đổi file để trông giống như sau, thay thế các giá trị cho phù hợp với mạng của bạn.

    YAML

    ```
    network:
      version: 2
      renderer: networkd
      ethernets:
        enp0s3: # <-- Thay bằng tên giao diện của bạn
          dhcp4: no # <-- Tắt DHCP để dùng IP tĩnh
          addresses:
            - 192.168.1.100/24 # <-- Địa chỉ IP tĩnh và netmask (dạng CIDR)
          gateway4: 192.168.1.1 # <-- Địa chỉ Gateway của mạng
          nameservers:
            addresses: [8.8.8.8, 1.1.1.1] # <-- Địa chỉ các máy chủ DNS
    ```

4. **Kiểm tra và Áp dụng:**

    - Trước khi áp dụng, hãy kiểm tra cú pháp file cấu hình:
      Bash
        ```
        sudo netplan try
        ```
        Lệnh này sẽ áp dụng cấu hình trong 120 giây và nếu không có vấn đề gì (ví dụ bạn không bị mất kết nối), nó sẽ giữ lại thay đổi. Nếu có lỗi, nó sẽ tự động hoàn nguyên.
    - Sau khi chắc chắn cấu hình đúng, hãy áp dụng vĩnh viễn:
      Bash
        ```
        sudo netplan apply
        ```

**Với Debian & Ubuntu cũ và `/etc/network/interfaces`**

Đây là phương pháp truyền thống trên các hệ thống dựa trên Debian (bao gồm cả Ubuntu 16.04 và cũ hơn).

1. **Chỉnh sửa file `interfaces`:**

    Bash

    ```
    sudo nano /etc/network/interfaces
    ```

2. **Cập nhật cấu hình:** Tìm đến đoạn cấu hình cho giao diện của bạn (ví dụ `eth0`) và sửa nó từ `dhcp` thành `static`, đồng thời thêm các thông số cần thiết.

    ```
    # Dòng này đảm bảo giao diện được bật khi khởi động
    auto eth0

    # Cấu hình IP tĩnh cho eth0
    iface eth0 inet static
        address 192.168.1.100
        netmask 255.255.255.0
        gateway 192.168.1.1
        dns-nameservers 8.8.8.8 1.1.1.1
    ```

3. **Khởi động lại dịch vụ mạng:** Để áp dụng các thay đổi, hãy khởi động lại dịch vụ mạng.

    Bash

    ```
    sudo systemctl restart networking
    ```

**Với CentOS/RHEL và `nmcli`**

Các hệ thống dựa trên Red Hat như CentOS, Fedora và RHEL sử dụng NetworkManager làm trình quản lý mạng mặc định. `nmcli` là công cụ dòng lệnh mạnh mẽ để tương tác với nó.

1. **Xác định tên kết nối:** Trước tiên, hãy liệt kê các kết nối mạng hiện có để lấy tên chính xác.

    Bash

    ```
    nmcli connection show
    ```

    Kết quả sẽ hiển thị một cột `NAME`, ví dụ: `ens33`.

2. **Sửa đổi kết nối:** Sử dụng một chuỗi các lệnh `nmcli` để cấu hình IP tĩnh. Thay `ens33` bằng tên kết nối của bạn.

    Bash

    ```
    # Chuyển sang phương thức cấu hình thủ công
    sudo nmcli con mod ens33 ipv4.method manual

    # Đặt địa chỉ IP và netmask
    sudo nmcli con mod ens33 ipv4.addresses 192.168.1.100/24

    # Đặt gateway
    sudo nmcli con mod ens33 ipv4.gateway 192.168.1.1

    # Đặt DNS
    sudo nmcli con mod ens33 ipv4.dns "8.8.8.8,1.1.1.1"
    ```

3. **Áp dụng cấu hình:** Kích hoạt lại kết nối để các thay đổi có hiệu lực.

    Bash

    ```
    sudo nmcli con up ens33
    ```

**Sử dụng Giao diện Đồ họa/Văn bản (NetworkManager GUI/TUI)**

Đối với các máy Linux có giao diện đồ họa (Desktop) hoặc cho những người không muốn làm việc trực tiếp với file cấu hình, NetworkManager cung cấp các công cụ trực quan.

-   **`nmtui` (Text User Interface):** Chạy lệnh `nmtui` trong terminal sẽ mở ra một giao diện dựa trên văn bản. Chọn `Edit a connection`, chọn giao diện của bạn, và sau đó thay đổi cấu hình IPv4 từ `Automatic` sang `Manual`. Bạn sẽ có các trường để nhập địa chỉ IP, Gateway và DNS.
-   **`nm-connection-editor` (Graphical User Interface):** Trên môi trường desktop GNOME, KDE, v.v., bạn có thể vào phần Cài đặt Mạng (Network Settings), chọn kết nối có dây hoặc không dây, nhấp vào biểu tượng cài đặt (bánh răng), chuyển sang tab IPv4, chọn phương thức "Manual" và điền các thông số tương tự.

## Phần 4: Khám phá "Hàng xóm" Kỹ thuật số: Quét tìm Thiết bị Mạng

Sau khi đã cấu hình xong mạng cho máy của mình, bước tiếp theo là khám phá xem có những thiết bị nào khác đang cùng tồn tại trong mạng cục bộ (LAN) của bạn.

### 4.1. Quét nhanh: Khám phá Láng giềng trong LAN với `arp-scan`

**Hiểu về ARP (Address Resolution Protocol)**

Trước khi dùng công cụ, hãy hiểu nguyên lý. Trong một mạng LAN, các thiết bị giao tiếp với nhau ở Lớp 2 (Data Link) bằng địa chỉ MAC. Khi máy A (IP `192.168.1.10`) muốn gửi dữ liệu cho máy B (IP `192.168.1.20`), nó cần biết địa chỉ MAC của máy B. Máy A sẽ phát một gói tin ARP request ra toàn mạng với câu hỏi: "Thiết bị nào có IP `192.168.1.20`? Xin hãy cho tôi biết địa chỉ MAC của bạn". Máy B khi nhận được yêu cầu này sẽ trả lời bằng một gói tin ARP reply chứa địa chỉ MAC của nó.

**Sử dụng `arp-scan`**

`arp-scan` là một công cụ dòng lệnh khai thác chính giao thức này. Nó gửi các gói tin ARP request cho mọi địa chỉ IP có thể có trong mạng con của bạn và lắng nghe các phản hồi.

Điểm mạnh của `arp-scan` là nó hoạt động ở Lớp 2. Nhiều thiết bị có thể được cấu hình tường lửa để chặn các gói tin ping (ICMP) hoặc các kết nối TCP (Lớp 3 và 4), khiến chúng trở nên "vô hình" trước các công cụ quét thông thường. Tuy nhiên, để có thể hoạt động trên mạng LAN, một thiết bị _bắt buộc_ phải phản hồi các yêu cầu ARP. Do đó, `arp-scan` có khả năng phát hiện gần như mọi thiết bị đang hoạt động trên mạng cục bộ của bạn, ngay cả khi chúng có tường lửa.

Để sử dụng, bạn có thể cần cài đặt nó trước:

Bash

```
# Trên Debian/Ubuntu
sudo apt install arp-scan
# Trên CentOS/RHEL
sudo yum install arp-scan
```

Sau đó, chạy lệnh với quyền root:

Bash

```
sudo arp-scan --localnet
# hoặc viết tắt
sudo arp-scan -l
```

Kết quả sẽ là một danh sách các địa chỉ IP, địa chỉ MAC tương ứng và nhà sản xuất card mạng (dựa trên địa chỉ MAC).

```
Interface: enp0s3, type: EN10MB, MAC: 08:00:27:1a:2b:3c, IPv4: 192.168.1.105
Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.1.1     01:23:45:67:89:ab   (Unknown)
192.168.1.50    ab:cd:ef:12:34:56   TP-LINK TECHNOLOGIES CO.,LTD.
192.168.1.102   fe:dc:ba:65:43:21   Apple, Inc.
...
```

### 4.2. Quét sâu: Sức mạnh của `nmap`

`arp-scan` rất tuyệt vời để trả lời câu hỏi "Có những ai ở đây?", nhưng `nmap` (Network Mapper) sẽ trả lời câu hỏi sâu hơn: "Họ là ai và họ đang làm gì?". `nmap` là một con dao đa năng của Thụy Sĩ trong lĩnh vực quét mạng, có khả năng khám phá máy chủ, các cổng đang mở, các dịch vụ đang chạy, phiên bản của chúng, hệ điều hành và thậm chí cả các lỗ hổng bảo mật tiềm tàng.

Một người mới bắt đầu có thể chỉ dùng `nmap` để quét, nhưng một cách tiếp cận chuyên nghiệp và đáng tin cậy hơn là kết hợp sức mạnh của cả hai công cụ. Tường lửa có thể chặn các phương pháp khám phá máy chủ của `nmap` (dựa trên ICMP, TCP, UDP). Do đó, một quy trình làm việc hiệu quả là:

1. **Sử dụng `arp-scan` (Layer 2) để xây dựng một danh sách chắc chắn về tất cả các thiết bị đang hoạt động trên mạng.**
2. **Sử dụng danh sách IP thu được từ `arp-scan` làm đầu vào cho `nmap` (Layer 3/4) để thực hiện quét chi tiết về cổng và dịch vụ.**

Cách tiếp cận kết hợp này đảm bảo bạn không bỏ sót bất kỳ thiết bị nào và có được bức tranh toàn cảnh nhất về mạng của mình.

**Các kiểu Quét Cơ bản với `nmap`**

-   **Khám phá Máy chủ (Ping Scan):** Nhanh chóng xác định các máy chủ nào đang "sống" trong một dải mạng mà không cần quét cổng.
    Bash
    ```
    nmap -sn 192.168.1.0/24
    ```
    Tùy chọn `-sn` (scan no port) chỉ thực hiện khám phá máy chủ.
-   **Quét các Cổng phổ biến:** Đây là kiểu quét mặc định của `nmap`. Nó sẽ quét 1000 cổng TCP phổ biến nhất trên một mục tiêu.
    Bash
    ```
    nmap 192.168.1.50
    ```
    Kết quả sẽ liệt kê các cổng ở trạng thái `open` (đang có dịch vụ lắng nghe), `closed` (không có dịch vụ), hoặc `filtered` (bị tường lửa chặn).
-   **Các loại quét cổng khác:**
    -   `nmap -sT 192.168.1.50`: TCP Connect Scan. Hoàn thành một bắt tay TCP đầy đủ. Đáng tin cậy nhưng dễ bị ghi lại trong log.
    -   `sudo nmap -sS 192.168.1.50`: SYN "Stealth" Scan. Chỉ gửi gói SYN đầu tiên của bắt tay TCP. Nhanh hơn, "kín đáo" hơn, nhưng yêu cầu quyền root.
    -   `sudo nmap -sU 192.168.1.50`: Quét các cổng UDP. Chậm hơn và khó xác định hơn TCP.

**Thu thập Thông tin Nâng cao**

-   **Phát hiện Phiên bản Dịch vụ (`-sV`):** Cố gắng xác định chính xác tên và phiên bản của dịch vụ đang chạy trên các cổng mở. Thông tin này cực kỳ quý giá để tìm kiếm các lỗ hổng đã biết.
    Bash
    ```
    sudo nmap -sV 192.168.1.50
    ```
-   **Phát hiện Hệ điều hành (`-O`):** Cố gắng đoán hệ điều hành của máy chủ mục tiêu dựa trên các phản hồi mạng của nó.
    Bash
    ```
    sudo nmap -O 192.168.1.50
    ```
-   **Quét Toàn diện (`-A`):** Tùy chọn "hung hăng" (Aggressive) này kết hợp nhiều tính năng mạnh mẽ, bao gồm phát hiện hệ điều hành (`-O`), phát hiện phiên bản (`-sV`), quét script (`-sC`) và traceroute. Nó cung cấp một báo cáo rất chi tiết về mục tiêu.
    Bash
    ```
    sudo nmap -A 192.168.1.50
    ```

## Phần 5: Điều khiển từ xa qua IP: SSH và VNC

Một khi bạn đã xác định được địa chỉ IP của một máy khác, bạn có thể sử dụng nó để truy cập và điều khiển máy đó từ xa. Hai giao thức phổ biến nhất cho việc này trên Linux là SSH (cho dòng lệnh) và VNC (cho giao diện đồ họa).

### 5.1. SSH (Secure Shell): Cổng vào Dòng lệnh của Quản trị viên

SSH là giao thức tiêu chuẩn để truy cập dòng lệnh của một máy chủ Linux từ xa một cách an toàn. Mọi dữ liệu truyền qua SSH, bao gồm cả thông tin đăng nhập và các lệnh bạn gõ, đều được mã hóa mạnh mẽ.

**Cài đặt và Thiết lập `openssh-server`**

Hầu hết các máy khách Linux đã cài đặt sẵn `openssh-client`. Tuy nhiên, máy bạn muốn kết nối đến (máy chủ) cần phải cài đặt và chạy `openssh-server`.

-   **Trên Debian/Ubuntu:**
    Bash
    ```
    sudo apt update
    sudo apt install openssh-server
    ```
-   **Trên CentOS/RHEL:**
    Bash
    ```
    sudo yum install openssh-server
    ```

Sau khi cài đặt, dịch vụ SSH (thường được gọi là `sshd`) sẽ tự động khởi động. Bạn có thể kiểm tra trạng thái của nó:

Bash

```
sudo systemctl status ssh
```

**Kết nối An toàn: Từ Mật khẩu Cơ bản đến Xác thực bằng Cặp khóa SSH**

-   **Kết nối bằng mật khẩu (Cách cơ bản):**
    Bash
    ```
    ssh username@ip_address
    ```
    Ví dụ: `ssh admin@192.168.1.100`. Lần đầu kết nối, bạn sẽ được yêu cầu xác nhận "dấu vân tay" (fingerprint) của máy chủ. Sau đó, bạn nhập mật khẩu của người dùng `admin` trên máy chủ. Cách này đơn giản nhưng kém an toàn hơn vì mật khẩu có thể bị dò ra.
-   Kết nối bằng cặp khóa SSH (Cách chuyên nghiệp và an toàn hơn):
    Phương pháp này sử dụng một cặp khóa mã hóa: một khóa riêng tư (private key) được giữ bí mật trên máy khách của bạn, và một khóa công khai (public key) được đặt trên máy chủ.
    -   **Tạo cặp khóa trên máy khách của bạn:**
        Bash
        ```
        ssh-keygen -t rsa -b 4096
        ```
        Lệnh này sẽ tạo ra một cặp khóa RSA với độ dài 4096 bit. Bạn sẽ được hỏi nơi lưu khóa (cứ nhấn Enter để dùng vị trí mặc định `~/.ssh/id_rsa`) và một cụm mật khẩu (passphrase) để bảo vệ thêm cho khóa riêng tư của bạn (bạn có thể bỏ trống).
    -   **Sao chép khóa công khai lên máy chủ:** Cách dễ nhất là sử dụng lệnh `ssh-copy-id`.
        Bash
        ```
        ssh-copy-id username@ip_address
        ```
        Lệnh này sẽ tự động kết nối đến máy chủ, yêu cầu bạn nhập mật khẩu lần cuối, và sau đó sao chép nội dung của khóa công khai (`~/.ssh/id_rsa.pub`) vào đúng file `~/.ssh/authorized_keys` trên máy chủ.
    -   **Đăng nhập:** Bây giờ, khi bạn chạy lại lệnh `ssh username@ip_address`, máy chủ sẽ nhận ra khóa công khai của bạn và cho phép bạn đăng nhập mà không cần mật khẩu.

**Tăng cường Bảo mật cho Máy chủ SSH**

Để làm cho máy chủ SSH của bạn an toàn hơn nữa, hãy chỉnh sửa file cấu hình `/etc/ssh/sshd_config`.

-   **Thay đổi cổng mặc định:** Tin tặc thường quét cổng 22 (cổng mặc định của SSH). Thay đổi nó sang một cổng khác (ví dụ: `Port 2222`) sẽ giúp tránh các cuộc tấn công tự động.
-   **Vô hiệu hóa đăng nhập của người dùng `root`:** Đăng nhập trực tiếp bằng `root` là một rủi ro bảo mật lớn. Hãy đặt `PermitRootLogin no`.
-   **Chỉ cho phép đăng nhập bằng khóa:** Sau khi đã thiết lập xác thực bằng khóa thành công, hãy vô hiệu hóa hoàn toàn việc đăng nhập bằng mật khẩu để tăng cường bảo mật tối đa. Đặt `PasswordAuthentication no`.

Sau khi thay đổi file cấu hình, đừng quên khởi động lại dịch vụ SSH: `sudo systemctl restart ssh`.

### 5.2. VNC (Virtual Network Computing): Giao diện Đồ họa Từ xa

Trong khi SSH là lựa chọn hoàn hảo cho dòng lệnh, VNC cho phép bạn xem và tương tác với toàn bộ môi trường desktop đồ họa (GUI) của một máy tính từ xa, như thể bạn đang ngồi ngay trước nó. Điều này rất hữu ích cho việc hỗ trợ kỹ thuật, quản lý các ứng dụng có giao diện đồ họa, hoặc làm việc từ xa.

**Cài đặt và Cấu hình một Máy chủ VNC (ví dụ: TightVNC) trên Linux**

1. **Cài đặt Môi trường Desktop (nếu cần):** Nếu bạn đang làm việc trên một phiên bản Server của Linux (không có GUI), bạn cần cài đặt một môi trường desktop trước. XFCE là một lựa chọn nhẹ và phổ biến.

    Bash

    ```
    # Trên Debian/Ubuntu
    sudo apt update
    sudo apt install xfce4 xfce4-goodies
    ```

2. **Cài đặt VNC Server:**

    Bash

    ```
    # Trên Debian/Ubuntu
    sudo apt install tightvncserver
    ```

3. **Chạy VNC Server lần đầu:** Chạy lệnh `vncserver` để thiết lập. Nó sẽ yêu cầu bạn tạo một mật khẩu chỉ dành cho VNC (tối đa 8 ký tự).

    Bash

    ```
    vncserver
    ```

    Sau khi thiết lập mật khẩu, nó sẽ khởi động một phiên VNC mới và cho bạn biết số hiệu màn hình (display number), ví dụ: `New 'X' desktop is your-hostname:1`. Số `:1` này tương ứng với cổng TCP `5901` (cổng mặc định của VNC là 5900 + số hiệu màn hình).

**Kết nối từ Máy Client bằng một Trình xem VNC**

Trên máy tính cục bộ của bạn (Windows, macOS, hoặc Linux khác), bạn cần cài đặt một phần mềm VNC Viewer. Có rất nhiều lựa chọn miễn phí như TightVNC Viewer, RealVNC Viewer, hoặc UltraVNC.

Mở VNC Viewer của bạn và nhập địa chỉ của máy chủ VNC theo định dạng `IP_máy_chủ:số_hiệu_màn_hình`, ví dụ: `192.168.1.100:1`. Sau đó, nhập mật khẩu VNC bạn đã tạo ở bước trên để kết nối.

### 5.3. Vượt Tường lửa An toàn: Giới thiệu về SSH Tunneling (Port Forwarding)

Đây là một kỹ thuật cực kỳ quan trọng, kết hợp sức mạnh của cả SSH và VNC. Vấn đề cốt lõi là giao thức VNC nguyên bản **không được mã hóa**. Mọi thứ bạn gõ và mọi thứ hiển thị trên màn hình đều được truyền đi dưới dạng văn bản thuần túy, khiến nó rất không an toàn khi sử dụng qua một mạng không tin cậy như Internet.

Việc mở trực tiếp cổng VNC (5901, 5902,...) ra Internet là một rủi ro bảo mật nghiêm trọng. Một người mới có thể làm điều này, nhưng một chuyên gia thì không. Cách tiếp cận chuyên nghiệp và an toàn là **không bao giờ phơi bày một dịch vụ không an toàn ra ngoài**. Thay vào đó, chúng ta sẽ sử dụng SSH, vốn đã là một kênh giao tiếp an toàn, để tạo một "đường hầm" được mã hóa và cho lưu lượng VNC đi qua đó. Đây không phải là một "mẹo", mà là một **tiêu chuẩn bắt buộc** khi làm việc với các giao thức không an toàn qua mạng công cộng.

**Kịch bản Sử dụng Thực tế: Bảo vệ Kết nối VNC qua Đường hầm SSH**

1. **Thiết lập:** Đảm bảo máy chủ của bạn đã cài đặt `openssh-server` và bạn có thể kết nối đến nó bằng SSH. Đảm bảo máy chủ cũng đang chạy một phiên VNC (ví dụ trên cổng 5901). **Không mở cổng 5901 trên tường lửa của máy chủ.**
2. **Tạo đường hầm SSH từ máy khách:** Mở terminal trên máy khách của bạn và chạy lệnh sau:

    Bash

    ```
    ssh -L 5901:localhost:5901 username@ip_address
    ```

    Hãy phân tích lệnh này 95:

    - `ssh...`: Khởi tạo một kết nối SSH như bình thường.
    - `-L 5901:localhost:5901`: Đây là phần tạo đường hầm (Local Port Forwarding).
        - `5901:` (phần đầu tiên): Mở cổng `5901` trên **máy khách** (máy cục bộ của bạn) và lắng nghe các kết nối.
        - `localhost`: Từ góc nhìn của **máy chủ SSH**, đích đến của đường hầm là `localhost` (chính nó).
        - `:5901` (phần cuối cùng): Kết nối sẽ được chuyển tiếp đến cổng `5901` trên đích đó (tức là cổng VNC trên máy chủ).

    Nói một cách đơn giản, lệnh này có nghĩa là: "Bất kỳ lưu lượng nào được gửi đến cổng 5901 trên máy tính của tôi, hãy chuyển tiếp nó một cách an toàn qua đường hầm SSH đến cổng 5901 trên máy chủ."

3. **Kết nối VNC:** Bây giờ, trên máy khách của bạn, hãy mở VNC Viewer và thay vì kết nối đến `dia_chi_ip_may_chu:1`, bạn hãy kết nối đến `localhost:1` (hoặc `127.0.0.1:5901`).

Kết nối VNC của bạn bây giờ sẽ đi qua đường hầm SSH đã được mã hóa, đảm bảo an toàn tuyệt đối cho phiên làm việc từ xa của bạn.

## Phần 6: Kết luận và các Bước Tiếp theo

Chúng ta đã cùng nhau trải qua một hành trình dài và chi tiết, từ việc giải phẫu những khái niệm cơ bản nhất của địa chỉ IP, phân loại chúng, cho đến việc sử dụng các công cụ dòng lệnh mạnh mẽ của Linux để tương tác với mạng. Bạn đã học cách tìm địa chỉ IP của mình, kiểm tra sức khỏe mạng, cấu hình IP tĩnh cho các bản phân phối phổ biến, quét tìm các thiết bị khác, và quan trọng nhất là thiết lập các kết nối từ xa an toàn bằng SSH và VNC kết hợp với SSH tunneling.

Kiến thức về mạng là vô tận. Những gì bạn đã học được ở đây là những khối xây dựng cơ bản. Để tiếp tục phát triển kỹ năng của mình, bạn có thể khám phá các chủ đề nâng cao sau:

-   **Tường lửa và Bảo mật Mạng:** Tìm hiểu về các công cụ như `ufw` (Uncomplicated Firewall), `firewalld`, và `iptables` để kiểm soát lưu lượng ra vào máy Linux của bạn.
-   **Chia Mạng con (Subnetting):** Học cách chia một mạng lớn thành các mạng con nhỏ hơn để quản lý không gian địa chỉ hiệu quả và tăng cường bảo mật.
-   **Mạng riêng ảo (VPN):** Tìm hiểu cách thiết lập các máy chủ VPN như OpenVPN hoặc WireGuard để tạo ra các kết nối an toàn và riêng tư đến mạng của bạn từ bất kỳ đâu.
-   **Các khái niệm Mạng Nâng cao:** Khám phá các chủ đề như Network Namespaces (để cô lập các môi trường mạng, nền tảng của container), các giao thức định tuyến động, và cấu hình mạng phức tạp hơn.

Chúc bạn thành công trên con đường làm chủ hệ thống của mình!

---

_Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!_
