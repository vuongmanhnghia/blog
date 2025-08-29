---
title: DDD (Domain-Driven Design)
date: 2025-08-27
draft: false
tags:
  - architechture
  - go
  - microservices
---
Architecture Overview Domain-Driven Design(DDD)
<!--more-->

## Phần I: Các Nguyên tắc Cốt lõi của DDD

### Thiết kế Chiến lược: Lập bản đồ Context Nghiệp vụ

#### Context Giới hạn (Bounded Contexts)

Các hệ thống lớn hiếm khi có một mô hình duy nhất, thống nhất. Thuật ngữ "Người dùng" có thể có ý nghĩa khác nhau trong layer "Xác thực" so với context "Hỗ trợ Kỹ thuật". Bounded Context là một ranh giới rõ ràng mà trong đó một mô hình miền cụ thể và Ngôn ngữ Phổ biến của nó là nhất quán và hợp lệ. Chiến lược "chia để trị" này là câu trả lời của DDD để quản lý sự phức tạp trong các tổ chức lớn. Việc xác định các context này là mục tiêu chính của Thiết kế Chiến lược và rất quan trọng để xác định ranh giới của các microservice.

Toàn bộ cấu trúc của một hệ thống phức tạp bắt nguồn trực tiếp từ những sự mơ hồ về ngôn ngữ được phát hiện trong quá trình thiết kế chiến lược. Quá trình này diễn ra như sau: đầu tiên, các chuyên gia lĩnh vực và nhà phát triển nhận ra rằng một thuật ngữ duy nhất (ví dụ: "Khách hàng") có nhiều ý nghĩa mâu thuẫn giữa các phòng ban (hiện tượng đa nghĩa). Xung đột ngôn ngữ này làm cho việc xây dựng một mô hình miền thống nhất duy nhất trở nên bất khả thi nếu không muốn tạo ra sự nhầm lẫn và lỗi. Để giải quyết vấn đề này, họ áp dụng mẫu Bounded Context, vẽ ra các ranh giới rõ ràng xung quanh các khu vực mà ngôn ngữ là nhất quán. Ví dụ, một "Context Bán hàng" và một "Context Hỗ trợ" được xác định. Các Bounded Context này sau đó trở thành những ứng cử viên tự nhiên cho các service hoặc module riêng biệt trong kiến trúc phần mềm. Do đó, kiến trúc ở cấp độ cao (ví dụ: việc phân chia thành các microservice) là một hệ quả trực tiếp của việc giải quyết các vấn đề giao tiếp và định nghĩa một Ngôn ngữ Phổ biến rõ ràng. Kiến trúc không phải là một quyết định kỹ thuật tùy tiện; nó là một giải pháp cho một vấn đề giao tiếp nghiệp vụ.

### Thiết kế Chiến thuật: Các Khối Xây dựng Miền

Thiết kế Chiến thuật cung cấp các mẫu để xây dựng một mô hình miền phong phú, biểu cảm _bên trong_ một Bounded Context duy nhất.

- **Entities (Thực thể):** Các đối tượng được xác định không phải bởi các thuộc tính của chúng, mà bởi định danh duy nhất và sự tồn tại liên tục theo thời gian (ví dụ: một `Customer` với một ID duy nhất). Chúng có thể thay đổi, nhưng các thay đổi trạng thái nên được mô hình hóa như các hoạt động nghiệp vụ rõ ràng (ví dụ:
    
    `customer.ChangeAddress()`, không phải `customer.setAddress()`.
    
- **Value Objects (Đối tượng Giá trị):** Các đối tượng đại diện cho một khía cạnh mô tả của miền và không có định danh khái niệm (ví dụ: `Money`, `Address`, `Color`). Được định nghĩa bởi các thuộc tính của chúng, là bất biến, và sự bằng nhau của chúng dựa trên giá trị, không phải định danh.
    
- **Aggregates (Tập hợp):** Một cụm các đối tượng liên quan (Entities và Value Objects) được coi là một đơn vị duy nhất cho các thay đổi dữ liệu. Mỗi Aggregate có một Entity gốc, được gọi là **Aggregate Root**. Aggregate Root là thành viên duy nhất của Aggregate mà các đối tượng bên ngoài được phép giữ tham chiếu đến. Nó chịu trách nhiệm thực thi các quy tắc nghiệp vụ (bất biến) cho toàn bộ cụm. Mẫu này xác định các ranh giới nhất quán giao dịch.
    
- **Domain Services (Dịch vụ Miền):** Khi một logic miền nào đó không tự nhiên thuộc về một Entity hoặc Value Object (ví dụ: một quy trình liên quan đến nhiều Aggregate), nó có thể được mô hình hóa trong một Domain Service không trạng thái.
    
- **Domain Events (Sự kiện Miền):** Một cơ chế để ghi lại các sự kiện quan trọng xảy ra trong miền (ví dụ: `OrderShipped`, `DeliveryCanceled`). Chúng rất quan trọng cho việc giao tiếp giữa các Aggregate và đặc biệt là giữa các Bounded Context khác nhau trong kiến trúc microservices.
    
- **Repositories (Kho chứa) và Factories (Nhà máy):** Repositories cung cấp ảo giác về một bộ sưu tập các Aggregate trong bộ nhớ, trừu tượng hóa cơ chế lưu trữ. Factories đóng gói logic để tạo ra các đối tượng hoặc Aggregate phức tạp.
    

| Tên Mẫu            | Mục đích                                                | Đặc điểm Chính                                                      | Ví dụ                                                     |
| ------------------ | ------------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------------- |
| **Entity**         | Đại diện cho một đối tượng có định danh và vòng đời.    | Có ID duy nhất, khả biến (mutable), sự bằng nhau dựa trên ID.       | `Customer`, `Product`, `Order`                            |
| **Value Object**   | Mô tả một thuộc tính của miền.                          | Không có ID, bất biến (immutable), sự bằng nhau dựa trên giá trị.   | `Address`, `Money`, `DateRange`                           |
| **Aggregate**      | Một cụm các đối tượng được coi là một đơn vị nhất quán. | Có một Aggregate Root, định nghĩa ranh giới giao dịch.              | Một `Order` cùng với các `OrderLineItem` của nó.          |
| **Domain Service** | Đóng gói logic miền không thuộc về một Entity duy nhất. | Không trạng thái, thường liên quan đến nhiều Aggregate.             | Dịch vụ tính toán phí vận chuyển dựa trên nhiều đơn hàng. |
| **Domain Event**   | Ghi lại một sự kiện nghiệp vụ đã xảy ra.                | Bất biến, mô tả một điều gì đó trong quá khứ.                       | `OrderPlaced`, `PaymentReceived`                          |
| **Repository**     | Trừu tượng hóa việc truy cập và lưu trữ các Aggregate.  | Cung cấp giao diện giống như bộ sưu tập, ẩn chi tiết cơ sở dữ liệu. | `CustomerRepository`, `OrderRepository`                   |
| **Factory**        | Đóng gói logic tạo đối tượng phức tạp.                  | Đảm bảo các đối tượng được tạo ra ở trạng thái hợp lệ.              | `OrderFactory` tạo một `Order` từ các thông tin đầu vào.  |

## Phần II: Clean và Hexagonal Architectures

Phần này sẽ bắc cầu từ "cái gì" (khái niệm DDD) đến "làm thế nào" (cấu trúc project).

### Nguyên tắc Đảo ngược Phụ thuộc

Vấn đề với kiến trúc phân lớp truyền thống là logic nghiệp vụ thường trở nên phụ thuộc vào cơ sở dữ liệu.

**Kiến trúc Lục giác (Ports and Adapters):** Mẫu này được giới thiệu như là giải pháp. Ý tưởng cốt lõi là cô lập logic nghiệp vụ của ứng dụng ("hình lục giác") khỏi thế giới bên ngoài (UI, cơ sở dữ liệu, API bên ngoài).

- **Ports:** Đây là các interface được định nghĩa _bên trong_ hình lục giác, quy định cách thức giao tiếp diễn ra. Chúng đại diện cho nhu cầu của ứng dụng (ví dụ: `Tôi cần lưu một người dùng`, `Tôi cần được điều khiển bởi một yêu cầu HTTP`).
    
- **Adapters:** Đây là các triển khai cụ thể của các port, sống _bên ngoài_ hình lục giác. Chúng dịch giữa port độc lập công nghệ và một công nghệ cụ thể (ví dụ: một adapter PostgreSQL triển khai port lưu người dùng, một adapter xử lý HTTP).
    

### Cấu trúc Lõi Ứng dụng

**Kiến trúc Sạch (Clean Architecture):** Được trình bày như một sự phát triển chi tiết hơn của Kiến trúc Lục giác, tổ chức lõi thành các lớp đồng tâm.

**Quy tắc Phụ thuộc:** Đây là quy tắc quan trọng nhất: các phụ thuộc mã nguồn chỉ có thể trỏ vào trong. Logic miền ở trung tâm không biết gì về các lớp bên ngoài.

**Giải thích các Lớp:**

- **Lớp Miền (Domain Layer - Entities):** Trung tâm tuyệt đối. Chứa các Entities, Value Objects, và Aggregates được định nghĩa bởi Thiết kế Chiến thuật. Nó không có phụ thuộc bên ngoài nào.
    
- **Lớp Ứng dụng (Application Layer - Use Cases):** Quay quanh lớp miền. Nó chứa các quy tắc nghiệp vụ cụ thể của ứng dụng và điều phối các đối tượng miền để thực hiện các trường hợp sử dụng (ví dụ: `CreateOrderService`). Phụ thuộc vào lớp miền nhưng không phụ thuộc vào các lớp bên ngoài.
    
- **Lớp Hạ tầng/Giao diện (Infrastructure/Interfaces Layer - Adapters):** Lớp ngoài cùng. Chứa mọi thứ tương tác với thế giới bên ngoài: cơ sở dữ liệu, web frameworks, hàng đợi tin nhắn. Lớp này phụ thuộc vào các lớp bên trong, triển khai các interface (ports) mà chúng định nghĩa.
    

Cấu trúc phân lớp của Clean Architecture về cơ bản là một chiến lược giảm thiểu rủi ro. Các lớp được tổ chức dựa trên tốc độ thay đổi và tầm quan trọng đối với nghiệp vụ. Phần ổn định và quan trọng nhất của ứng dụng là các quy tắc nghiệp vụ cốt lõi (miền). Những quy tắc này lý tưởng chỉ nên thay đổi khi chính nghiệp vụ thay đổi. Ngược lại, các phần dễ thay đổi và ít độc đáo nhất là các chi tiết triển khai: cơ sở dữ liệu cụ thể, web framework, API của bên thứ ba. Quy tắc Phụ thuộc đảm bảo rằng những thay đổi trong các thành phần dễ thay đổi (lớp ngoài) không thể phá vỡ các thành phần ổn định (lớp trong). Việc chuyển từ PostgreSQL sang MongoDB không nên đòi hỏi thay đổi một dòng mã nào trong lớp miền hoặc lớp ứng dụng. Do đó, kiến trúc được thiết kế để bảo vệ tài sản quý giá nhất (logic nghiệp vụ) khỏi các thành phần có rủi ro cao nhất (chi tiết triển khai). Nó hoạt động như một bức tường lửa kiến trúc, làm cho hệ thống trở nên kiên cường hơn trước sự thay đổi công nghệ và dễ bảo trì hơn trong dài hạn.

## Phần III: Triển khai Thực tế
### Giải phẫu một Project Go DDD

Phần này trình bày một cấu trúc project Go kinh điển, được tổng hợp từ nhiều ví dụ chất lượng cao. Cấu trúc này tuân thủ các quy ước của Go và các thực tiễn tốt nhất của cộng đồng (ví dụ: sử dụng thư mục `/internal`).

**Cấu trúc Thư mục Đề xuất:**

```
/cmd
  /app
    main.go          // Điểm khởi đầu ứng dụng, DI
/internal
  /application       // Các dịch vụ ứng dụng, use cases, DTOs
    /user
      service.go
  /domain            // Logic miền cốt lõi
    /user
      user.go        // Aggregate root User, entities, value objects
      repository.go  // Interface Repository (port)
  /infrastructure    // Triển khai cụ thể các interface của miền
    /repository
      user_memory.go // Triển khai repository trong bộ nhớ
      user_mysql.go  // Triển khai repository MySQL
  /interfaces        // Các adapter điều khiển ứng dụng
    /http
      handler.go     // Các HTTP handler (controllers)
      router.go
```

Bảng sau đây tạo ra một liên kết rõ ràng giữa các khái niệm trừu tượng của DDD/Clean Architecture và các thư mục cụ thể trong project Go.

| Mẫu DDD/Chiến thuật           | Khái niệm Clean/Hexagonal | Trách nhiệm của Lớp                                           | Thư mục Go                                          |
| ----------------------------- | ------------------------- | ------------------------------------------------------------- | --------------------------------------------------- |
| **Aggregate Root**            | Entity                    | Mô hình hóa các quy tắc nghiệp vụ cốt lõi, bất biến.          | `/internal/domain/user/user.go`                     |
| **Repository Interface**      | Port (Driven)             | Định nghĩa hợp đồng cho việc lưu trữ, độc lập công nghệ.      | `/internal/domain/user/repository.go`               |
| **Application Service**       | Use Case / Interactor     | Điều phối các đối tượng miền để thực hiện một tác vụ.         | `/internal/application/user/service.go`             |
| **Repository Implementation** | Adapter (Driven)          | Triển khai cụ thể việc lưu trữ (ví dụ: PostgreSQL, MongoDB).  | `/internal/infrastructure/repository/user_mysql.go` |
| **HTTP Handler**              | Adapter (Driving)         | Dịch các yêu cầu HTTP thành các lệnh gọi Application Service. | `/internal/interfaces/http/handler.go`              |

### Code trong Thực tế: Triển khai Mẫu Repository

Phần này cung cấp một phân tích chi tiết về một triển khai hoàn chỉnh, sử dụng ví dụ xuất sắc từ blog của Three Dots Labs. Mẫu này được chọn vì nó minh họa hoàn hảo nguyên tắc đảo ngược phụ thuộc ở trung tâm của kiến trúc.

#### Định nghĩa Port (Lớp Miền)

Đây là mã nguồn cho interface `Repository`. Interface này nằm trong package `domain` vì nó định nghĩa một hợp đồng mà lõi nghiệp vụ yêu cầu, nhưng nó không quan tâm đến cách hợp đồng đó được thực hiện. Nó hoàn toàn độc lập với công nghệ.

Go

```go
// trong /internal/domain/hour/repository.go
package hour

import (
    "context"
    "time"
)

type Repository interface {
    GetOrCreateHour(ctx context.Context, hourTime time.Time) (*Hour, error)
    UpdateHour(
        ctx context.Context,
        hourTime time.Time,
        updateFn func(h *Hour) (*Hour, error),
    ) error
}
```

#### Triển khai các Adapter (Lớp Hạ tầng)

##### Adapter Trong bộ nhớ (In-Memory)

Triển khai này sử dụng một map của Go để mô phỏng một cơ sở dữ liệu. Nó rất quan trọng để cho phép các bài kiểm thử đơn vị (unit test) nhanh chóng và đáng tin cậy cho các dịch vụ ứng dụng mà không cần đến một cơ sở dữ liệu thực sự.

Go

```go
// trong /internal/infrastructure/repository/hour_memory.go
package repository

import (
    //... imports
)

type MemoryHourRepository struct {
    hours maphour.Hour
    lock  *sync.RWMutex
    hourFactory hour.Factory
}

func NewMemoryHourRepository(hourFactory hour.Factory) *MemoryHourRepository {
    //...
    return &MemoryHourRepository{
        hours:       maphour.Hour{},
        lock:        &sync.RWMutex{},
        hourFactory: hourFactory,
    }
}

func (m *MemoryHourRepository) UpdateHour(
    _ context.Context,
    hourTime time.Time,
    updateFn func(h *hour.Hour) (*hour.Hour, error),
) error {
    m.lock.Lock()
    defer m.lock.Unlock()

    currentHour, err := m.getOrCreateHour(hourTime)
    if err!= nil {
        return err
    }

    updatedHour, err := updateFn(currentHour)
    if err!= nil {
        return err
    }

    m.hours = *updatedHour
    return nil
}
//... các phương thức khác
```

##### Adapter MySQL

Đây là một triển khai sẵn sàng cho môi trường production, bao gồm cả việc quản lý giao dịch để đảm bảo tính nhất quán của dữ liệu.

Go

```go
// trong /internal/infrastructure/repository/hour_mysql.go
package repository

import (
    //... imports
)

type MySQLHourRepository struct {
    db *sqlx.DB
    hourFactory hour.Factory
}

//... NewMySQLHourRepository

func (m MySQLHourRepository) UpdateHour(
    ctx context.Context,
    hourTime time.Time,
    updateFn func(h *hour.Hour) (*hour.Hour, error),
) (err error) {
    tx, err := m.db.Beginx()
    if err!= nil {
        return errors.Wrap(err, "unable to start transaction")
    }
    defer func() {
        err = m.finishTransaction(err, tx)
    }()

    existingHour, err := m.getOrCreateHour(ctx, tx, hourTime, true) // forUpdate = true
    if err!= nil {
        return err
    }

    updatedHour, err := updateFn(existingHour)
    if err!= nil {
        return err
    }

    if err := m.upsertHour(tx, updatedHour); err!= nil {
        return err
    }

    return nil
}

func (m MySQLHourRepository) getOrCreateHour(
    ctx context.Context,
    db sqlContextGetter,
    hourTime time.Time,
    forUpdate bool,
) (*hour.Hour, error) {
    //...
    query := "SELECT * FROM `hours` WHERE `hour` =?"
    if forUpdate {
        query += " FOR UPDATE"
    }
    //...
}
//... các phương thức khác
```

#### Kết nối các Lớp: Ví dụ về một Use Case

Một `Application Service` sẽ sử dụng interface `hour.Repository` thông qua dependency injection. Nó không biết và không quan tâm đến việc triển khai cụ thể là in-memory hay MySQL.

Go

```go
// trong /internal/application/booking/service.go
package booking

type Service struct {
    hourRepo hour.Repository
}

func (s Service) ScheduleTraining(ctx context.Context, hourTime time.Time) error {
    err := s.hourRepo.UpdateHour(ctx, hourTime, func(h *hour.Hour) (*hour.Hour, error) {
        if err := h.ScheduleTraining(); err!= nil {
            return nil, err
        }
        return h, nil
    })
    return err
}
```

Cuối cùng, tệp `main.go` là nơi ứng dụng được khởi tạo. Đây là nơi "kết nối" xảy ra: một `MySQLHourRepository` cụ thể được khởi tạo và được tiêm vào `Application Service`, thỏa mãn interface `hour.Repository`. Điều này minh họa cơ chế dependency injection làm cho toàn bộ kiến trúc hoạt động.

Go

```go
// trong /cmd/app/main.go
package main

func main() {
    //... thiết lập kết nối cơ sở dữ liệu (db)

    hourFactory := hour.NewFactory()
    // Tiêm triển khai MySQL cụ thể
    hourRepo := repository.NewMySQLHourRepository(db, hourFactory)

    bookingService := booking.NewService(hourRepo)

    //... khởi tạo và chạy máy chủ HTTP với bookingService
}
```

## Phần IV: Phân tích và Khuyến nghị - Sự Đánh đổi của DDD trong Go
### Đánh giá Lợi ích ("Pros")

- **Khả năng Kiểm thử (Testability):** Logic nghiệp vụ cốt lõi có thể được kiểm thử hoàn toàn độc lập với UI, cơ sở dữ liệu hoặc bất kỳ dịch vụ bên ngoài nào, dẫn đến các bài kiểm thử nhanh hơn và đáng tin cậy hơn.
    
- **Khả năng Bảo trì & Linh hoạt:** Sự tách biệt rõ ràng các mối quan tâm và quy tắc phụ thuộc có nghĩa là những thay đổi ở một phần của hệ thống (ví dụ: thay đổi cơ sở dữ liệu) có tác động tối thiểu đến các phần khác. Điều này làm cho codebase dễ hiểu và phát triển hơn theo thời gian.
    
- **Phát triển Song song:** Một khi các interface (ports) được định nghĩa, các nhóm khác nhau có thể làm việc trên các adapter khác nhau (ví dụ: nhóm UI, nhóm cơ sở dữ liệu) song song mà không có xung đột.
    
- **Phù hợp với Nghiệp vụ:** Kiến trúc buộc mã nguồn phải phản ánh miền nghiệp vụ, tạo ra một tài sản có giá trị và dễ hiểu hơn.
    

### Xem xét Nhược điểm ("Cons")

- **Phức tạp & Đường cong Học tập:** Đây không phải là kiến trúc dành cho người mới bắt đầu. Nó đòi hỏi sự hiểu biết vững chắc về các nguyên tắc thiết kế phần mềm như SOLID và chính DDD. Có một sự đầu tư đáng kể ban đầu về thời gian học tập.
    
- **Mã lặp (Boilerplate) & Sự Gián tiếp:** Nhu cầu về các interface, DTO, và việc ánh xạ giữa các lớp có thể làm tăng lượng mã và khiến việc theo dõi một yêu cầu có cảm giác như "nhảy qua các lớp thừa thãi".
    
- **Nguy cơ Thiết kế Quá mức (Over-Engineering):** Đối với các ứng dụng CRUD đơn giản hoặc các project có logic nghiệp vụ tối thiểu, kiến trúc này là quá mức cần thiết. Chi phí triển khai vượt xa lợi ích. Điều này trực tiếp giải quyết những lo ngại của cộng đồng Go về việc các mẫu "doanh nghiệp" bị áp đặt lên một ngôn ngữ coi trọng sự đơn giản.
    
- **Chi phí Hiệu năng Tiềm tàng:** Sự gián tiếp từ các interface và việc ánh xạ dữ liệu có thể gây ra một hình phạt hiệu năng nhỏ, điều này có thể là một mối quan tâm trong các ứng dụng yêu cầu hiệu năng cực kỳ cao.
    
## Kết luận

DDD, được hỗ trợ bởi kiến trúc Clean/Hexagonal, là một chiến lược mạnh mẽ để xây dựng các ứng dụng Go phức tạp, dễ bảo trì và bền vững. Đây là một sự đầu tư chiến lược. Chi phí ban đầu về sự phức tạp và học tập được đền đáp trong suốt vòng đời của dự án thông qua việc tăng khả năng bảo trì, khả năng kiểm thử và khả năng thích ứng với các nhu cầu nghiệp vụ thay đổi.

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*