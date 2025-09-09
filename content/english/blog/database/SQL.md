---
title: SQL
date: 2025-08-12
draft: false
tags:
  - database
  - sql
---
Các kiến trức trọng tâm và tất cả các lệnh SQL
<!--more-->
# Cẩm Nang SQL Toàn Tập: Từ Zero Đến Hero - Tổng Hợp Tất Cả Các Lệnh SQL Quan Trọng

Trong thế giới số hiện đại, dữ liệu được ví như "dầu mỏ" mới, và SQL chính là công cụ thiết yếu để khai thác và tinh chế nguồn tài nguyên quý giá đó. Tuy nhiên, đối với người mới bắt đầu, việc học SQL có thể trở nên khó khăn khi phải đối mặt với vô số tài liệu rời rạc và thiếu cấu trúc. Bài viết này được biên soạn như một cuốn cẩm nang toàn diện, cung cấp một lộ trình học tập có hệ thống, từ những viên gạch nền móng đầu tiên như định nghĩa dữ liệu, cho đến các kỹ thuật truy vấn và tối ưu hóa phức tạp. Mục tiêu là trang bị cho người đọc một kiến thức vững chắc và một cái nhìn tổng quan, mạch lạc về Ngôn ngữ Truy vấn có Cấu trúc.

## Phần 1: Giới Thiệu - SQL Là Gì và Tại Sao Bạn Cần Phải Học Nó?

Để bắt đầu hành trình làm chủ dữ liệu, điều đầu tiên cần hiểu rõ là công cụ cốt lõi mà chúng ta sẽ sử dụng.

### SQL là gì?

SQL, viết tắt của **Structured Query Language** (Ngôn ngữ Truy vấn có Cấu trúc), là ngôn ngữ tiêu chuẩn được sử dụng để giao tiếp, quản lý và thao tác với các cơ sở dữ liệu quan hệ. Cần phải nhấn mạnh rằng SQL không phải là một ngôn ngữ lập trình đa năng như Python hay Java, mà là một ngôn ngữ chuyên dụng, được thiết kế riêng cho mục đích làm việc với dữ liệu. Một trong những ưu điểm lớn nhất của SQL là nó không đòi hỏi kỹ năng mã hóa phức tạp; thay vào đó, nó sử dụng các từ khóa tiếng Anh gần gũi và dễ hiểu như

`SELECT`, `INSERT`, `UPDATE`, giúp người dùng dễ dàng tiếp cận và sử dụng.

### Lịch sử hình thành

SQL ra đời vào những năm 1970, được phát triển bởi hai kỹ sư của IBM là Donald D. Chamberlin và Raymond F. Boyce. Ngôn ngữ này được xây dựng dựa trên nền tảng lý thuyết của mô hình cơ sở dữ liệu quan hệ do Tiến sĩ Edgar F. Codd, cũng là một nhà khoa học của IBM, đề xuất vào năm 1970. Ban đầu, nó có tên là SEQUEL (Structured English Query Language), nhưng sau đó được rút gọn thành SQL do một tranh chấp về thương hiệu. Kể từ đó, SQL đã trở thành một tiêu chuẩn công nghiệp được công nhận toàn cầu.

### Vai trò và ứng dụng thực tế

Ngày nay, SQL là một kỹ năng không thể thiếu đối với nhiều vị trí trong ngành công nghệ, từ nhà phân tích dữ liệu, nhà khoa học dữ liệu, lập trình viên backend cho đến quản trị viên cơ sở dữ liệu. Sự phổ biến của nó đến từ khả năng ứng dụng trong vô số lĩnh vực:

- **Phân tích kinh doanh (Business Intelligence):** Các chuyên gia sử dụng SQL để trích xuất, tổng hợp và phân tích dữ liệu từ các hệ thống lớn, nhằm tìm ra các xu hướng (insights) kinh doanh, tạo báo cáo và hỗ trợ việc ra quyết định.
    
- **Phát triển ứng dụng:** Hầu hết các ứng dụng web và di động đều cần một nơi để lưu trữ dữ liệu người dùng, thông tin sản phẩm, đơn hàng, v.v. SQL đóng vai trò là cầu nối ở tầng backend, giúp ứng dụng quản lý và thao tác với các dữ liệu này.
    
- **Ngành Game:** Các trò chơi điện tử sử dụng cơ sở dữ liệu để lưu trữ và quản lý một lượng lớn thông tin như hồ sơ người chơi, điểm số, vật phẩm và thành tích.
    
- **Hệ thống giáo dục:** Các trường học và tổ chức giáo dục dùng SQL để quản lý hồ sơ sinh viên, thông tin khóa học, điểm số và các hoạt động hành chính khác.
    

### Các Hệ Quản trị Cơ sở dữ liệu Quan hệ (RDBMS) phổ biến

Một điểm quan trọng cần làm rõ là sự khác biệt giữa SQL và các Hệ Quản trị Cơ sở dữ liệu Quan hệ (Relational Database Management System - RDBMS). SQL là ngôn ngữ, trong khi RDBMS là phần mềm, là hệ thống thực thi các câu lệnh SQL đó. Có thể hình dung SQL như "tiếng Anh", còn RDBMS như một "nhà xuất bản" sử dụng tiếng Anh để tạo ra sách. Việc nhầm lẫn giữa SQL và MySQL là rất phổ biến; MySQL chỉ là một trong nhiều RDBMS sử dụng ngôn ngữ SQL.

Một số RDBMS phổ biến hiện nay bao gồm:

- **MySQL:** Một hệ quản trị CSDL quan hệ mã nguồn mở rất phổ biến, đặc biệt trong các ứng dụng web.
    
- **PostgreSQL:** Một hệ quản trị CSDL quan hệ mã nguồn mở mạnh mẽ, nổi tiếng với sự tuân thủ chuẩn SQL và các tính năng nâng cao.
    
- **Microsoft SQL Server:** Một sản phẩm thương mại của Microsoft, được sử dụng rộng rãi trong các môi trường doanh nghiệp, đặc biệt là các tổ chức sử dụng hệ sinh thái Windows.
    
- **Oracle Database:** Một hệ quản trị CSDL thương mại hàng đầu, thường được các tập đoàn lớn sử dụng cho các ứng dụng quan trọng và yêu cầu hiệu suất cao.
    

## Phần 2: Nền Tảng Của SQL - Hiểu Về Cơ Sở Dữ Liệu Quan Hệ

Trước khi viết những câu lệnh SQL đầu tiên, việc nắm vững các khái niệm nền tảng của cơ sở dữ liệu quan hệ là điều kiện tiên quyết. Đây chính là cấu trúc mà SQL được thiết kế để tương tác.

### Các khái niệm cốt lõi

- **Cơ sở dữ liệu (Database):** Là một tập hợp các thông tin có liên quan đến nhau, được tổ chức và lưu trữ một cách có hệ thống trên máy tính để có thể dễ dàng truy cập và quản lý.
    
- **Cơ sở dữ liệu quan hệ (Relational Database):** Là một loại cơ sở dữ liệu mà trong đó dữ liệu được tổ chức thành các bảng (tables) có cấu trúc chặt chẽ. Mô hình này được E.F. Codd đề xuất vào năm 1970 và đã trở thành mô hình thống trị trong quản lý dữ liệu suốt nhiều thập kỷ.
    
- **Bảng (Table):** Là thành phần cấu trúc cơ bản nhất trong CSDL quan hệ, bao gồm các hàng và cột. Mỗi bảng đại diện cho một loại thực thể, ví dụ như bảng `SinhVien`, bảng `SanPham`.
    
- **Hàng (Row) và Cột (Column):**
    
    - **Cột (Column/Field/Attribute):** Đại diện cho một thuộc tính hoặc một mẩu thông tin mô tả thực thể. Ví dụ, trong bảng `SinhVien`, các cột có thể là `MaSinhVien`, `HoTen`, `NgaySinh`.
        
    - **Hàng (Row/Record/Tuple):** Đại diện cho một bản ghi dữ liệu cụ thể, một thực thể đơn lẻ trong bảng. Ví dụ, một hàng trong bảng `SinhVien` chứa thông tin đầy đủ của một sinh viên cụ thể.
        

### Chìa khóa của sự toàn vẹn

Để đảm bảo dữ liệu luôn chính xác và nhất quán, CSDL quan hệ sử dụng các loại "khóa".

- **Khóa chính (Primary Key):** Là một hoặc nhiều cột được sử dụng để xác định _duy nhất_ mỗi hàng trong một bảng. Giá trị trong cột khóa chính không được phép trống (`NULL`) và phải là duy nhất trong toàn bộ bảng. Đây là "chứng minh nhân dân" của mỗi hàng.
    
- **Khóa ngoại (Foreign Key):** Là một cột (hoặc một nhóm cột) trong một bảng dùng để thiết lập một liên kết đến khóa chính của một bảng khác. Khóa ngoại là cơ chế để thực thi _toàn vẹn tham chiếu_ (referential integrity), đảm bảo rằng mối quan hệ giữa các bảng luôn hợp lệ. Ví dụ, trong bảng `DonHang`, cột `MaKhachHang` sẽ là khóa ngoại tham chiếu đến cột `MaKhachHang` (khóa chính) trong bảng `KhachHang`.
    

### Các kiểu dữ liệu (Data Types)

Mỗi cột trong một bảng phải được gán một kiểu dữ liệu cụ thể. Kiểu dữ liệu định nghĩa loại giá trị mà cột đó có thể chứa, ví dụ như số nguyên, văn bản, ngày tháng, v.v.. Việc chọn đúng kiểu dữ liệu không chỉ đảm bảo tính toàn vẹn mà còn giúp tối ưu hóa không gian lưu trữ và hiệu suất truy vấn.

Mặc dù SQL có một bộ chuẩn, các RDBMS khác nhau có thể có những tên gọi và đặc điểm riêng cho các kiểu dữ liệu. Việc hiểu rõ sự khác biệt này là rất quan trọng khi làm việc trên nhiều hệ thống.

**Bảng so sánh các kiểu dữ liệu phổ biến**

| Loại Dữ Liệu    | SQL Server                                   | MySQL                                   | Oracle                                         | Mô tả chung                                                                                          |
| --------------- | -------------------------------------------- | --------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Chuỗi Ký Tự** | `VARCHAR(n)`, `NVARCHAR(n)`, `VARCHAR(MAX)`  | `VARCHAR(n)`, `TEXT`                    | `VARCHAR2(n)`, `CLOB`                          | Lưu trữ văn bản. Kiểu có tiền tố `N` (ví dụ: `NVARCHAR`) dùng để lưu trữ ký tự Unicode (đa ngôn ngữ) |
| **Số Nguyên**   | `TINYINT`, `SMALLINT`, `INT`, `BIGINT`       | `TINYINT`, `SMALLINT`, `INT`, `BIGINT`  | `NUMBER(p)`                                    | Lưu trữ các số không có phần thập phân, với các phạm vi khác nhau                                    |
| **Số Thực**     | `FLOAT`, `REAL`, `DECIMAL(p,s)`              | `FLOAT`, `DOUBLE`, `DECIMAL(p,s)`       | `NUMBER(p,s)`, `FLOAT`                         | Lưu trữ các số có phần thập phân. `DECIMAL` dùng cho các giá trị cần độ chính xác cao như tiền tệ    |
| **Ngày & Giờ**  | `DATE`, `TIME`, `DATETIME2`, `SMALLDATETIME` | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | `DATE`, `TIMESTAMP`                            | Lưu trữ thông tin về ngày, giờ hoặc cả hai                                                           |
| **Logic/Bit**   | `BIT`                                        | `BOOLEAN` (thực chất là `TINYINT(1)`)   | (Không có kiểu riêng, thường dùng `NUMBER(1)`) | Lưu trữ giá trị logic True/False (thường là 1/0)                                                     |

### Các ràng buộc (Constraints)

Ràng buộc là các quy tắc được áp dụng trên các cột của bảng để đảm bảo tính chính xác và toàn vẹn của dữ liệu. Ngoài khóa chính và khóa ngoại, các ràng buộc phổ biến khác bao gồm:

- `NOT NULL`: Đảm bảo một cột không thể có giá trị `NULL` (trống).
    
- `UNIQUE`: Đảm bảo tất cả các giá trị trong một cột phải là duy nhất.
    
- `CHECK`: Đảm bảo rằng tất cả các giá trị trong một cột thỏa mãn một điều kiện cụ thể (ví dụ: `Tuoi > 18`).
    
- `DEFAULT`: Cung cấp một giá trị mặc định cho một cột khi không có giá trị nào được chỉ định lúc chèn dữ liệu.
    

## Phần 3: Phân Loại Lệnh SQL - Sơ Đồ Tư Duy Để Làm Chủ SQL

Để hệ thống hóa kiến thức và hiểu rõ mục đích của từng câu lệnh, SQL được chia thành các nhóm lệnh con. Cách phân loại phổ biến và hiện đại nhất chia SQL thành 5 họ lệnh chính. Việc hiểu rõ sự phân chia này giống như có một bản đồ tư duy, giúp người học biết chính xác nên dùng công cụ nào cho công việc nào.

- **DDL (Data Definition Language - Ngôn ngữ Định nghĩa Dữ liệu):** Các lệnh này được sử dụng để định nghĩa, tạo, thay đổi và xóa cấu trúc của các đối tượng trong cơ sở dữ liệu như bảng, chỉ mục, hay view.
    
- **DML (Data Manipulation Language - Ngôn ngữ Thao tác Dữ liệu):** Các lệnh này dùng để quản lý dữ liệu bên trong các bảng, bao gồm việc thêm, cập nhật và xóa dữ liệu.
    
- **DQL (Data Query Language - Ngôn ngữ Truy vấn Dữ liệu):** Họ lệnh này chỉ có một thành viên duy nhất và quan trọng nhất là `SELECT`. Nó được dùng để truy xuất và đọc dữ liệu từ cơ sở dữ liệu.
    
- **DCL (Data Control Language - Ngôn ngữ Điều khiển Dữ liệu):** Các lệnh này liên quan đến việc quản lý quyền truy cập và bảo mật, cho phép hoặc thu hồi quyền của người dùng trên các đối tượng cơ sở dữ liệu.
    
- **TCL (Transaction Control Language - Ngôn ngữ Điều khiển Giao dịch):** Các lệnh này quản lý các giao dịch (transactions) để đảm bảo tính toàn vẹn và nhất quán của dữ liệu khi thực hiện một chuỗi các thao tác.
    

Một số tài liệu cũ hoặc một số hệ thống có thể gộp lệnh `SELECT` vào nhóm DML, vì nó cũng là một dạng "thao tác" với dữ liệu (thao tác đọc). Tuy nhiên, cách phân loại hiện đại tách

`SELECT` thành một họ riêng là DQL mang lại sự rõ ràng và logic hơn. Việc tách biệt này nhấn mạnh sự khác biệt cơ bản giữa các hành động **thay đổi trạng thái** của dữ liệu (ghi - write) của DML và hành động **chỉ đọc trạng thái** (đọc - read) của DQL. Đối với người học, việc phân biệt rạch ròi giữa "đọc" và "ghi" là cực kỳ quan trọng để hiểu sâu hơn về các vấn đề như hiệu suất, khóa (locking) và bảo mật trong cơ sở dữ liệu.

**Bảng tổng quan các lệnh SQL**

Bảng dưới đây cung cấp một cái nhìn tổng thể về các họ lệnh và các lệnh chính thuộc mỗi họ, đóng vai trò như một bản đồ để định hướng trong suốt quá trình học.

|Họ Lệnh|Tên Đầy Đủ|Mục Đích|Các Lệnh Chính|
|---|---|---|---|
|**DDL**|Data Definition Language|Định nghĩa, thay đổi cấu trúc CSDL|`CREATE`, `ALTER`, `DROP`, `TRUNCATE`|
|**DML**|Data Manipulation Language|Thêm, sửa, xóa dữ liệu|`INSERT`, `UPDATE`, `DELETE`|
|**DQL**|Data Query Language|Truy vấn, đọc dữ liệu|`SELECT`|
|**DCL**|Data Control Language|Quản lý quyền truy cập|`GRANT`, `REVOKE`|
|**TCL**|Transaction Control Language|Quản lý các giao dịch|`COMMIT`, `ROLLBACK`, `SAVEPOINT`|

## Phần 4: DDL - Xây Dựng và Quản Lý "Ngôi Nhà" Dữ Liệu

Các lệnh DDL là những công cụ đầu tiên bạn cần đến khi bắt đầu một dự án, dùng để xây dựng nên "khung xương" cho cơ sở dữ liệu của mình.

- `CREATE DATABASE`, `CREATE TABLE`: Được dùng để tạo mới một cơ sở dữ liệu hoặc một bảng. Khi tạo bảng, chúng ta cần định nghĩa các cột, kiểu dữ liệu cho từng cột và các ràng buộc cần thiết như khóa chính (`PRIMARY KEY`) hay `NOT NULL`.
    
    - Ví dụ tạo bảng:
        
        SQL
        
        ```
        CREATE TABLE SinhVien (
            MaSV INT PRIMARY KEY,
            HoTen NVARCHAR(100) NOT NULL,
            NgaySinh DATE
        );
        ```
        
- `ALTER TABLE`: Lệnh này cho phép sửa đổi cấu trúc của một bảng đã tồn tại. Các thao tác phổ biến bao gồm thêm cột (`ADD COLUMN`), xóa cột (`DROP COLUMN`), hoặc thay đổi kiểu dữ liệu của một cột (`MODIFY COLUMN` hoặc `ALTER COLUMN`).
    
    - Ví dụ thêm cột:
        
        SQL
        
        ```
        ALTER TABLE SinhVien ADD Email VARCHAR(255);
        ```
        
- `DROP DATABASE`, `DROP TABLE`: Xóa vĩnh viễn một cơ sở dữ liệu hoặc một bảng, bao gồm cả cấu trúc, dữ liệu, chỉ mục và các ràng buộc liên quan. Đây là một hành động cực kỳ nguy hiểm và không thể hoàn tác nếu không có bản sao lưu (backup).
    
- `TRUNCATE TABLE`: Xóa toàn bộ dữ liệu bên trong một bảng một cách nhanh chóng nhưng vẫn giữ lại cấu trúc của bảng (tên cột, kiểu dữ liệu, chỉ mục, v.v.). Lệnh này hữu ích khi cần dọn sạch dữ liệu trong một bảng tạm để nạp dữ liệu mới.
    

### So sánh chuyên sâu: DELETE, TRUNCATE, và DROP

Người mới bắt đầu thường nhầm lẫn giữa ba lệnh này vì chúng đều liên quan đến việc "xóa". Tuy nhiên, chúng hoạt động theo những cách rất khác nhau và có những hệ quả riêng biệt.

1. **Phân loại lệnh:** `DELETE` là một lệnh DML (Thao tác dữ liệu), trong khi `TRUNCATE` và `DROP` là các lệnh DDL (Định nghĩa dữ liệu). Sự khác biệt này không chỉ mang tính học thuật mà còn dẫn đến những khác biệt về cơ chế hoạt động.
    
2. **Cơ chế hoạt động và Hiệu suất:**
    
    - `DELETE`: Xóa các hàng một cách có chọn lọc (nếu có mệnh đề `WHERE`) hoặc toàn bộ. Nó xóa từng hàng một và ghi lại mỗi hành động xóa vào nhật ký giao dịch (transaction log). Điều này làm cho `DELETE` chậm hơn nhưng cho phép hoàn tác (`ROLLBACK`) và có thể kích hoạt các `TRIGGER` (hành động tự động) trên bảng.
        
    - `TRUNCATE`: Xóa tất cả các hàng trong bảng bằng cách giải phóng các trang dữ liệu (data pages) chứa dữ liệu của bảng. Nó không ghi log cho từng hàng nên thực thi nhanh hơn rất nhiều so với `DELETE` trên các bảng lớn. `TRUNCATE` không kích hoạt `TRIGGER` và thường không thể `ROLLBACK` một cách dễ dàng.
        
    - `DROP`: Xóa toàn bộ đối tượng bảng, bao gồm cả cấu trúc và dữ liệu. Bảng đó sẽ không còn tồn tại trong cơ sở dữ liệu.
        
3. **Trường hợp sử dụng:**
    
    - **Dùng `DELETE`** khi cần xóa dữ liệu có điều kiện (`WHERE`), muốn kích hoạt `TRIGGER`, hoặc cần khả năng hoàn tác. Ví dụ: Xóa một khách hàng cụ thể đã không hoạt động trong 2 năm.
        
    - **Dùng `TRUNCATE`** khi cần xóa sạch dữ liệu của một bảng lớn một cách nhanh chóng và reset lại các giá trị tự tăng (identity), không quan tâm đến `TRIGGER`. Ví dụ: Dọn dẹp một bảng tạm (staging table) trước mỗi lần nhập dữ liệu hàng loạt.
        
    - **Dùng `DROP`** khi muốn loại bỏ hoàn toàn một bảng không còn được sử dụng khỏi cơ sở dữ liệu.
        

Việc lựa chọn đúng lệnh phụ thuộc vào mục đích cụ thể, yêu cầu về hiệu suất và khả năng phục hồi dữ liệu.

## Phần 5: DML - "Thêm, Sửa, Xóa" Dữ Liệu

Sau khi đã có "ngôi nhà" (cấu trúc bảng), các lệnh DML giúp chúng ta đưa "đồ đạc" (dữ liệu) vào, sắp xếp lại hoặc loại bỏ chúng.

- `INSERT INTO`: Dùng để chèn một hoặc nhiều hàng dữ liệu mới vào một bảng.
    
    - Cú pháp cơ bản:
        
        SQL
        
        ```
        INSERT INTO SinhVien (MaSV, HoTen, NgaySinh) VALUES (1, 'Nguyễn Văn A', '2002-01-15');
        ```
        
    - Chèn dữ liệu từ bảng khác: Một kỹ thuật nâng cao và rất hữu ích là sử dụng `INSERT INTO... SELECT...` để sao chép và chèn dữ liệu từ một bảng khác vào bảng hiện tại.
        
        SQL
        
        ```
        INSERT INTO SinhVienLuuTru (MaSV, HoTen)
        SELECT MaSV, HoTen FROM SinhVien WHERE NgaySinh < '2000-01-01';
        ```
        
- `UPDATE`: Dùng để cập nhật, sửa đổi các bản ghi hiện có trong bảng.
    
    SQL
    
    ```
    UPDATE SinhVien SET Email = 'a.nguyen@example.com' WHERE MaSV = 1;
    ```
    
- `DELETE`: Dùng để xóa một hoặc nhiều bản ghi khỏi bảng.
    
    SQL
    
    ```
    DELETE FROM SinhVien WHERE MaSV = 1;
    ```
    

### Tầm quan trọng sống còn của mệnh đề WHERE

Một trong những sai lầm nguy hiểm và dễ mắc phải nhất đối với người mới làm việc với SQL là thực thi lệnh `UPDATE` hoặc `DELETE` mà quên mất mệnh đề `WHERE`. Nếu không có

`WHERE` để chỉ định điều kiện, lệnh sẽ được áp dụng cho **toàn bộ các hàng** trong bảng, dẫn đến việc cập nhật hoặc xóa sạch dữ liệu một cách không mong muốn. Trong môi trường sản xuất, đây là một thảm họa có thể gây mất mát dữ liệu nghiêm trọng.

Vì vậy, một quy tắc vàng cần phải tuân thủ nghiêm ngặt là: **Luôn luôn viết và kiểm tra câu lệnh `SELECT` với cùng mệnh đề `WHERE` trước khi thực thi `UPDATE` hoặc `DELETE`**.

1. Viết câu lệnh `SELECT * FROM ten_bang WHERE dieu_kien;`.
    
2. Chạy câu lệnh `SELECT` và kiểm tra kết quả để đảm bảo rằng nó chỉ trả về đúng những hàng mà bạn muốn thay đổi.
    
3. Sau khi đã chắc chắn, thay thế `SELECT *` bằng `UPDATE ten_bang SET...` hoặc `DELETE`.
    

Thực hành thói quen này sẽ giúp tránh được những sai lầm tốn kém và đảm bảo an toàn cho dữ liệu.

## Phần 6: DQL - Trái Tim Của SQL, Nghệ Thuật Truy Vấn Dữ Liệu

Nếu DDL xây dựng cấu trúc và DML quản lý dữ liệu, thì DQL (với lệnh `SELECT`) chính là công cụ để khai thác giá trị từ dữ liệu đó. Đây là phần được sử dụng thường xuyên nhất trong công việc hàng ngày của một nhà phân tích.

### Truy vấn cơ bản

- `SELECT`: Chọn các cột mà bạn muốn hiển thị trong kết quả. Có thể sử dụng `*` để chọn tất cả các cột.
    
- `FROM`: Chỉ định bảng nguồn mà bạn muốn lấy dữ liệu từ đó.
    
- `DISTINCT`: Loại bỏ các hàng có giá trị trùng lặp hoàn toàn trong kết quả trả về.
    

SQL

```
SELECT DISTINCT ThanhPho FROM KhachHang; -- Lấy danh sách các thành phố duy nhất của khách hàng
```

### Lọc dữ liệu với WHERE

Mệnh đề `WHERE` được dùng để lọc các hàng, chỉ giữ lại những hàng thỏa mãn một điều kiện nhất định.

- **Toán tử so sánh:** `=`, `!=` (hoặc `<>`), `>`, `<`, `>=`, `<=`
    
- **Toán tử logic:** `AND`, `OR`, `NOT` để kết hợp nhiều điều kiện.
    
- **Toán tử nâng cao:**
    
    - `IN`: Kiểm tra xem giá trị của một cột có nằm trong một danh sách các giá trị cho trước hay không.
        
    - `BETWEEN`: Lọc các giá trị nằm trong một khoảng (bao gồm cả hai đầu mút).
        
    - `LIKE`: Tìm kiếm dữ liệu văn bản theo một mẫu. Nó thường được kết hợp với các ký tự đại diện: `%` (đại diện cho không, một hoặc nhiều ký tự) và `_` (đại diện cho chính xác một ký tự).
        

SQL

```
SELECT * FROM SanPham
WHERE Gia BETWEEN 100000 AND 500000
AND TenSanPham LIKE 'Áo sơ mi%';
```

### Sắp xếp và Giới hạn

- `ORDER BY`: Sắp xếp tập kết quả theo một hoặc nhiều cột. `ASC` (Ascending) là sắp xếp tăng dần (mặc định), và `DESC` (Descending) là giảm dần.
    
- `LIMIT` / `TOP`: Giới hạn số lượng hàng được trả về. Cú pháp có sự khác biệt giữa các RDBMS: MySQL và PostgreSQL sử dụng `LIMIT`, trong khi SQL Server sử dụng `TOP`.
    

SQL

```
-- Lấy 5 sản phẩm đắt nhất (MySQL/PostgreSQL)
SELECT TenSanPham, Gia
FROM SanPham
ORDER BY Gia DESC
LIMIT 5;

-- Lấy 5 sản phẩm đắt nhất (SQL Server)
SELECT TOP 5 TenSanPham, Gia
FROM SanPham
ORDER BY Gia DESC;
```

### Các hàm tổng hợp (Aggregate Functions)

Các hàm này thực hiện một phép tính trên một tập hợp các hàng và trả về một giá trị duy nhất, tóm tắt cho tập hợp đó.

- `COUNT()`: Đếm số lượng hàng.
    
- `SUM()`: Tính tổng các giá trị (chỉ áp dụng cho cột số).
    
- `AVG()`: Tính giá trị trung bình (chỉ áp dụng cho cột số).
    
- `MAX()`: Tìm giá trị lớn nhất.
    
- `MIN()`: Tìm giá trị nhỏ nhất.
    

### Gom nhóm dữ liệu

- `GROUP BY`: Nhóm các hàng có cùng giá trị trong một hoặc nhiều cột lại với nhau thành các hàng tóm tắt. Lệnh này gần như luôn đi kèm với các hàm tổng hợp để thực hiện tính toán trên mỗi nhóm.
    
- `HAVING`: Được sử dụng sau `GROUP BY` để lọc các nhóm dựa trên một điều kiện. Điều kiện này thường áp dụng cho kết quả của một hàm tổng hợp.
    

SQL

```
SELECT ChuyenMuc, COUNT(*) AS SoLuongSanPham
FROM SanPham
GROUP BY ChuyenMuc
HAVING COUNT(*) > 10; -- Chỉ hiển thị các chuyên mục có nhiều hơn 10 sản phẩm
```

### Thứ tự thực thi logic và sự khác biệt giữa WHERE và HAVING

Một trong những điểm gây nhầm lẫn nhất cho người mới học SQL là sự khác biệt giữa `WHERE` và `HAVING`. Cả hai đều dùng để lọc, nhưng chúng hoạt động ở các giai đoạn khác nhau trong quá trình xử lý truy vấn của cơ sở dữ liệu. Mặc dù chúng ta viết câu lệnh theo thứ tự

`SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY`, hệ quản trị CSDL không thực thi theo thứ tự đó. Thứ tự xử lý logic thực tế là:

1. `FROM` và `JOIN`: Xác định và kết hợp các bảng nguồn.
    
2. `WHERE`: Lọc các hàng riêng lẻ dựa trên các điều kiện.
    
3. `GROUP BY`: Gom các hàng đã được lọc thành các nhóm.
    
4. `HAVING`: Lọc các nhóm đã được tạo.
    
5. `SELECT`: Chọn các cột cuối cùng và tính toán các biểu thức.
    
6. `DISTINCT`: Loại bỏ các hàng trùng lặp.
    
7. `ORDER BY`: Sắp xếp tập kết quả cuối cùng.
    
8. `LIMIT` / `TOP`: Lấy ra một phần của kết quả đã sắp xếp.
    

Từ thứ tự này, có thể rút ra kết luận:

- `WHERE` được thực thi ở bước 2, **trước khi** dữ liệu được gom nhóm (bước 3). Do đó, `WHERE` chỉ có thể lọc dựa trên dữ liệu của từng hàng riêng lẻ và không thể sử dụng các hàm tổng hợp (như `SUM()`, `COUNT()`) vì chúng chưa được tính toán.
    
- `HAVING` được thực thi ở bước 4, **sau khi** dữ liệu đã được gom nhóm và các hàm tổng hợp đã được tính toán cho mỗi nhóm. Do đó, `HAVING` được thiết kế đặc biệt để lọc dựa trên kết quả của các hàm tổng hợp.
    

Một cách dễ hình dung: `WHERE` là bộ lọc "đầu vào" cho các hàng, còn `HAVING` là bộ lọc "đầu ra" cho các nhóm.

## Phần 7: Sức Mạnh Kết Nối - Làm Chủ Các Loại JOIN

Trong một cơ sở dữ liệu quan hệ được thiết kế tốt, dữ liệu thường được chia nhỏ ra nhiều bảng để tránh lặp lại và đảm bảo tính nhất quán. Lệnh `JOIN` chính là công cụ mạnh mẽ cho phép chúng ta kết hợp dữ liệu từ hai hoặc nhiều bảng này lại với nhau dựa trên các cột có liên quan (thường là cặp khóa chính - khóa ngoại).

### Phân tích chi tiết từng loại JOIN

- `INNER JOIN` (hoặc `JOIN`): Đây là loại `JOIN` phổ biến nhất. Nó trả về các bản ghi chỉ khi có giá trị khớp ở cả hai bảng tham gia. Về mặt lý thuyết tập hợp, đây chính là phép giao (intersection).
    
- `LEFT JOIN` (hoặc `LEFT OUTER JOIN`): Trả về **tất cả** các bản ghi từ bảng bên trái và các bản ghi khớp từ bảng bên phải. Nếu không có sự khớp nối, các cột tương ứng của bảng bên phải sẽ có giá trị `NULL`.
    
- `RIGHT JOIN` (hoặc `RIGHT OUTER JOIN`): Hoạt động ngược lại với `LEFT JOIN`. Nó trả về **tất cả** các bản ghi từ bảng bên phải và các bản ghi khớp từ bảng bên trái. Nếu không có sự khớp nối, các cột của bảng bên trái sẽ có giá trị `NULL`.
    
- `FULL OUTER JOIN`: Kết hợp kết quả của cả `LEFT JOIN` và `RIGHT JOIN`. Nó trả về tất cả các bản ghi khi có sự khớp ở một trong hai bảng. Nếu một hàng ở bảng này không có hàng khớp ở bảng kia, các cột của bảng kia sẽ là `NULL`. Đây là phép hợp (union) của hai tập hợp.
    
- `CROSS JOIN`: Trả về tích Descartes của hai bảng. Nó kết hợp mỗi hàng của bảng thứ nhất với tất cả các hàng của bảng thứ hai. Loại `JOIN` này có thể tạo ra một tập kết quả rất lớn và cần được sử dụng một cách cẩn trọng.
    
- `SELF JOIN`: Đây không phải là một loại `JOIN` riêng biệt mà là một kỹ thuật, trong đó một bảng được kết nối với chính nó. Kỹ thuật này rất hữu ích để truy vấn các dữ liệu có cấu trúc phân cấp, ví dụ như trong một bảng `NhanVien`, có cột `MaNguoiQuanLy` tham chiếu trở lại cột `MaNhanVien` trong cùng bảng đó.
    

**Bảng so sánh các loại JOIN**

|Loại JOIN|Kết Quả Trả Về|Kịch Bản Sử Dụng Điển Hình|
|---|---|---|
|**INNER JOIN**|Chỉ các hàng có khóa khớp ở cả hai bảng.|Lấy danh sách khách hàng đã từng đặt hàng.|
|**LEFT JOIN**|Tất cả hàng từ bảng trái, và hàng khớp từ bảng phải.|Lấy danh sách tất cả khách hàng và đơn hàng của họ (kể cả những khách hàng chưa từng đặt hàng).|
|**RIGHT JOIN**|Tất cả hàng từ bảng phải, và hàng khớp từ bảng trái.|Lấy danh sách tất cả sản phẩm và thông tin người đã mua chúng (kể cả những sản phẩm chưa từng được bán).|
|**FULL OUTER JOIN**|Tất cả hàng từ cả hai bảng.|Lấy danh sách tất cả nhân viên và tất cả phòng ban, ghép nối thông tin nếu nhân viên thuộc phòng ban đó.|
|**CROSS JOIN**|Mọi tổ hợp hàng có thể có giữa hai bảng.|Tạo dữ liệu thử nghiệm, ví dụ: ghép mọi size áo với mọi màu sắc để tạo danh sách sản phẩm.|
|**SELF JOIN**|Bảng tự kết nối với chính nó.|Tìm tên của mỗi nhân viên và tên của người quản lý trực tiếp của họ trong cùng một bảng nhân sự.|

## Phần 8: Giao Dịch và Bảo Mật - Đảm Bảo An Toàn Dữ Liệu

Việc thao tác với dữ liệu không chỉ dừng lại ở truy vấn mà còn phải đảm bảo tính toàn vẹn và bảo mật. Đây là lúc các lệnh TCL và DCL phát huy vai trò.

### TCL - Transaction Control Language

Một **giao dịch (transaction)** là một chuỗi các thao tác SQL được thực hiện như một đơn vị công việc logic duy nhất. Nguyên tắc của giao dịch là "hoặc tất cả thành công, hoặc tất cả thất bại". Ví dụ kinh điển là giao dịch chuyển tiền: việc trừ tiền từ tài khoản A và cộng tiền vào tài khoản B phải cùng xảy ra, nếu một trong hai bước thất bại, toàn bộ giao dịch phải được hủy bỏ.

Độ tin cậy của giao dịch được đảm bảo bởi bốn thuộc tính, gọi là **ACID**:

- **Atomicity (Tính nguyên tử):** Giao dịch là không thể chia nhỏ.
    
- **Consistency (Tính nhất quán):** Giao dịch đưa cơ sở dữ liệu từ một trạng thái hợp lệ này sang một trạng thái hợp lệ khác.
    
- **Isolation (Tính cô lập):** Các giao dịch đồng thời không ảnh hưởng lẫn nhau.
    
- **Durability (Tính bền vững):** Một khi giao dịch đã được xác nhận thành công, các thay đổi của nó sẽ tồn tại vĩnh viễn, ngay cả khi hệ thống gặp sự cố. 20
    

Các lệnh TCL chính bao gồm:

- `COMMIT`: Lưu vĩnh viễn các thay đổi của giao dịch hiện tại vào cơ sở dữ liệu.
    
- `ROLLBACK`: Hủy bỏ tất cả các thay đổi đã được thực hiện trong giao dịch hiện tại, đưa cơ sở dữ liệu trở về trạng thái trước khi giao dịch bắt đầu.
    
- `SAVEPOINT`: Đặt một điểm lưu tạm thời bên trong một giao dịch. Điều này cho phép `ROLLBACK` về một điểm cụ thể mà không cần phải hủy bỏ toàn bộ giao dịch.
    

### DCL - Data Control Language

DCL là nhóm lệnh dùng để quản lý quyền truy cập của người dùng đối với các đối tượng trong cơ sở dữ liệu, đảm bảo rằng chỉ những người được ủy quyền mới có thể thực hiện các hành động nhất định.

- `GRANT`: Cấp quyền cho một người dùng hoặc một nhóm người dùng. Ví dụ: cấp quyền `SELECT`, `INSERT` trên một bảng cụ thể.
    
- `REVOKE`: Thu hồi lại các quyền đã được cấp trước đó.
    

SQL

```
-- Cấp quyền SELECT trên bảng SanPham cho người dùng 'analyst'
GRANT SELECT ON SanPham TO analyst;

-- Thu hồi quyền INSERT trên bảng SanPham từ người dùng 'analyst'
REVOKE INSERT ON SanPham FROM analyst;
```

Việc cấp quyền trực tiếp trên các bảng dữ liệu gốc đôi khi có thể làm lộ thông tin nhạy cảm (ví dụ: cột `Luong` trong bảng `NhanVien`). Để giải quyết vấn đề này, DCL thường được sử dụng kết hợp với các đối tượng cơ sở dữ liệu khác như `View` và `Stored Procedure` để tạo ra một cơ chế bảo mật đa lớp và linh hoạt hơn. Thay vì cấp quyền `SELECT` trực tiếp trên bảng `NhanVien`, quản trị viên có thể tạo một `View` không chứa cột `Luong` và chỉ cấp quyền `SELECT` trên `View` đó cho người dùng. Tương tự, thay vì cấp quyền

`UPDATE` trên bảng, quản trị viên có thể tạo một `Stored Procedure` để thực hiện một hành động cụ thể (như tăng lương) và chỉ cấp quyền thực thi (`EXECUTE`) thủ tục đó. Cách tiếp cận này che giấu cấu trúc dữ liệu phức tạp và giới hạn các hành động mà người dùng có thể thực hiện, tăng cường đáng kể tính bảo mật.

## Phần 9: Tối Ưu Hóa và Các Đối Tượng Nâng Cao

Để làm việc hiệu quả với các hệ thống cơ sở dữ liệu lớn, việc hiểu và sử dụng các đối tượng nâng cao để tối ưu hóa hiệu suất là vô cùng cần thiết.

### Index (Chỉ mục)

- **Khái niệm:** Một chỉ mục (Index) là một cấu trúc dữ liệu đặc biệt được sử dụng để tăng tốc độ truy xuất dữ liệu từ một bảng. Nó hoạt động tương tự như mục lục ở cuối một cuốn sách. Thay vì phải lật từng trang (quét toàn bộ bảng - table scan) để tìm thông tin, cơ sở dữ liệu có thể sử dụng chỉ mục để đi thẳng đến vị trí của dữ liệu cần tìm.
    
- **Lợi ích và Đánh đổi:** Lợi ích chính của chỉ mục là tăng tốc đáng kể các truy vấn `SELECT` có mệnh đề `WHERE` hoặc các phép `JOIN`. Tuy nhiên, nó cũng có một cái giá phải trả: các thao tác ghi dữ liệu (`INSERT`, `UPDATE`, `DELETE`) sẽ trở nên chậm hơn, vì ngoài việc thay đổi dữ liệu trong bảng, cơ sở dữ liệu còn phải cập nhật cả cấu trúc của chỉ mục. Do đó, cần cân nhắc kỹ lưỡng việc tạo chỉ mục trên các bảng có tần suất ghi dữ liệu cao.
    
- **Cú pháp:**
    
    SQL
    
    ```
    CREATE INDEX idx_TenSanPham ON SanPham (TenSanPham);
    ```
    

### View (Khung nhìn)

- **Khái niệm:** Một View là một "bảng ảo" (virtual table), được định nghĩa bởi một câu lệnh `SELECT`. View không lưu trữ dữ liệu của riêng nó mà chỉ đơn giản là một "cửa sổ" để nhìn vào dữ liệu từ một hoặc nhiều bảng cơ sở. Mọi thao tác trên View thực chất sẽ được phản ánh xuống các bảng gốc.
    
- **Lợi ích:**
    
    - **Đơn giản hóa truy vấn phức tạp:** Một câu lệnh `JOIN` phức tạp qua nhiều bảng có thể được gói gọn trong một View. Sau đó, người dùng chỉ cần thực hiện một câu lệnh `SELECT` đơn giản từ View đó.
        
    - **Tăng cường bảo mật:** Cho phép giới hạn quyền truy cập của người dùng. Họ chỉ có thể xem và tương tác với dữ liệu thông qua View (ví dụ: một View không chứa các cột nhạy cảm như lương hoặc thông tin cá nhân).
        
    - **Tính nhất quán:** Đảm bảo rằng nhiều ứng dụng và người dùng khác nhau cùng truy cập vào một logic dữ liệu nhất quán được định nghĩa sẵn trong View.
        
- **Cú pháp:**
    
    SQL
    
    ```
    CREATE VIEW v_SanPhamGiaCao AS
    SELECT TenSanPham, Gia, ChuyenMuc
    FROM SanPham
    WHERE Gia > 1000000;
    ```
    

### Stored Procedure (Thủ tục lưu trữ)

- **Khái niệm:** Một Stored Procedure (thường gọi tắt là SP) là một nhóm các câu lệnh SQL đã được biên dịch trước và được lưu trữ ngay trong cơ sở dữ liệu. Nó có thể nhận các tham số đầu vào, thực hiện một chuỗi logic phức tạp và trả về kết quả.
    
- **Lợi ích:**
    
    - **Tái sử dụng mã:** Viết một lần, gọi nhiều lần từ các ứng dụng khác nhau mà không cần lặp lại mã.
        
    - **Tăng hiệu suất:** Vì các SP đã được biên dịch và tối ưu hóa sẵn, việc thực thi chúng thường nhanh hơn so với việc gửi các câu lệnh SQL riêng lẻ từ ứng dụng qua mạng.
        
    - **Giảm lưu lượng mạng:** Thay vì gửi một khối mã SQL dài, ứng dụng chỉ cần gửi một lệnh gọi SP ngắn gọn.
        
    - **Tăng cường bảo mật:** Tương tự như View, có thể cấp cho người dùng quyền thực thi một SP mà không cần cấp quyền trực tiếp trên các bảng cơ sở. Điều này giúp kiểm soát chặt chẽ các hành động và là một biện pháp hiệu quả để chống lại các cuộc tấn công SQL Injection.
        
- **Cú pháp (ví dụ trong SQL Server):**
    
    SQL
    
    ```
    CREATE PROCEDURE sp_TimSanPhamTheoGia
        @GiaToiThieu DECIMAL(10, 2)
    AS
    BEGIN
        SELECT TenSanPham, Gia FROM SanPham WHERE Gia >= @GiaToiThieu;
    END;
    ```
    

## Phần 10: Tổng Kết và Lộ Trình Học Tập Tiếp Theo

Qua các phần trên, chúng ta đã cùng nhau xây dựng một nền tảng vững chắc về SQL, từ việc hiểu các khái niệm cơ bản về cơ sở dữ liệu quan hệ, phân loại và nắm vững cú pháp của 5 họ lệnh chính (DDL, DML, DQL, DCL, TCL), cho đến việc làm chủ các kỹ thuật mạnh mẽ như `JOIN`, `GROUP BY` và các đối tượng nâng cao như `Index`, `View`, `Stored Procedure`.

Tuy nhiên, SQL là một kỹ năng cần được mài giũa qua thực hành liên tục. Kiến thức lý thuyết là quan trọng, nhưng việc áp dụng chúng để giải quyết các bài toán dữ liệu thực tế mới thực sự giúp bạn trở thành một chuyên gia. Các nền tảng như LeetCode, HackerRank hay các bộ dữ liệu công khai là những nguồn tài nguyên tuyệt vời để luyện tập.

Sau khi đã nắm vững các kiến thức trong cẩm nang này, đây là một vài gợi ý cho lộ trình học tập tiếp theo của bạn:

- **Hàm cửa sổ (Window Functions):** Đây là một bước tiến lớn trong phân tích dữ liệu. Các hàm như `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`, `LEAD()`, `LAG()` cho phép thực hiện các phép tính phức tạp trên một "cửa sổ" các hàng liên quan mà không làm thay đổi kết quả của truy vấn chính.
    
- **Tối ưu hóa truy vấn (Query Optimization):** Học cách đọc và hiểu kế hoạch thực thi (Execution Plan) của một câu lệnh SQL để xác định các điểm nghẽn về hiệu suất và tìm cách cải thiện chúng.
    
- **Chuyên sâu về một RDBMS cụ thể:** Mỗi hệ quản trị cơ sở dữ liệu như PostgreSQL, SQL Server, hay MySQL đều có những tính năng và cú pháp đặc thù. Việc tìm hiểu sâu về một hệ thống sẽ mở ra nhiều khả năng mạnh mẽ hơn.
    

Hành trình làm chủ SQL là một cuộc marathon, không phải là một cuộc chạy nước rút. Hy vọng rằng cuốn cẩm nang này sẽ là người bạn đồng hành đáng tin cậy trên chặng đường chinh phục thế giới dữ liệu của bạn.

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*