---
title: "Microservices"
date: 2025-08-07
image: "/images/image-placeholder.png"
categories: ["system", "microservices"]
tags: [""]
draft: false
---

Tổng quan về kiến trúc microservices

<!--more-->

### 1. Kiến trúc Microservices là gì?

Hãy tưởng tượng bạn đang xây một ngôi nhà.

-   **Kiến trúc nguyên khối (Monolith):** Bạn xây toàn bộ ngôi nhà bằng một khối bê tông khổng lồ duy nhất. Mọi thứ dính liền với nhau. Nếu bạn muốn sửa đường ống nước trong bếp, bạn có thể phải đục cả bức tường lớn, ảnh hưởng đến phòng khách bên cạnh.

-   **Kiến trúc Microservices:** Bạn xây ngôi nhà bằng những viên gạch LEGO. Mỗi phòng (phòng khách, phòng ngủ, nhà bếp) là một khối LEGO riêng. Nếu muốn sửa bếp, bạn chỉ cần nhấc khối LEGO "nhà bếp" ra, sửa nó, rồi đặt lại mà không ảnh hưởng gì đến các phòng khác.

Trong phần mềm, **kiến trúc microservices** là phương pháp chia một ứng dụng lớn thành **nhiều dịch vụ (service) nhỏ, độc lập**. Mỗi service đảm nhiệm một chức năng cụ thể, có database riêng, và được phát triển, triển khai, nâng cấp độc lập với các service khác.

![Image Description](blog.nagih.io.vn/posts/imagespasted-image-20250807092251png)

### 2. Các Service giao tiếp với nhau ra sao? Có giống Frontend gọi tới Backend không?

Đây là câu hỏi cốt lõi và quan trọng nhất. Các service (vốn là các backend) giao tiếp với nhau qua mạng. Có hai kiểu giao tiếp chính:

#### **Giao tiếp Đồng bộ (Synchronous)**

Giống như một cuộc gọi điện thoại. Service A gọi đến Service B và phải **chờ** Service B trả lời rồi mới làm việc tiếp.

-   **Cách thức:** Thường sử dụng các giao thức như **REST API (qua HTTP/S)** hoặc **gRPC**.
-   **Ví dụ:** Khi bạn đặt hàng, `Service Đơn Hàng` sẽ gọi trực tiếp đến `Service Kho Hàng` để hỏi "Sản phẩm X còn hàng không?". `Service Đơn Hàng` sẽ phải đợi câu trả lời từ `Service Kho Hàng` rồi mới cho phép khách đặt hàng.
-   **Giống Frontend gọi Backend không?** Về mặt kỹ thuật (dùng REST API) thì **giống**, nhưng bản chất là **khác**. Đây là giao tiếp **giữa các backend với nhau (backend-to-backend)**, diễn ra bên trong hệ thống mà người dùng không nhìn thấy.

#### **Giao tiếp Bất đồng bộ (Asynchronous)**

Giống như gửi email hoặc tin nhắn. Service A gửi một "thông điệp" (message) cho Service B rồi tiếp tục công việc của mình ngay lập tức, **không cần chờ** B trả lời. Service B sẽ nhận và xử lý thông điệp đó khi nào sẵn sàng.

-   **Cách thức:** Sử dụng một hệ thống trung gian gọi là **Message Broker** (hoặc Message Queue) như **RabbitMQ, Kafka**.
-   **Ví dụ:** Sau khi bạn đặt hàng thành công, `Service Đơn Hàng` sẽ gửi một thông điệp có nội dung "Đơn hàng #123 đã được tạo" vào một hàng đợi (queue). `Service Thông Báo` sẽ lắng nghe hàng đợi này, thấy có thông điệp mới liền lấy ra và gửi email xác nhận cho bạn. `Service Đơn Hàng` không cần quan tâm `Service Thông Báo` đã gửi email hay chưa.
-   **Ưu điểm:** Giúp các service **hoàn toàn độc lập** (decoupled). Nếu `Service Thông Báo` bị lỗi, các đơn hàng vẫn được tạo bình thường, các thông điệp sẽ nằm chờ trong queue để được xử lý sau.

---

### 3. Có phải Microservices là kiến trúc ở Backend? Frontend chỉ cần 1 service?

Đúng vậy, **Microservices chủ yếu là một kiến trúc cho phần backend**. Tuy nhiên, việc có nhiều service backend nhỏ lẻ lại tạo ra một vấn đề cho frontend: "Frontend nên gọi đến service nào?".

Không thể để frontend (ứng dụng web, mobile) gọi trực tiếp đến 10 service backend khác nhau. Điều này rất phức tạp, khó quản lý và không an toàn. Giải pháp phổ biến nhất là sử dụng một **API Gateway**.

#### **API Gateway là gì?**

Hãy coi API Gateway như một **anh chàng lễ tân** của toàn bộ hệ thống.

-   Frontend chỉ cần nói chuyện với "anh lễ tân" này thôi.
-   "Anh lễ tân" sẽ chịu trách nhiệm xác thực yêu cầu, sau đó xem xét yêu cầu này thuộc về phòng ban nào (service nào) và chuyển tiếp đến đúng nơi.
-   Nó cũng có thể tổng hợp thông tin từ nhiều service trước khi trả về cho frontend.

**Ví dụ:** Để hiển thị trang chi tiết sản phẩm, frontend chỉ cần gửi 1 yêu cầu duy nhất đến API Gateway. API Gateway sẽ tự động gọi đến `Service Sản Phẩm` để lấy thông tin sản phẩm và gọi đến `Service Đánh Giá` để lấy các bình luận, sau đó gộp hai kết quả này lại và trả về cho frontend.

Vậy câu trả lời là: **Backend được chia thành nhiều microservices, và thường có một lớp API Gateway làm điểm vào duy nhất cho tất cả các client (web, mobile...).**

---

### 4. Vấn đề về Dữ liệu: Mỗi Service một Database?

Đây là một trong những quy tắc vàng và cũng là thách thức lớn nhất của microservices: **Mỗi microservice phải sở hữu và quản lý cơ sở dữ liệu (database) của riêng mình.**

-   **Tại sao?** Để đảm bảo tính độc lập tuyệt đối. Nếu `Service A` và `Service B` dùng chung một database, khi `Service A` muốn thay đổi cấu trúc bảng, nó có thể làm sập `Service B`. Như vậy thì không còn gọi là độc lập nữa.
-   **Thách thức:** Làm sao để thực hiện một nghiệp vụ yêu cầu dữ liệu từ nhiều service? Ví dụ: làm sao để đảm bảo khi tạo đơn hàng (Service Đơn Hàng) thì số lượng tồn kho (Service Kho Hàng) cũng phải được trừ đi một cách nhất quán?
-   **Giải pháp:** Cần sử dụng các pattern nâng cao như **Saga Pattern** để quản lý các giao dịch phân tán (distributed transactions). Đây là một chủ đề phức tạp, nhưng ý tưởng cơ bản là mỗi service sẽ thực hiện phần việc của mình và phát ra sự kiện để service tiếp theo thực hiện phần việc của nó.

---

_Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!_
