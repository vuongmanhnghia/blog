---
title: Hướng dẫn đầy đủ command `du`
date: 2026-01-17
image:
categories:
  - linux
tags:
  - command
draft: false
---

Lệnh `du` (**D**isk **U**sage) là công cụ mạnh mẽ để kiểm tra dung lượng ổ đĩa, nhưng nếu chỉ gõ `du` trần thì kết quả trả về sẽ rất rối mắt và khó đọc

<!--more-->

---

Để dùng `du` như một "Pro" (chuyên nghiệp, hiệu quả), bạn cần kết hợp các cờ (flags) và đường ống (pipe) để lọc dữ liệu. Dưới đây là các tuyệt chiêu hay dùng nhất:

### 1. Combo "Huyền thoại": Xem tổng dung lượng thư mục hiện tại

Đây là lệnh bạn sẽ dùng 90% thời gian.
```bash
du -sh
```

Hoặc xem cụ thể từng thư mục con cấp 1:
```bash
du -sh *
```

*   **`-s` (summary):** Chỉ hiện tổng số, không liệt kê từng file nhỏ bên trong.
	
*   **`-h` (human-readable):** Hiển thị đơn vị dễ đọc (K, M, G) thay vì số block.

### 2. Combo "Thám tử": Tìm 10 thư mục/file nặng nhất (Quan trọng)

Khi ổ cứng bị đầy, bạn cần biết thằng nào đang chiếm chỗ. Lệnh `du` không tự sắp xếp, nên ta phải kết hợp với `sort`.

```bash
du -ah . | sort -rh | head -n 10
```

*   **`-a` (all):** Hiển thị cả file lẫn thư mục (để bắt được các file log hoặc backup lẻ tẻ nhưng nặng).
	
*   **`.`**: Thư mục hiện tại (hoặc thay bằng `/var`, `/home`...).
	
*   **`sort -rh`**: Sắp xếp (sort) theo dạng đảo ngược (**r**everse) và hiểu được đơn vị K/M/G (**h**uman-numeric-sort).
	
*   **`head -n 10`**: Chỉ lấy 10 dòng đầu tiên (top 10 nặng nhất).

### 3. Combo "Khoan cắt bê tông": Giới hạn độ sâu thư mục

Nếu bạn muốn kiểm tra thư mục gốc `/` nhưng sợ nó liệt kê hàng triệu file, hãy dùng `--max-depth` (hoặc `-d`).

```bash
sudo du -h --max-depth=1 /
```

*   **`--max-depth=1` (hoặc `-d 1`):** Chỉ hiển thị dung lượng của các thư mục con cấp 1, không đi sâu hơn. Rất gọn gàng để nhìn tổng quan.

### 4. Combo "Tính tổng": Cộng dồn dung lượng

Đôi khi bạn muốn check dung lượng của một vài folder cụ thể và muốn biết tổng của chúng là bao nhiêu.

```bash
du -ch folder1 folder2 folder3
```
*   **`-c` (total):** Thêm một dòng "total" ở cuối cùng cộng dồn tất cả lại.

### 5. Combo "Lọc rác": Loại trừ file không cần thiết
Bạn muốn tính dung lượng thư mục web nhưng muốn bỏ qua các file log hoặc cache?

```bash
du -sh --exclude="*.log" --exclude="cache" /var/www/html
```
*   **`--exclude`:** Bỏ qua các file hoặc thư mục khớp với mẫu.

### 6. Combo "Thời gian": Xem thư mục nào mới được sửa đổi

Vừa thấy dung lượng tăng vọt? Hãy xem thư mục nào vừa được cập nhật dung lượng gần đây kèm thời gian:

```bash
du -ha --time | sort -rh | head -n 10
```

*   **`--time`**: Hiển thị thêm cột ngày giờ sửa đổi lần cuối của file/folder.

---

### Bảng tóm tắt các phím tắt cho "Pro"

| Flag   | Ý nghĩa (Dễ nhớ)                            |
| :----- | :------------------------------------------ |
| `-h`   | **H**uman (Dễ đọc: KB, MB, GB)              |
| `-s`   | **S**ummary (Tóm tắt, không in dài dòng)    |
| `-a`   | **A**ll (Hiện cả file lẻ, không chỉ folder) |
| `-c`   | **C**ount/Total (Tính tổng ở dòng cuối)     |
| `-d N` | **D**epth (Độ sâu N cấp thư mục)            |

### ⭐ Pro Tip: Dùng `ncdu` (Nếu được phép cài đặt)

Nếu bạn được quyền cài thêm phần mềm, hãy quên `du` đi và cài `ncdu`. Đây là phiên bản `du` có giao diện đồ họa dòng lệnh, cho phép bạn dùng phím mũi tên để đi vào/ra các thư mục và xóa file trực tiếp cực nhanh.

**Cài đặt:**

```bash
sudo apt install ncdu
```

**Sử dụng:**

```bash
ncdu /
```