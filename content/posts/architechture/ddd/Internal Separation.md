---
title: "Internal Separation"
date: 2025-08-29
image: "/images/image-placeholder.png"
categories: ["architechture", "microservices"]
tags: ["ddd"]
draft: false
---

Phân biệt rõ các tác vụ trong Internal

<!--more-->

Việc phân chia các tác vụ trong cấu trúc thư mục của một dự án DDD nhằm mục đích **tách biệt các mối quan tâm (Separation of Concerns)**. Mỗi lớp có một trách nhiệm duy nhất và các quy tắc phụ thuộc chặt chẽ.

Hãy tưởng tượng bạn đang xây một nhà hàng cao cấp:

-   **Domain:** Bếp trưởng và các công thức nấu ăn bí mật. Đây là trái tim, là giá trị cốt lõi.
-   **Application:** Người phục vụ nhận yêu cầu từ khách, chuyển cho bếp và mang món ăn ra. Họ điều phối, không nấu ăn.
-   **Infrastructure:** Hệ thống điện, nước, nhà cung cấp nguyên liệu. Họ cung cấp kỹ thuật và dịch vụ bên ngoài.
-   **Shared:** Các dụng cụ làm bếp cơ bản, gia vị chung, quy định an toàn vệ sinh. Ai cũng cần dùng.

## Domain Layer: Trái tim của nghiệp vụ

Đây là lớp quan trọng nhất, chứa đựng toàn bộ logic, quy tắc và mô hình của bài toán nghiệp vụ mà phần mềm đang giải quyết.

### Vai trò chính

-   Định nghĩa các khái niệm nghiệp vụ (ví dụ: `Order`, `Product`, `Customer`).
-   Thực thi các quy tắc nghiệp vụ (ví dụ: "một đơn hàng không thể có tổng giá trị âm", "khách hàng VIP được giảm giá 10%").
-   Đảm bảo trạng thái của các đối tượng luôn nhất quán và hợp lệ.

### Bao gồm những gì ?

-   **Entities & Aggregates:** Các đối tượng có định danh và vòng đời, là trung tâm của logic nghiệp vụ (ví dụ: `OrderAggregate`).
-   **Value Objects:** Các đối tượng mô tả thuộc tính, không có định danh (ví dụ: `Address`, `Money`).
-   **Domain Services:** Chứa các logic nghiệp vụ không thuộc về bất kỳ Entity nào.
-   **Repository Interfaces:** Các hợp đồng (interface) định nghĩa cách truy xuất dữ liệu, nhưng **không có code cài đặt**.
-   **Domain Events:** Các sự kiện xảy ra trong miền nghiệp vụ (ví dụ: `OrderPlacedEvent`).

### Quy tắc vàng

Lớp **Domain** không được phụ thuộc vào bất kỳ lớp nào khác. Nó hoàn toàn trong sáng và không biết gì về database, API hay giao diện người dùng.

## Application Layer: Bộ điều phối các tác vụ

Lớp này đóng vai trò như một kịch bản, điều phối các đối tượng trong lớp Domain để thực hiện một yêu cầu cụ thể từ bên ngoài (use case).

### Vai trò chính

-   Nhận yêu cầu từ bên ngoài (ví dụ: từ API Controller, UI).
-   Sử dụng các Repository để lấy ra các Aggregate từ database.
-   Gọi các phương thức trên Aggregate để thực thi logic nghiệp vụ.
-   Sử dụng Repository để lưu lại trạng thái của Aggregate.
-   Điều phối các tác vụ liên quan đến cơ sở hạ tầng (ví dụ: gửi email sau khi đặt hàng thành công).

### Bao gồm những gì ?

-   **Application Services:** Các class xử lý một use case cụ thể (ví dụ: `OrderService` với phương thức `PlaceOrder(PlaceOrderCommand)`).
-   **Commands & Queries:** Các đối tượng DTOs đại diện cho ý định thay đổi hệ thống hoặc truy vấn dữ liệu (mô hình CQRS).
-   **Data Transfer Objects (DTOs):** Các đối tượng dùng để truyền dữ liệu vào và ra khỏi lớp Application.

### Quy tắc vàng

Lớp **Application** **không chứa logic nghiệp vụ**. Nó chỉ điều phối. Nếu bạn thấy có câu lệnh `if/else` liên quan đến nghiệp vụ ở đây, rất có thể bạn đã đặt sai chỗ.

## Infrastructure Layer: Lớp keo dán kỹ thuật

Lớp này chứa tất cả các chi tiết kỹ thuật về việc giao tiếp với thế giới bên ngoài. Nó là phần cài đặt cụ thể cho các hợp đồng được định nghĩa ở lớp Domain và Application.

### Vai trò chính

-   Cung cấp các cài đặt cụ thể cho việc lưu trữ dữ liệu (database).
-   Tương tác với các hệ thống bên ngoài như message queue, dịch vụ email, hệ thống file, cache...
-   Triển khai các framework và thư viện cụ thể.

### Bao gồm những gì ?

-   **Repository Implementations:** Cài đặt cụ thể các Repository interface từ lớp Domain (ví dụ: `OrderRepository` sử dụng Entity Framework Core).
-   **ORM/Database Context:** Các class liên quan đến ORM như `DbContext`.
-   **File Access, Email Sender, Message Bus Clients...:** Các class cụ thể để làm việc với các dịch lỹ thuật.

### Quy tắc vàng

Lớp **Infrastructure** phụ thuộc vào **Domain** và **Application**, nhưng các lớp đó không biết gì về sự tồn tại của Infrastructure (thông qua nguyên lý Đảo ngược phụ thuộc - Dependency Inversion).

## Shared Kernel (hoặc Core/Shared): Hộp công cụ chung

Đây là một "lớp" đặc biệt, chứa các code và tiện ích được sử dụng chung bởi tất cả các lớp khác.

### Vai trò chính

-   Cung cấp các thành phần cơ sở, dùng chung để tránh lặp lại code.
-   Định nghĩa các hợp đồng hoặc hằng số dùng xuyên suốt dự án.

### Bao gồm những gì ?

-   Các lớp cơ sở (ví dụ: `BaseEntity`, `BaseRepository`).
-   Các hàm tiện ích (helper functions), các extension method.
-   Các Exception tùy chỉnh dùng chung.
-   Các thành phần cross-cutting concerns như logging, authentication contracts.

### Quy tắc vàng

Phải rất ổn định và ít khi thay đổi. Một thay đổi ở lớp này có thể ảnh hưởng đến toàn bộ dự án.

### **Bảng tóm tắt phân biệt**

| Lớp                | Trách nhiệm chính                              | Ví dụ thành phần                                              | "Không được phép" làm gì?                        |
| ------------------ | ---------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------ |
| **Domain**         | Trái tim nghiệp vụ, các quy tắc và mô hình     | `Aggregate`, `Entity`, `Value Object`, `Repository Interface` | Phụ thuộc vào các lớp khác; biết về database/UI. |
| **Application**    | Điều phối các tác vụ, xử lý use case           | `Application Service`, `Command`, `Query`, `DTO`              | Chứa logic nghiệp vụ.                            |
| **Infrastructure** | Cài đặt chi tiết kỹ thuật, giao tiếp bên ngoài | `EFCoreDbContext`, `OrderRepository (EF)`, `EmailSender`      | Chứa logic nghiệp vụ.                            |
| **Shared**         | Các tiện ích và code dùng chung                | `BaseEntity`, `Helper Functions`, `Custom Exceptions`         | Chứa logic cụ thể của một nghiệp vụ.             |

---

_Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!_
