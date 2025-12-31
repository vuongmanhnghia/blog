---
title: 6 Level Deploy
date: 2025-08-17
image: /images/image-placeholder.png
categories:
  - devops
tags:
  - docker
draft: false
---

6 Cấp Độ Trưởng Thành Từ Deploy Thủ Công Đến Vận Hành Tinh Gọn

<!--more-->

---
## Level 0: Deploy Thủ Công

### Công cụ và Quy trình

-   **Quy trình thủ công:** Việc triển khai được thực hiện bằng cách kết nối thủ công đến máy chủ thông qua các giao thức như FTP, SCP, hoặc SSH, sau đó sao chép từng tệp.
	
-   **Quản lý mã nguồn hỗn loạn:** Nếu có sử dụng Git, quy trình làm việc thường là "Centralized Workflow", nơi mọi người đều đẩy (push) mã nguồn trực tiếp lên nhánh chính (`main` hoặc `master`), gây ra sự bất ổn định và khó theo dõi.
	
### Rủi ro và Nỗi đau
	
-   **Rủi ro bảo mật:** Giao thức FTP truyền thông tin đăng nhập (username, password) dưới dạng văn bản thuần (plain text), khiến chúng dễ dàng bị "bắt" bởi bất kỳ ai trên mạng. Dữ liệu truyền đi cũng không được mã hóa, có nguy cơ bị tấn công xen giữa (man-in-the-middle), nơi kẻ tấn công có thể chèn mã độc vào các tệp đang được triển khai mà không bị phát hiện.
	
-   **Hệ thống cực kỳ mong manh:** Quy trình này rất dễ xảy ra lỗi. Chỉ cần quên một tệp, sao chép sai thư mục, hoặc một tệp truyền bị lỗi cũng có thể làm sập toàn bộ hệ thống.
	
-   **Không có cơ chế Rollback:** Khi một lần triển khai thất bại, không có cách nào dễ dàng và tự động để quay trở lại phiên bản ổn định trước đó.
	
## Level 1: Script và Quản Lý Mã Nguồn Có Cấu Trúc

### Công cụ và Quy trình
	
-   **Sự ra đời của Script:** "Deployment checklist" từ `level 0` được mã hóa thành một kịch bản (script) triển khai đơn giản, thường sử dụng Bash. Script này tự động hóa các bước kết nối đến máy chủ, lấy mã nguồn mới nhất từ kho chứa, và khởi động lại các dịch vụ.
	
-   **Quy trình Git có cấu trúc:** Nhóm nhận ra rằng việc đẩy trực tiếp lên nhánh `main` là không bền vững. Họ áp dụng một chiến lược phân nhánh chính thức, phổ biến nhất là **Feature Branch Workflow**.
	
    -   Nhánh `main` giờ đây được coi là "bất khả xâm phạm" và luôn ở trạng thái sẵn sàng để triển khai.
		
    -   Tất cả công việc mới (tính năng, sửa lỗi) được thực hiện trên các nhánh riêng biệt.
		
    -   Các thay đổi được tích hợp trở lại vào `main` thông qua Pull Request (hoặc Merge Request), cho phép thực hiện quy trình đánh giá mã nguồn (code review).
	
### Lợi ích và Những Vấn đề Còn Tồn Tại
	
-   **Lợi ích:** Bản thân quy trình triển khai giờ đây đã đáng tin cậy và nhất quán hơn. Nhánh `main` ổn định hơn. Việc đánh giá mã nguồn giúp cải thiện chất lượng.
	
-   **Vấn đề còn tồn tại:** Script không xử lý tốt các trường hợp thất bại. Không có kiểm thử tự động, lỗi vẫn được triển khai, chỉ là một cách nhất quán hơn. Các môi trường (development, staging, production) vẫn được cấu hình thủ công và không nhất quán, dẫn đến vấn đề kinh điển "nó chạy trên máy của tôi".
	
## Level 2: CI/CD

Đây là một bước nhảy vọt. Trọng tâm chuyển từ một script triển khai đơn lẻ sang một **đường ống (pipeline)** tự động hóa hoàn toàn, hoạt động như một "nhà máy" trung tâm cho việc phân phối phần mềm. Đây là nơi thế giới "Dev" và "Ops" thực sự bắt đầu hợp nhất.

### Cốt Lõi

-   **Tích hợp Liên tục (Continuous Integration - CI):** Là thực tiễn tự động hóa việc tích hợp các thay đổi mã nguồn từ nhiều nhà phát triển vào một dự án duy nhất. Mỗi lần đẩy mã nguồn lên một nhánh sẽ kích hoạt một quy trình xây dựng (build) tự động và một bộ các bài kiểm thử tự động (unit test, integration test).
	
-   **Phân phối Liên tục (Continuous Delivery - CD):** Là một phần mở rộng của CI. Sau khi các giai đoạn xây dựng và kiểm thử thành công, phần mềm sẽ được đóng gói và triển khai tự động đến một hoặc nhiều môi trường phi sản xuất (như staging). Việc triển khai lên production thường là một bước thủ công, chỉ cần một cú nhấp chuột.
	
-   **Triển khai Liên tục (Continuous Deployment - cũng là CD):** Là hình thức tiên tiến nhất, nơi mọi thay đổi vượt qua tất cả các bài kiểm thử tự động đều được _triển khai tự động_ lên production mà không cần sự can thiệp của con người.
	
### Công cụ

Việc lựa chọn một công cụ CI/CD là một quyết định quan trọng ở giai đoạn này. Bảng dưới đây so sánh các lựa chọn phổ biến nhất.

| Tính năng                       | Jenkins                                                                                              | GitLab CI                                                                                     | GitHub Actions                                                                                 |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Thiết lập & Lưu trữ**         | Cần cài đặt thủ công, thiết lập agent, tự lưu trữ (on-premise/cloud).                                | Tích hợp sẵn trong GitLab, không cần cài đặt riêng.                                           | Tích hợp sẵn trong GitHub, không cần cài đặt riêng.                                            |
| **Cấu hình**                    | Jenkinsfile (viết bằng Groovy) hoặc qua giao diện người dùng (UI).                                   | Tệp YAML (`.gitlab-ci.yml`) trong kho mã nguồn.                                               | Tệp YAML trong thư mục `.github/workflows`.                                                    |
| **Hệ sinh thái & Mở rộng**      | Cực kỳ mạnh mẽ với hơn 1800 plugin, tùy biến cao nhưng có thể phức tạp và dễ gặp vấn đề tương thích. | Tích hợp sâu với các tính năng của GitLab. Hệ sinh thái plugin nhỏ hơn Jenkins.               | Thị trường (Marketplace) rộng lớn với các "Actions" tái sử dụng. Dễ dàng tạo action tùy chỉnh. |
| **Trường hợp sử dụng lý tưởng** | Các quy trình phức tạp, yêu cầu tùy biến sâu, môi trường on-premise hoặc các hệ thống cũ (legacy).   | Các nhóm đã và đang sử dụng GitLab làm nền tảng chính, muốn một giải pháp "tất cả trong một". | Các nhóm ưu tiên GitHub, dự án mã nguồn mở, startup, cần sự đơn giản và khởi đầu nhanh chóng.  |

### Lợi ích và Thách thức Mới

-   **Lợi ích:** Vòng lặp phản hồi nhanh hơn đáng kể, chất lượng mã nguồn được cải thiện, giảm rủi ro triển khai và tăng năng suất của nhà phát triển.
	
-   **Thách thức:** Bản thân "đường ống CI/CD" trở thành một phần mềm phức tạp cần được bảo trì. Các nhóm giờ đây phải đối mặt với những vấn đề mới như các bài kiểm thử chạy chậm hoặc không ổn định (flaky tests), quản lý các phụ thuộc phức tạp, và vấn đề dai dẳng về "trôi dạt môi trường" (environment drift), nơi môi trường staging và production không giống hệt nhau.

## Level 3: Hạ Tầng Dưới Dạng Mã (IaC) và Container Hóa

Để giải quyết vấn đề trôi dạt môi trường và làm cho việc quản lý hạ tầng trở nên nghiêm ngặt như phát triển ứng dụng, các nhóm áp dụng triết lý "mọi thứ đều là mã nguồn".

### Cốt Lõi
	
-   **Hạ tầng dưới dạng mã (Infrastructure as Code - IaC):** Là việc quản lý và cấp phát hạ tầng (máy chủ, mạng, cơ sở dữ liệu) thông qua các tệp định nghĩa mà máy có thể đọc được (mã nguồn), thay vì cấu hình thủ công. Có hai cách tiếp cận chính:
	
    -   **Declarative:** Bạn định nghĩa _trạng thái cuối cùng_ mong muốn của hạ tầng. Công cụ (ví dụ: Terraform) sẽ tự tìm cách để đạt được trạng thái đó. Đây là cách tiếp cận chủ đạo trong IaC hiện đại.
		
    -   **Imperative:** Bạn viết các kịch bản chỉ định các _bước chính xác_ cần thực hiện để cấu hình hạ tầng (ví dụ: Ansible, Chef, Puppet).
	
-   **Container hóa với Docker:** Là người bạn đồng hành hoàn hảo của IaC. Docker giải quyết vấn đề "nó chạy trên máy của tôi" bằng cách đóng gói một ứng dụng và tất cả các phụ thuộc của nó vào một đơn vị duy nhất, được tiêu chuẩn hóa và bị cô lập gọi là **container**.
	
    -   **Dockerfile:** "Công thức" hay bản thiết kế để xây dựng một image.
		
    -   **Image:** Một mẫu chỉ đọc (read-only) chứa ứng dụng và môi trường của nó.
		
    -   **Container:** Một thực thể đang chạy (running instance) của một image. Nó nhẹ và có tính di động cao.
	
### Quy trình Mới

Đường ống CI/CD được nâng cấp. Nó không còn chỉ triển khai mã nguồn; nó xây dựng một Docker image (một tạo phẩm nhất quán được đảm bảo) và sử dụng các công cụ IaC như Terraform để cấp phát một môi trường giống hệt nơi container sẽ chạy.

### Lợi ích và Nút thắt Cổ chai Tiếp theo

-   **Lợi ích:** Vấn đề trôi dạt môi trường được loại bỏ. Các lần triển khai giờ đây có tính nhất quán và độ tin cậy cao trên các môi trường dev, staging và production. Các thay đổi về hạ tầng được quản lý phiên bản, được đánh giá và có thể kiểm tra lại.
	
-   **Nút thắt cổ chai tiếp theo:** Tổ chức bây giờ đã thành công và có hàng trăm hoặc hàng nghìn container. Làm thế nào để quản lý chúng? Làm thế nào để xử lý mạng, mở rộng quy mô và kiểm tra sức khỏe cho tất cả các container này? Đây là vấn đề của việc **điều phối (orchestration)**.
	
## Level 4: Điều Phối Container và Kiến Trúc Cloud-Native

Trọng tâm chuyển từ việc quản lý các container riêng lẻ sang quản lý một ứng dụng phân tán bao gồm nhiều container ở quy mô lớn. Điều này đòi hỏi một "nhạc trưởng" cho "dàn nhạc" container.

### Cốt Lõi: Kubernetes (K8s)

-   **Kubernetes:** Là hệ thống mã nguồn mở, tiêu chuẩn de-facto của ngành công nghiệp, dùng để tự động hóa việc triển khai, mở rộng quy mô và quản lý các ứng dụng được container hóa. Nó giải quyết vấn đề chạy các hệ thống phân tán một cách linh hoạt và có khả năng phục hồi.
	
-   **Các đối tượng Kubernetes chính:
	
    -   **Pod:** Đơn vị triển khai nhỏ nhất, cơ bản nhất trong Kubernetes. Nó là một lớp vỏ bọc quanh một hoặc nhiều container, chia sẻ tài nguyên lưu trữ và mạng. Hãy coi nó như "nguyên tử" cơ bản của một ứng dụng K8s.
		
    -   **Deployment:** Một đối tượng cấp cao hơn mô tả _trạng thái mong muốn_ cho ứng dụng của bạn. Nó nói với Kubernetes rằng "Tôi muốn có 3 bản sao (replica) của pod máy chủ web của tôi chạy mọi lúc." Bộ điều khiển Deployment (Deployment Controller) sẽ làm việc để biến trạng thái này thành hiện thực.
		
    -   **Service:** Một lớp trừu tượng định nghĩa một tập hợp logic các Pod và một chính sách để truy cập chúng. Nó cung cấp một địa chỉ IP và tên DNS ổn định, để các phần khác của ứng dụng (hoặc người dùng bên ngoài) có thể kết nối đến các Pod, ngay cả khi chúng được tạo ra và phá hủy.

### Lợi ích và Sự Phức Tạp Mới

-   **Lợi ích:** Tổ chức đạt được khả năng mở rộng quy mô thực sự, tự phục hồi (Kubernetes tự động khởi động lại các container bị lỗi), và tính sẵn sàng cao. Các bản cập nhật và quay lui (rolling updates and rollbacks) giờ đây được quản lý một cách khai báo và an toàn.
	
-   **Sự phức tạp mới:** Bản thân Kubernetes là một hệ thống cực kỳ phức tạp. Việc học nó rất khó khăn. Quản lý, giám sát và bảo mật một cụm Kubernetes (cluster) trở thành một công việc toàn thời gian. Thách thức mới không còn là "làm thế nào để chạy ứng dụng của chúng ta?" mà là "làm thế nào để chạy Kubernetes một cách đáng tin cậy?"
	
## Level 5: Vận Hành Dựa Trên Dữ Liệu (SRE, GitOps, & Observability)

Đây là level cao nhất. Các hoạt động vận hành không còn là bị động hay thậm chí chỉ là tự động; chúng trở nên chủ động, được điều khiển bằng dữ liệu và được xem như một ngành kỹ thuật phần mềm.

### Cốt Lõi

-   **Site Reliability Engineering - SRE:** Một phương pháp triển khai cụ thể của DevOps, bắt nguồn từ Google. Nó coi các vấn đề vận hành như những bài toán phần mềm.
	
    -   **SLI, SLO, và Ngân sách Lỗi (Error Budgets):** SRE cung cấp một khung làm việc toán học cho độ tin cậy.
		
        -   **SLI (Service Level Indicator - Chỉ số Cấp độ Dịch vụ):** Một thước đo định lượng về một khía cạnh nào đó của dịch vụ (ví dụ: độ trễ yêu cầu, tỷ lệ lỗi).
			
        -   **SLO (Service Level Objective - Mục tiêu Cấp độ Dịch vụ):** Một giá trị mục tiêu cho một SLI trong một khoảng thời gian (ví dụ: 99.9% yêu cầu được phục vụ trong <200ms).
			
        -   **Error Budget (Ngân sách Lỗi):** Là phần nghịch đảo của SLO (100%−SLO). Đây là lượng "không đáng tin cậy" mà nhóm được phép "tiêu thụ". Nếu ngân sách lỗi còn dương, nhóm có thể phát hành tính năng mới. Nếu nó cạn kiệt, mọi công việc phải chuyển sang cải thiện độ tin cậy.
		
    -   **SRE và DevOps:** SRE trả lời câu hỏi "làm thế nào" cho cái "gì" của DevOps.
	
-   **GitOps:** Sự tiến hóa của IaC và CI/CD. Git là **nguồn chân lý duy nhất (single source of truth)** cho _toàn bộ_ trạng thái hệ thống (hạ tầng và ứng dụng).
	
    -   **Quy trình làm việc:** Các thay đổi được thực hiện thông qua Pull Request đến một kho chứa Git. Một agent bên trong cụm Kubernetes (như Argo CD hoặc Flux) liên tục so sánh trạng thái thực tế với trạng thái được khai báo trong Git và tự động điều chỉnh bất kỳ sự khác biệt nào.
		
    -   **Argo CD và Flux:** Argo CD giống một nền tảng hoàn chỉnh, có giao diện người dùng, trong khi Flux là một bộ công cụ mô-đun hơn, tập trung vào dòng lệnh và thường được coi là gần gũi hơn với cách tiếp cận "thuần Kubernetes".
	
-   **Khả năng Quan sát (Observability):** Vượt ra ngoài việc giám sát đơn giản ("máy chủ có hoạt động không?") để đạt đến sự hiểu biết sâu sắc về hệ thống ("tại sao máy chủ lại chậm đối với người dùng ở khu vực cụ thể này?").
	
    -   **Ba Trụ cột của Observability:**
		
        -   **Logs:** Các bản ghi chi tiết, có dấu thời gian về các sự kiện riêng lẻ.
			
        -   **Metrics:** Dữ liệu số, được tổng hợp theo thời gian (ví dụ: mức sử dụng CPU, số lượng yêu cầu).
			
        -   **Traces:** Cho thấy hành trình từ đầu đến cuối của một yêu cầu khi nó di chuyển qua một hệ thống phân tán.
		
    -   **Công cụ:** Các ngăn xếp công cụ phổ biến bao gồm Prometheus & Grafana để theo dõi số liệu và trực quan hóa, và ELK Stack (Elasticsearch, Logstash, Kibana) để quản lý nhật ký.
	
## Kết luận

### Hành động

-   **Đánh giá Mức độ Trưởng thành:** Các tổ chức nên sử dụng mô hình này để xác định vị trí hiện tại của nhóm mình.
	
-   **Tập trung vào Nút thắt Cổ chai Tiếp theo:** Thay vì cố gắng nhảy từ Cấp độ 0 lên Cấp độ 5, chìa khóa là xác định điểm yếu lớn nhất hiện tại và áp dụng các thực tiễn của cấp độ tiếp theo để giải quyết nó. Quá trình này nên diễn ra từ từ và có kế hoạch.
	
-   **Lộ trình Kỹ năng Tóm tắt:** Để phát triển cá nhân hoặc xây dựng đội ngũ, một lộ trình kỹ năng có cấu trúc là cần thiết:
	
    - **Nền tảng:** Ngôn ngữ lập trình (Python/Go), Linux/Shell Scripting, Git.
		
    -  **DevOps Cốt lõi:** Công cụ CI/CD (Jenkins, GitLab CI, GitHub Actions), IaC (Terraform), Containers (Docker).
		
    -  **Nâng cao/Cloud-Native:** Kubernetes, Nền tảng Đám mây (AWS/GCP/Azure), Giám sát/Quan sát (Prometheus, Grafana).
		
    -  **Tinh hoa/SRE:** Hiểu biết sâu về hệ thống phân tán, triển khai SLI/SLO, tự động hóa nâng cao.
	
---
