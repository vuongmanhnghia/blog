---
title: "Docker Dockerfile"
date: 2025-08-14
image: "/images/image-placeholder.png"
categories: ["devops"]
tags: ["docker"]
draft: false
---

Nghệ Thuật Viết Dockerfile - Tối Ưu và Bảo Mật

<!--more-->

Phần 1: [Docker Principle](https://blog.nagih.io.vn/post/docker/docker/)

Phần 2: [Docker CLI](https://blog.nagih.io.vn/post/docker/docker-cli/)

## Phần 3: Nghệ Thuật Viết Dockerfile - Tối Ưu và Bảo Mật

`Dockerfile` là một tệp văn bản chứa một loạt các chỉ thị, hướng dẫn Docker cách xây dựng một image. Viết một `Dockerfile` tốt không chỉ là làm cho nó hoạt động, mà còn là về việc tạo ra các image nhỏ gọn, an toàn và xây dựng nhanh chóng.

### 3.1. Cấu trúc và các chỉ thị quan trọng

Một `Dockerfile` điển hình bao gồm các chỉ thị sau 48:

-   `FROM`: Luôn là chỉ thị đầu tiên. Nó xác định image cơ sở (base image) mà bạn sẽ xây dựng lên trên. Ví dụ: `FROM python:3.9-slim`.
-   `WORKDIR`: Thiết lập thư mục làm việc cho các chỉ thị tiếp theo như `RUN`, `COPY`, `CMD`. Nếu thư mục không tồn tại, nó sẽ được tạo. Ví dụ: `WORKDIR /app`.
-   `COPY`: Sao chép tệp và thư mục từ bối cảnh xây dựng (thư mục chứa `Dockerfile`) vào hệ thống tệp của image. Ví dụ: `COPY. /app`.
-   `RUN`: Thực thi các lệnh trong một lớp (layer) mới trên đỉnh của image hiện tại. Thường được sử dụng để cài đặt các gói phần mềm. Ví dụ: `RUN pip install -r requirements.txt`.
-   `EXPOSE`: Thông báo cho Docker rằng container sẽ lắng nghe trên các cổng mạng được chỉ định khi chạy. Đây chỉ là một hình thức tài liệu; nó không thực sự public cổng. Ví dụ: `EXPOSE 8000`.
-   `ENV`: Thiết lập các biến môi trường. Các biến này có sẵn cho các chỉ thị tiếp theo trong `Dockerfile` và cho ứng dụng khi container chạy. Ví dụ: `ENV APP_HOME /app`.
-   `ARG`: Định nghĩa các biến chỉ tồn tại trong quá trình xây dựng image (build-time). Chúng có thể được truyền vào từ dòng lệnh `docker build` với cờ `--build-arg`. Ví dụ: `ARG APP_VERSION=1.0`.

### 3.2. `CMD` vs. `ENTRYPOINT`

Đây là hai chỉ thị thường gây nhầm lẫn nhưng có mục đích khác nhau rõ rệt.

-   `ENTRYPOINT`: Cấu hình một container sẽ chạy như một tệp thực thi. Nó xác định lệnh chính sẽ luôn được thực thi khi container khởi động.
-   `CMD`: Cung cấp các đối số mặc định cho `ENTRYPOINT`. Nếu không có `ENTRYPOINT`, `CMD` sẽ được thực thi như lệnh chính.

Khi chạy `docker run my-image arg1 arg2`, các đối số `arg1 arg2` sẽ **ghi đè** hoàn toàn `CMD`, nhưng sẽ được **nối vào sau** `ENTRYPOINT`.

Cách sử dụng tốt nhất là kết hợp cả hai:

Sử dụng ENTRYPOINT để chỉ định tệp thực thi chính và CMD để cung cấp các đối số mặc định. Điều này tạo ra một image linh hoạt, cho phép người dùng dễ dàng truyền các đối số khác nhau mà không cần phải biết tên của tệp thực thi.

Ví dụ:

Dockerfile

```
ENTRYPOINT ["/usr/bin/python3", "app.py"]
CMD ["--mode", "production"]
```

-   `docker run my-image`: Sẽ chạy `/usr/bin/python3 app.py --mode production`.
-   `docker run my-image --mode debug`: Sẽ chạy `/usr/bin/python3 app.py --mode debug` (ghi đè `CMD`).

Cả hai chỉ thị nên được viết ở dạng "exec form" (mảng JSON) thay vì "shell form" (chuỗi lệnh) để tránh các vấn đề về phân tích cú pháp của shell và đảm bảo tín hiệu hệ thống được xử lý đúng cách.

### 3.3. `COPY` vs. `ADD`

Cả hai lệnh đều sao chép tệp vào image, nhưng có một sự khác biệt quan trọng.

-   `COPY`: Đơn giản và dễ đoán. Nó chỉ sao chép các tệp và thư mục cục bộ từ bối cảnh xây dựng vào container.
-   `ADD`: Có thêm hai tính năng "ma thuật":
    1. Nó có thể tải xuống tệp từ một URL.
    2. Nó có thể tự động giải nén các tệp lưu trữ (như tar, gzip) nếu nguồn là một tệp cục bộ.

**Cách sử dụng tốt nhất**: **Luôn ưu tiên `COPY`**. Sự rõ ràng và dễ đoán của

`COPY` làm cho `Dockerfile` của bạn dễ bảo trì hơn. Các tính năng bổ sung của `ADD` có thể dẫn đến hành vi không mong muốn, làm tăng kích thước image một cách không cần thiết và tạo ra các rủi ro bảo mật (ví dụ: tải xuống tệp từ một URL không đáng tin cậy). Chỉ sử dụng `ADD` khi bạn thực sự cần tính năng tự động giải nén một tệp tar cục bộ. Để tải xuống từ URL, cách tốt hơn là sử dụng `RUN curl...` hoặc `RUN wget...` để bạn có thể kiểm tra và dọn dẹp tệp trong cùng một lớp.

### 3.4. Tối ưu hóa kích thước Image với Multi-Stage Builds

Đây là kỹ thuật quan trọng nhất để tạo ra các image sản xuất nhỏ gọn và an toàn. Ý tưởng là tách biệt môi trường xây dựng (build environment) và môi trường chạy (runtime environment) trong cùng một `Dockerfile`.

-   **Cách hoạt động**: Một `Dockerfile` đa giai đoạn (multi-stage) có nhiều chỉ thị `FROM`. Mỗi `FROM` bắt đầu một giai đoạn mới.
    -   **Giai đoạn 1 (Build Stage)**: Bạn bắt đầu với một image lớn chứa tất cả các công cụ cần thiết để biên dịch ứng dụng của mình (ví dụ: `golang:1.24` hoặc `node:20`). Giai đoạn này được đặt tên bằng cách sử dụng `AS builder`.
    -   **Giai đoạn 2 (Final Stage)**: Bạn bắt đầu một giai đoạn mới với một image cơ sở tối giản, chỉ chứa những gì cần thiết để chạy ứng dụng (ví dụ: `scratch` - một image trống, hoặc `alpine` - một bản phân phối Linux siêu nhẹ).
    -   **Sao chép tạo phẩm**: Bạn sử dụng chỉ thị `COPY --from=builder <đường_dẫn_tạo_phẩm> <đích>` để sao chép chỉ kết quả biên dịch (ví dụ: một tệp nhị phân duy nhất) từ giai đoạn xây dựng vào giai đoạn cuối cùng.
-   **Lợi ích**: Image cuối cùng chỉ chứa ứng dụng đã biên dịch và các phụ thuộc thời gian chạy tối thiểu, loại bỏ hoàn toàn SDK, công cụ xây dựng và các tệp trung gian. Điều này giúp giảm đáng kể kích thước image (có thể từ hàng trăm MB xuống chỉ còn vài MB) và giảm bề mặt tấn công bảo mật.

### 3.5. Các phương pháp tốt nhất (Best Practices)

Một `Dockerfile` được viết tốt không chỉ là một tập lệnh; nó là một bản hợp đồng. Nó định nghĩa một cách tường minh trạng thái chính xác của môi trường ứng dụng. Khi kết hợp với việc ghim phiên bản cụ thể (ví dụ: `node:20.9.0-slim`), nó đảm bảo rằng bất kỳ ai, ở bất kỳ đâu, khi chạy `docker build` trên tệp này sẽ nhận được một image giống hệt nhau, từng bit một.5 Bản hợp đồng này là nền tảng của cơ sở hạ tầng bất biến (immutable infrastructure). Bạn không vá một container đang chạy (một "thú cưng"); bạn xây dựng một image mới, đã được vá từ bản hợp đồng đã cập nhật và triển khai một container mới (một "gia súc").

Dưới đây là một số quy tắc vàng để viết các `Dockerfile` chất lượng cao:

-   **Giảm thiểu số lớp (Limit Layers)**: Mỗi chỉ thị `RUN`, `COPY`, `ADD` tạo ra một lớp mới. Kết hợp các lệnh liên quan vào một chỉ thị `RUN` duy nhất bằng cách sử dụng `&&` để giảm số lượng lớp, giúp image nhỏ hơn.
-   **Tận dụng bộ đệm (Leverage Cache)**: Docker xây dựng image theo từng lớp và lưu vào bộ đệm. Để tận dụng tối đa bộ đệm, hãy sắp xếp các chỉ thị từ ít thay đổi nhất đến thay đổi thường xuyên nhất. Ví dụ, sao chép `package.json` và chạy `npm install` trước khi sao chép toàn bộ mã nguồn của bạn (`COPY..`).
-   **Sử dụng `.dockerignore`**: Tạo một tệp `.dockerignore` để loại trừ các tệp và thư mục không cần thiết (như `.git`, `node_modules`, các tệp nhật ký) khỏi bối cảnh xây dựng. Điều này giúp tăng tốc độ xây dựng và giữ cho image gọn gàng.
-   **Sử dụng thẻ cụ thể (Use Specific Tags)**: Tránh sử dụng thẻ `:latest`. Nó không thể đoán trước và có thể phá vỡ các bản dựng của bạn. Luôn sử dụng các thẻ phiên bản cụ thể (ví dụ: `python:3.9.7-slim`) để đảm bảo các bản dựng có thể tái tạo.
-   **Chạy với người dùng không phải root (Run as Non-Root User)**: Vì lý do bảo mật, hãy tránh chạy các container với người dùng `root`. Tạo một người dùng và nhóm riêng cho ứng dụng của bạn trong `Dockerfile` và chuyển sang người dùng đó bằng chỉ thị `USER`.

Phần 4: [Docker Compose](https://blog.nagih.io.vn/post/docker/docker-compose/)

Phần 5: [Docker Practical Guide](https://blog.nagih.io.vn/post/docker/docker-practical-guide/)

Phần 6: [Docker Fullstack Example](https://blog.nagih.io.vn/post/docker/docker-fullstack-example/)

Phần 7: [Docker Best Practice for Production](https://blog.nagih.io.vn/post/docker/docker-best-practice-for-production/)

---

_Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!_
