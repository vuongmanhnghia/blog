---
title: 6 Level Deploy
meta_title: 6 Level Deploy
description: 6 Cấp Độ Trưởng Thành Từ Deploy Thủ Công Đến Vận Hành Tinh Gọn
date: 2025-08-17
image: /images/image-placeholder.png
categories:
  - devops
  - CI/CD
author: Nagih
tags:
  - docker
draft: false
---
6 Cấp Độ Trưởng Thành Từ Deploy Thủ Công Đến Vận Hành Tinh Gọn
<!--more-->

## Hành Trình Trưởng Thành DevOps

Trong thế giới phát triển phần mềm hiện đại, DevOps không chỉ là một chức danh công việc mà là một triết lý văn hóa và một tập hợp các phương pháp kỹ thuật. Mục tiêu cốt lõi của DevOps là rút ngắn vòng đời phát triển phần mềm và cung cấp sản phẩm một cách liên tục với chất lượng cao, thông qua việc phá vỡ các rào cản giữa đội ngũ Phát triển (Development - Dev) và Vận hành (Operations - Ops), thúc đẩy sự hợp tác, chia sẻ trách nhiệm và giao tiếp hiệu quả

Trước khi bắt đầu, cần phải làm rõ một sự khác biệt nền tảng nhưng thường bị nhầm lẫn: "Deployment" (Triển khai) và "Release" (Phát hành).

- **Deployment** là một hoạt động _kỹ thuật_, bao gồm việc di chuyển mã nguồn từ môi trường này sang môi trường khác, ví dụ từ staging lên production. Đây là một quy trình vận hành thuần túy, tập trung vào việc đảm bảo mã nguồn chạy đúng trong môi trường mới.
    
- **Release** là một quyết định _kinh doanh_, liên quan đến việc cung cấp các tính năng mới cho người dùng. Quá trình này có thể bao gồm các hoạt động marketing, đào tạo người dùng, hoặc tung ra theo từng giai đoạn. Một tính năng có thể được "deploy" lên production nhiều lần nhưng ẩn sau một "feature flag" (cờ tính năng) và chỉ được "release" khi có quyết định từ phía kinh doanh.
    

Hiểu rõ sự khác biệt này là chìa khóa để nhận ra rằng toàn bộ hành trình trưởng thành của DevOps về cơ bản là một cuộc tìm kiếm không ngừng nhằm quản lý và giảm thiểu rủi ro, đồng thời tăng tốc độ cung cấp giá trị cho người dùng. Mỗi cấp độ đại diện cho một chiến lược quản lý rủi ro ngày càng tinh vi hơn. Ở cấp độ thấp nhất, rủi ro cực kỳ cao, một phương pháp kém hiệu quả. Các cấp độ tiếp theo lần lượt giảm thiểu rủi ro từ lỗi con người, lỗi tích hợp, sự không nhất quán của môi trường, cho đến các lỗi vận hành hệ thống phân tán. 

## Cấp độ 0: Deploy Thủ Công

Đây là vạch xuất phát, điểm khởi đầu hỗn loạn của nhiều tổ chức. Các quy trình ở cấp độ này chủ yếu là thủ công, bị động và không có tài liệu rõ ràng.

### Thực tiễn, Công cụ và Quy trình

- **Quy trình thủ công:** Việc triển khai được thực hiện bằng cách kết nối thủ công đến máy chủ thông qua các giao thức như FTP, SCP, hoặc SSH, sau đó sao chép từng tệp. Hoàn toàn không có tự động hóa.
    
- **Quản lý mã nguồn hỗn loạn:** Nếu có sử dụng Git, quy trình làm việc thường là "Centralized Workflow", nơi mọi người đều đẩy (push) mã nguồn trực tiếp lên nhánh chính (`main` hoặc `master`), gây ra sự bất ổn định và khó theo dõi.
    
- **"Deployment Checklist" - Tia hy vọng đầu tiên:** Nỗ lực đầu tiên để tạo ra trật tự thường là một danh sách kiểm tra (checklist) thủ công. Đây là một tài liệu liệt kê các bước cần tuân theo, từ việc sao lưu cơ sở dữ liệu đến việc khởi động lại dịch vụ. Dù thô sơ, đây là bước quan trọng đầu tiên hướng tới việc chuẩn hóa quy trình.
    

### Rủi ro và Nỗi đau

- **Rủi ro bảo mật thảm khốc:** Giao thức FTP truyền thông tin đăng nhập (username, password) dưới dạng văn bản thuần (plain text), khiến chúng dễ dàng bị "bắt" bởi bất kỳ ai trên mạng. Dữ liệu truyền đi cũng không được mã hóa, có nguy cơ bị tấn công xen giữa (man-in-the-middle), nơi kẻ tấn công có thể chèn mã độc vào các tệp đang được triển khai mà không bị phát hiện.
    
- **Hệ thống cực kỳ mong manh:** Quy trình này rất dễ xảy ra lỗi. Chỉ cần quên một tệp, sao chép sai thư mục, hoặc một tệp truyền bị lỗi cũng có thể làm sập toàn bộ hệ thống.
    
- **Không có cơ chế Rollback đáng tin cậy:** Khi một lần triển khai thất bại, không có cách nào dễ dàng và tự động để quay trở lại phiên bản ổn định trước đó. "Rollback" lại là một quy trình thủ công điên cuồng khác, cố gắng khôi phục phiên bản cũ dưới áp lực cực lớn.
    
- **Cái giá phải trả của con người:** Cấp độ này gây ra căng thẳng cực độ, kiệt sức và một nền văn hóa sợ hãi xung quanh việc triển khai. Các bản phát hành trở nên hiếm hoi, đồ sộ và đầy rủi ro.
    

## Cấp độ 1: Tự Động Hóa Bằng Script và Quản Lý Mã Nguồn Có Cấu Trúc

Khi nỗi đau của Cấp độ 0 trở nên không thể chịu đựng được, tổ chức buộc phải thực hiện bước tiến thực sự đầu tiên hướng tới tự động hóa. Trọng tâm lúc này là làm cho quy trình thủ công hiện có trở nên lặp lại được và ít bị lỗi hơn bằng cách viết script cho nó.

### Thực tiễn, Công cụ và Quy trình

- **Sự ra đời của Script triển khai:** "Deployment checklist" từ Cấp độ 0 được mã hóa thành một kịch bản (script) triển khai đơn giản, thường sử dụng Bash. Script này tự động hóa các bước kết nối đến máy chủ, lấy mã nguồn mới nhất từ kho chứa, và khởi động lại các dịch vụ.
    
- **Quy trình Git có cấu trúc:** Nhóm nhận ra rằng việc đẩy trực tiếp lên nhánh `main` là không bền vững. Họ áp dụng một chiến lược phân nhánh chính thức, phổ biến nhất là **Feature Branch Workflow**.
    
    - Nhánh `main` giờ đây được coi là "bất khả xâm phạm" và luôn ở trạng thái sẵn sàng để triển khai.
        
    - Tất cả công việc mới (tính năng, sửa lỗi) được thực hiện trên các nhánh riêng biệt.
        
    - Các thay đổi được tích hợp trở lại vào `main` thông qua Pull Request (hoặc Merge Request), cho phép thực hiện quy trình đánh giá mã nguồn (code review).
        

### Lợi ích và Những Vấn đề Còn Tồn Tại

- **Lợi ích:** Bản thân quy trình triển khai giờ đây đã đáng tin cậy và nhất quán hơn. Nhánh `main` ổn định hơn. Việc đánh giá mã nguồn giúp cải thiện chất lượng.
    
- **Vấn đề còn tồn tại:** Đây là một hình thức tự động hóa mong manh. Script không xử lý tốt các trường hợp thất bại. Không có kiểm thử tự động—lỗi vẫn được triển khai, chỉ là một cách nhất quán hơn. Các môi trường (development, staging, production) vẫn được cấu hình thủ công và không nhất quán, dẫn đến vấn đề kinh điển "nó chạy trên máy của tôi".
    

Tự động hóa quy trình triển khai không giải quyết được tất cả các vấn đề; nó chỉ làm cho chúng lộ ra rõ ràng hơn. Script bây giờ có thể triển khai một cách đáng tin cậy mã nguồn bị lỗi, hoặc thất bại vì môi trường production khác với môi trường staging. Nút thắt cổ chai không còn là các bước triển khai thủ công nữa, mà là sự thiếu vắng các cổng kiểm soát chất lượng tự động và tính nhất quán của môi trường. Khi nhóm tạo một script để tự động hóa việc triển khai, script có thể chạy nhưng ứng dụng được triển khai lại bị hỏng. Nhóm nhận ra họ không có các bài kiểm thử tự động để phát hiện lỗi trước khi triển khai. Hoặc, script chạy hoàn hảo trong môi trường staging nhưng lại thất bại trong môi trường production vì phiên bản thư viện khác nhau hoặc thiếu một cấu hình nào đó. Nhóm đi đến kết luận rằng chỉ một script là không đủ. Họ cần một hệ thống có khả năng

_tích hợp_ và _kiểm thử_ mã nguồn một cách tự động và đảm bảo các môi trường phải giống hệt nhau. Nhận thức này chính là chất xúc tác trực tiếp để áp dụng CI/CD và IaC.

## Cấp độ 2: Tích Hợp và Phân Phối Liên Tục (CI/CD)

Đây là một bước nhảy vọt về mức độ trưởng thành. Trọng tâm chuyển từ một script triển khai đơn lẻ sang một **đường ống (pipeline)** tự động hóa hoàn toàn, hoạt động như một "nhà máy" trung tâm cho việc phân phối phần mềm. Đây là nơi thế giới "Dev" và "Ops" thực sự bắt đầu hợp nhất.

### Các Khái Niệm Cốt Lõi

- **Tích hợp Liên tục (Continuous Integration - CI):** Là thực tiễn tự động hóa việc tích hợp các thay đổi mã nguồn từ nhiều nhà phát triển vào một dự án duy nhất. Mỗi lần đẩy mã nguồn lên một nhánh sẽ kích hoạt một quy trình xây dựng (build) tự động và một bộ các bài kiểm thử tự động (unit test, integration test). Điều này cung cấp phản hồi nhanh chóng và ngăn chặn "địa ngục tích hợp" (integration hell).
    
- **Phân phối Liên tục (Continuous Delivery - CD):** Là một phần mở rộng của CI. Sau khi các giai đoạn xây dựng và kiểm thử thành công, phần mềm sẽ được đóng gói và triển khai tự động đến một hoặc nhiều môi trường phi sản xuất (như staging). Việc triển khai lên production thường là một bước thủ công, chỉ cần một cú nhấp chuột.
    
- **Triển khai Liên tục (Continuous Deployment - cũng là CD):** Là hình thức tiên tiến nhất, nơi mọi thay đổi vượt qua tất cả các bài kiểm thử tự động đều được _triển khai tự động_ lên production mà không cần sự can thiệp của con người.
    

Đường ống CI/CD là một chuỗi các bước đã được thiết lập mà các nhà phát triển phải tuân theo để cung cấp một phiên bản phần mềm mới. Nó tự động hóa các giai đoạn từ phát triển, kiểm thử, đến sản xuất và giám sát, giúp các nhóm phát triển mã chất lượng cao hơn, nhanh hơn và an toàn hơn. Các giai đoạn điển hình bao gồm: Source (lấy mã nguồn), Build (biên dịch và đóng gói), Test (chạy các bài kiểm thử tự động), và Deploy (triển khai đến các môi trường).

### Công cụ

Việc lựa chọn một công cụ CI/CD là một quyết định quan trọng ở giai đoạn này. Bảng dưới đây so sánh các lựa chọn phổ biến nhất.

| Tính năng                       | Jenkins                                                                                              | GitLab CI                                                                                     | GitHub Actions                                                                                 |
| ------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Thiết lập & Lưu trữ**         | Cần cài đặt thủ công, thiết lập agent, tự lưu trữ (on-premise/cloud).                                | Tích hợp sẵn trong GitLab, không cần cài đặt riêng.                                           | Tích hợp sẵn trong GitHub, không cần cài đặt riêng.                                            |
| **Cấu hình**                    | Jenkinsfile (viết bằng Groovy) hoặc qua giao diện người dùng (UI).                                   | Tệp YAML (`.gitlab-ci.yml`) trong kho mã nguồn.                                               | Tệp YAML trong thư mục `.github/workflows`.                                                    |
| **Hệ sinh thái & Mở rộng**      | Cực kỳ mạnh mẽ với hơn 1800 plugin, tùy biến cao nhưng có thể phức tạp và dễ gặp vấn đề tương thích. | Tích hợp sâu với các tính năng của GitLab. Hệ sinh thái plugin nhỏ hơn Jenkins.               | Thị trường (Marketplace) rộng lớn với các "Actions" tái sử dụng. Dễ dàng tạo action tùy chỉnh. |
| **Trường hợp sử dụng lý tưởng** | Các quy trình phức tạp, yêu cầu tùy biến sâu, môi trường on-premise hoặc các hệ thống cũ (legacy).   | Các nhóm đã và đang sử dụng GitLab làm nền tảng chính, muốn một giải pháp "tất cả trong một". | Các nhóm ưu tiên GitHub, dự án mã nguồn mở, startup, cần sự đơn giản và khởi đầu nhanh chóng.  |

### Lợi ích và Thách thức Mới

- **Lợi ích:** Vòng lặp phản hồi nhanh hơn đáng kể, chất lượng mã nguồn được cải thiện, giảm rủi ro triển khai và tăng năng suất của nhà phát triển.
    
- **Thách thức:** Bản thân "đường ống CI/CD" trở thành một phần mềm phức tạp cần được bảo trì. Các nhóm giờ đây phải đối mặt với những vấn đề mới như các bài kiểm thử chạy chậm hoặc không ổn định (flaky tests), quản lý các phụ thuộc phức tạp, và vấn đề dai dẳng về "trôi dạt môi trường" (environment drift), nơi môi trường staging và production không giống hệt nhau.
    

## Cấp độ 3: Hạ Tầng Dưới Dạng Mã (IaC) và Container Hóa

Để giải quyết vấn đề trôi dạt môi trường và làm cho việc quản lý hạ tầng trở nên nghiêm ngặt như phát triển ứng dụng, các nhóm áp dụng triết lý "mọi thứ đều là mã nguồn".

### Các Khái Niệm Cốt Lõi

- **Hạ tầng dưới dạng mã (Infrastructure as Code - IaC):** Là việc quản lý và cấp phát hạ tầng (máy chủ, mạng, cơ sở dữ liệu) thông qua các tệp định nghĩa mà máy có thể đọc được (mã nguồn), thay vì cấu hình thủ công. Có hai cách tiếp cận chính:
    
    - **Khai báo (Declarative - "Cái gì"):** Bạn định nghĩa _trạng thái cuối cùng_ mong muốn của hạ tầng. Công cụ (ví dụ: Terraform) sẽ tự tìm cách để đạt được trạng thái đó. Đây là cách tiếp cận chủ đạo trong IaC hiện đại.
        
    - **Mệnh lệnh (Imperative - "Như thế nào"):** Bạn viết các kịch bản chỉ định các _bước chính xác_ cần thực hiện để cấu hình hạ tầng (ví dụ: Ansible, Chef, Puppet).
        
        Sự chuyển đổi sang IaC khai báo là một bước nhảy vọt về mặt khái niệm. Nó chuyển từ "chạy các lệnh này" sang "đảm bảo trạng thái này", một phương pháp mạnh mẽ, tự tài liệu hóa và có tính bất biến (idempotent) hơn.
        
- **Container hóa với Docker:** Là người bạn đồng hành hoàn hảo của IaC. Docker giải quyết vấn đề "nó chạy trên máy của tôi" bằng cách đóng gói một ứng dụng và tất cả các phụ thuộc của nó vào một đơn vị duy nhất, được tiêu chuẩn hóa và bị cô lập gọi là **container**.
    
    - **Dockerfile:** "Công thức" hay bản thiết kế để xây dựng một image.
        
    - **Image:** Một mẫu chỉ đọc (read-only) chứa ứng dụng và môi trường của nó.
        
    - **Container:** Một thực thể đang chạy (running instance) của một image. Nó nhẹ và có tính di động cao.
        

### Quy trình Mới

Đường ống CI/CD được nâng cấp. Nó không còn chỉ triển khai mã nguồn; nó xây dựng một Docker image (một tạo phẩm nhất quán được đảm bảo) và sử dụng các công cụ IaC như Terraform để cấp phát một môi trường giống hệt nơi container sẽ chạy.

### Lợi ích và Nút thắt Cổ chai Tiếp theo

- **Lợi ích:** Vấn đề trôi dạt môi trường được loại bỏ. Các lần triển khai giờ đây có tính nhất quán và độ tin cậy cao trên các môi trường dev, staging và production. Các thay đổi về hạ tầng được quản lý phiên bản, được đánh giá và có thể kiểm tra lại.
    
- **Nút thắt cổ chai tiếp theo:** Tổ chức bây giờ đã thành công và có hàng trăm hoặc hàng nghìn container. Làm thế nào để quản lý chúng? Làm thế nào để xử lý mạng, mở rộng quy mô và kiểm tra sức khỏe cho tất cả các container này? Đây là vấn đề của việc **điều phối (orchestration)**.
    

## Cấp độ 4: Điều Phối Container và Kiến Trúc Cloud-Native

Trọng tâm chuyển từ việc quản lý các container riêng lẻ sang quản lý một ứng dụng phân tán bao gồm nhiều container ở quy mô lớn. Điều này đòi hỏi một "nhạc trưởng" cho "dàn nhạc" container.

### Các Khái Niệm Cốt Lõi: Kubernetes (K8s)

- **Kubernetes là gì:** Là hệ thống mã nguồn mở, tiêu chuẩn de-facto của ngành công nghiệp, dùng để tự động hóa việc triển khai, mở rộng quy mô và quản lý các ứng dụng được container hóa. Nó giải quyết vấn đề chạy các hệ thống phân tán một cách linh hoạt và có khả năng phục hồi.
    
- **Các đối tượng Kubernetes chính (Đơn giản hóa cho người mới bắt đầu):**
    
    - **Pod:** Đơn vị triển khai nhỏ nhất, cơ bản nhất trong Kubernetes. Nó là một lớp vỏ bọc quanh một hoặc nhiều container, chia sẻ tài nguyên lưu trữ và mạng. Hãy coi nó như "nguyên tử" cơ bản của một ứng dụng K8s.
        
    - **Deployment:** Một đối tượng cấp cao hơn mô tả _trạng thái mong muốn_ cho ứng dụng của bạn. Nó nói với Kubernetes rằng "Tôi muốn có 3 bản sao (replica) của pod máy chủ web của tôi chạy mọi lúc." Bộ điều khiển Deployment (Deployment Controller) sẽ làm việc để biến trạng thái này thành hiện thực.
        
    - **Service:** Một lớp trừu tượng định nghĩa một tập hợp logic các Pod và một chính sách để truy cập chúng. Nó cung cấp một địa chỉ IP và tên DNS ổn định, để các phần khác của ứng dụng (hoặc người dùng bên ngoài) có thể kết nối đến các Pod, ngay cả khi chúng được tạo ra và phá hủy.
        

### Lợi ích và Sự Phức Tạp Mới

- **Lợi ích:** Tổ chức đạt được khả năng mở rộng quy mô thực sự, tự phục hồi (Kubernetes tự động khởi động lại các container bị lỗi), và tính sẵn sàng cao. Các bản cập nhật và quay lui (rolling updates and rollbacks) giờ đây được quản lý một cách khai báo và an toàn.
    
- **Sự phức tạp mới:** Bản thân Kubernetes là một hệ thống cực kỳ phức tạp. Việc học nó rất khó khăn. Quản lý, giám sát và bảo mật một cụm Kubernetes (cluster) trở thành một công việc toàn thời gian. Thách thức mới không còn là "làm thế nào để chạy ứng dụng của chúng ta?" mà là "làm thế nào để chạy Kubernetes một cách đáng tin cậy?"
    

Kubernetes về cơ bản đã đảo ngược mô hình vận hành. Trước K8s, các nhóm Ops chịu trách nhiệm _làm cho mọi thứ hoạt động_. Với K8s, trách nhiệm của nhà phát triển mở rộng đến việc _khai báo cách mọi thứ nên hoạt động_ (thông qua các tệp kê khai YAML), và bộ điều khiển của K8s trở thành "đội ngũ Ops" tự động thực thi các khai báo đó. Để làm được điều này, nhà phát triển phải viết một tệp `Deployment.yaml` chỉ định image container, số lượng bản sao và yêu cầu tài nguyên. Tệp YAML này là một hợp đồng, là cách nhà phát triển nói với cụm máy chủ (và qua đó là nhóm Ops quản lý cụm máy chủ) chính xác những gì họ cần. Điều này đòi hỏi nhà phát triển phải có hiểu biết sâu sắc hơn về các vấn đề vận hành (giới hạn tài nguyên, kiểm tra sức khỏe, v.v.), và đòi hỏi nhóm Ops phải cung cấp một nền tảng đáng tin cậy (cụm máy chủ) để các khai báo này có thể chạy. Trách nhiệm chung này chính là bản chất của DevOps trưởng thành.

## Cấp độ 5: Vận Hành Dựa Trên Dữ Liệu (SRE, GitOps, & Observability)

Đây là cấp độ trưởng thành cao nhất. Các hoạt động vận hành không còn là bị động hay thậm chí chỉ là tự động; chúng trở nên chủ động, được điều khiển bằng dữ liệu và được xem như một ngành kỹ thuật phần mềm.

### Các Khái Niệm Cốt Lõi

- **Kỹ thuật Đảm bảo Độ tin cậy của Hệ thống (Site Reliability Engineering - SRE):** Một phương pháp triển khai cụ thể của DevOps, bắt nguồn từ Google. Nó coi các vấn đề vận hành như những bài toán phần mềm.
    
    - **SLI, SLO, và Ngân sách Lỗi (Error Budgets):** SRE cung cấp một khung làm việc toán học cho độ tin cậy.
        
        - **SLI (Service Level Indicator - Chỉ số Cấp độ Dịch vụ):** Một thước đo định lượng về một khía cạnh nào đó của dịch vụ (ví dụ: độ trễ yêu cầu, tỷ lệ lỗi).
            
        - **SLO (Service Level Objective - Mục tiêu Cấp độ Dịch vụ):** Một giá trị mục tiêu cho một SLI trong một khoảng thời gian (ví dụ: 99.9% yêu cầu được phục vụ trong <200ms).
            
        - **Error Budget (Ngân sách Lỗi):** Là phần nghịch đảo của SLO (100%−SLO). Đây là lượng "không đáng tin cậy" mà nhóm được phép "tiêu thụ". Nếu ngân sách lỗi còn dương, nhóm có thể phát hành tính năng mới. Nếu nó cạn kiệt, mọi công việc phải chuyển sang cải thiện độ tin cậy. Đây là một cách tiếp cận dựa trên dữ liệu để cân bằng giữa đổi mới và sự ổn định.
            
    - **SRE và DevOps:** DevOps là triết lý văn hóa; SRE là một cách cụ thể, có chính kiến để thực hiện nó. SRE trả lời câu hỏi "làm thế nào" cho cái "gì" của DevOps.
        
- **GitOps:** Sự tiến hóa của IaC và CI/CD. Git là **nguồn chân lý duy nhất (single source of truth)** cho _toàn bộ_ trạng thái hệ thống (hạ tầng và ứng dụng).
    
    - **Quy trình làm việc:** Các thay đổi được thực hiện thông qua Pull Request đến một kho chứa Git. Một agent bên trong cụm Kubernetes (như Argo CD hoặc Flux) liên tục so sánh trạng thái thực tế với trạng thái được khai báo trong Git và tự động điều chỉnh bất kỳ sự khác biệt nào.
        
    - **Argo CD và Flux:** Argo CD giống một nền tảng hoàn chỉnh, có giao diện người dùng, trong khi Flux là một bộ công cụ mô-đun hơn, tập trung vào dòng lệnh và thường được coi là gần gũi hơn với cách tiếp cận "thuần Kubernetes".
        
- **Khả năng Quan sát (Observability):** Vượt ra ngoài việc giám sát đơn giản ("máy chủ có hoạt động không?") để đạt đến sự hiểu biết sâu sắc về hệ thống ("tại sao máy chủ lại chậm đối với người dùng ở khu vực cụ thể này?").
    
    - **Ba Trụ cột của Observability:**
        
        - **Logs (Nhật ký):** Các bản ghi chi tiết, có dấu thời gian về các sự kiện riêng lẻ.
            
        - **Metrics (Số liệu):** Dữ liệu số, được tổng hợp theo thời gian (ví dụ: mức sử dụng CPU, số lượng yêu cầu).
            
        - **Traces (Dấu vết):** Cho thấy hành trình từ đầu đến cuối của một yêu cầu khi nó di chuyển qua một hệ thống phân tán.
            
    - **Công cụ:** Các ngăn xếp công cụ phổ biến bao gồm Prometheus & Grafana để theo dõi số liệu và trực quan hóa, và ELK Stack (Elasticsearch, Logstash, Kibana) để quản lý nhật ký.
        

Ở cấp độ tinh hoa, SRE, GitOps và Observability không phải là các ngành riêng biệt; chúng là một vòng lặp tích hợp chặt chẽ, tự củng cố lẫn nhau. Observability cung cấp dữ liệu thô (SLI) cần thiết để xác định SLO và ngân sách lỗi của SRE. Quy trình SRE sử dụng ngân sách lỗi để quyết định _khi nào_ an toàn để phê duyệt một thay đổi. Thay đổi đó được đề xuất và thực thi thông qua quy trình GitOps (một pull request). Khi công cụ GitOps áp dụng thay đổi, các công cụ Observability sẽ giám sát tác động của nó, cung cấp dữ liệu mới trở lại cho các SLI. Điều này tạo ra một hệ thống vòng kín, dựa trên dữ liệu để quản lý một môi trường production phức tạp, đó là mục tiêu cuối cùng của DevOps.

## Kết luận
### Lời khuyên Hành động

- **Đánh giá Mức độ Trưởng thành:** Các tổ chức nên sử dụng mô hình này để xác định vị trí hiện tại của nhóm mình.
    
- **Tập trung vào Nút thắt Cổ chai Tiếp theo:** Thay vì cố gắng nhảy từ Cấp độ 0 lên Cấp độ 5, chìa khóa là xác định điểm yếu lớn nhất hiện tại và áp dụng các thực tiễn của cấp độ tiếp theo để giải quyết nó. Quá trình này nên diễn ra từ từ và có kế hoạch.
    
- **Lộ trình Kỹ năng Tóm tắt:** Để phát triển cá nhân hoặc xây dựng đội ngũ, một lộ trình kỹ năng có cấu trúc là cần thiết:
    
    1. **Nền tảng:** Ngôn ngữ lập trình (Python/Go), Linux/Shell Scripting, Git.
        
    2. **DevOps Cốt lõi:** Công cụ CI/CD (Jenkins, GitLab CI, GitHub Actions), IaC (Terraform), Containers (Docker).
        
    3. **Nâng cao/Cloud-Native:** Kubernetes, Nền tảng Đám mây (AWS/GCP/Azure), Giám sát/Quan sát (Prometheus, Grafana).
        
    4. **Tinh hoa/SRE:** Hiểu biết sâu về hệ thống phân tán, triển khai SLI/SLO, tự động hóa nâng cao.
        

### Tương lai: Kỹ thuật Nền tảng (Platform Engineering)

Đối với các tổ chức trưởng thành, mục tiêu của một nhóm DevOps/SRE trung tâm không phải là tự mình làm mọi thứ, mà là _tạo điều kiện_ cho tất cả các nhà phát triển khác. Đây chính là vai trò của **Kỹ thuật Nền tảng**.

Một nhóm Kỹ thuật Nền tảng xây dựng một "Nền tảng Nhà phát triển Nội bộ" (Internal Developer Platform - IDP) cung cấp một "con đường trải nhựa" cho các nhóm phát triển sản phẩm. Họ cung cấp các công cụ tự phục vụ, được tiêu chuẩn hóa cho CI/CD, cấp phát hạ tầng, giám sát và triển khai. Điều này cho phép các nhà phát triển sản phẩm triển khai mã nguồn một cách nhanh chóng và an toàn mà không cần phải là chuyên gia về Kubernetes hay Terraform. Cách tiếp cận này giúp nhân rộng các lợi ích của Cấp độ 5 trên toàn bộ tổ chức, và đây chính là đích đến cuối cùng của quá trình chuyển đổi DevOps.

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*
