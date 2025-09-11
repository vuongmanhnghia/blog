---
title: Hướng dẫn setup môi trường App Development trên nixos best practice
meta_title: Hướng dẫn setup môi trường App Development trên nixos best practice
description: Sử dụng triết lý của Nix ứng dụng trong việc triển khai môi trường lập trình ứng dụng sao cho tối ưu và tốt nhất.
date: 2025-09-09
image: /images/thumbnails/app-development.png
categories:
  - environment
  - OS
author: Nagih
tags:
  - app
  - NixOS
draft: false
---
Sử dụng triết lý của Nix ứng dụng trong việc triển khai môi trường lập trình ứng dụng sao cho tối ưu và tốt nhất.
<!--more-->

Trong bài viết này, tôi sẽ hướng dẫn các bạn setup môi trường lập trình ứng dụng trên **NixOS bằng IntelliJ IDEA và Nix Flakes** thay vì sử dụng **Android Studio**. Đây là quy trình hiệu quả và phù hợp với triết lý của NixOS

**Quá trình này quản lý 2 nguyên tắc cốt lõi của NixOS**

- **Quản lý hệ thống bằng cách khai báo (Declarative System Management):** Mọi package, phần mềm, cấu hình hệ thống được define trong file `configuration.nix`, giúp hệ thống luôn có thể tái tạo và có tính nhất quán

- **Môi trường phát triển biệt lập (Isolated Development Environments):** Sử dụng `nix-shell` để tạo ra môi trường chứa chính xác phiên bản của các công cụ đã được define cho từng project mà không làm ảnh hưởng tới hệ thống chính

---
## Các bước tiến hành
### Bước 1: Cài đặt các công cụ cơ bản trên hệ thống

Điều đầu tiên, vì sử dụng IntelliJ IDEA nên bắt buộc rằng nó được cài trên hệ thống của bạn và đã bật tính năng **Flakes của NixOS**

- Mở file cấu hình hệ thống NixOS của bạn
	
- Thêm package `jetbrains.idea-community` hoặc `idea-ultimate`(nếu có premium) vào danh sách `environment.systemPackages`
	
- Trong bước này có thể thêm JDK mặc định nếu muốn, nhưng việc define JDK cho từng project sẽ tốt hơn nếu bạn không muốn cài trên hệ thống chính

	```nix
	# .../configuration.nix
	{ config, pkgs, ... }:
		
	{
	  # Bật tính năng Flakes và nix-command mới 
	  nix.settings.experimental-features = [ "nix-command" "flakes" ];
		
	  environment.systemPackages = with pkgs; [
	    git                        # Git để quản lý mã nguồn
	    jetbrains.idea-community   # Thêm IntelliJ IDEA vào cấu hình
	  ];
		  
	  # ... các cấu hình khác
	}
	```

- **Rebuild NixOS** để áp dụng thay đổi: `sudo nixos-rebuild switch`

### Bước 2: Tạo môi trường phát triển riêng cho Project

Đây là bước quan trọng nhất và là nơi sức mạnh của nix được thể hiện rõ nhất

- **Tạo thư mục chứa dự án**
	
	```bash
	mkdir my-app
	cd my-app
	```
	
- Tạo file `flake.nix`. File này là trái tim của môi trường, nó sẽ define tất cả những công cụ cần thiết trong project: JDK, Maven, Gradle, ... 

	```nix
	{
	  description = "Môi trường phát triển Android trên NixOS (kênh Unstable)";
	
	  inputs = {
	    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
	    flake-utils.url = "github:numtide/flake-utils";
	  };
	
	  outputs = { self, nixpkgs, flake-utils }:
	    flake-utils.lib.eachDefaultSystem (system:
	      let
	        # Cấu hình để tự động chấp nhận giấy phép Android SDK
	        pkgs = import nixpkgs {
	          inherit system;
	          config = {
	            allowUnfree = true;
	            android_sdk.accept_license = true;
	          };
	        };
	
	        # "Lắp ráp" môi trường SDK bằng hàm và tham số tương thích
	        android-sdk-env = pkgs.androidenv.composeAndroidPackages {
	          platformVersions = [ "34" "36" ];
	          buildToolsVersions = [ "34.0.0" "36.0.0" ];
	
	          includeEmulator = true;
	          platformToolsVersion = "36.0.0";
	          cmdLineToolsVersion = "11.0";
	
	          includeSystemImages = true;
	          systemImageTypes = [ "google_apis" ];
	          abiVersions = [ "x86_64" ];
	        };
	      in
	      {
	        devShells.default = pkgs.mkShell {
	          buildInputs = [
	            # Hàm cũ trả về một attribute set, cần truy cập .androidsdk
	            android-sdk-env.androidsdk
	            pkgs.jdk
	            pkgs.qt6.qtwayland
	          ];
	
	          shellHook = ''
	            # Đường dẫn SDK cũng cần .androidsdk
	            export ANDROID_SDK_ROOT="${android-sdk-env.androidsdk}/libexec/android-sdk"
	            export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/emulator:$PATH"
	            export QT_QPA_PLATFORM=xcb
	            echo "✅ Môi trường Android cho API 36 (Unstable) đã sẵn sàng."
	          '';
	        };
	      });
	}
	```

 	>**Lưu ý:** Có thể thay đổi các version máy ảo Android cho phù hợp, tuy nhiên các công cần sử dụng đúng version để có thể hoạt động được với nhau (platformVersions, buildToolsVersions , platformToolsVersion) 
 	
 - **Install và truy cập vào `nix-shell`**

	```bash
	nix develop
	```

	```bash
	➜ nix develop
	✅ Môi trường Android đã sẵn sàng.
	
	[nagih@nixos:~/Workspaces/noob/app/my-app]$ 
	```

### Bước 3: Cấu hình IntelliJ IDEA

Bây giờ, ta sẽ khởi động IntelliJ IDEA bên trong môi trường Nix để có thể nhận diện được tất cả công cụ

- **Khởi động IntelliJ:** Từ terminal, gõ lệnh
	
	```bash
	idea-community .
	```
	
- **Cài đặt Plugin Android mới**: Nếu đây là lần đầu sử dụng IntelliJ cho Android, hãy vào `Plugins` -> `Marketplace`, Tìm kiếm `Android` và cài đặt

	![Image Description](/images/Pasted%20image%2020250909150919.png)

- **Tạo dự án mới**
		
	- Trong IntelliJ, vào `Projects` -> `New Project` 
		
	- Chọn `Android` từ danh sách `Generators` bên trái
		
	- Chọn template, ví dụ `Empty Views Activity` và nhấn next
		
		![Image Description](/images/Pasted%20image%2020250909151418.png)
		
	- Điền thông tin project
		
	- **Quan trọng:** Ở mục `Build configuration language` cần phù hợp với language đã được khai báo trong `flake.nix` (`kotlin` / `groovy`)
		
		![Image Description](/images/Pasted%20image%2020250909152633.png)

> **Nguyên lý hoạt động:** Khi khởi chạy từ `nix develop`, IntelliJ kế thừa tất cả các biến môi trường, bao gồm `PATH` và `ANDROID_SDK_ROOT`. Nhờ vậy, nó tự động biết JDK và Android SDK nằm ở đâu trong `/nix/store` mà không cần bạn phải cấu hình thủ công.

### Bước 4: Tạo máy ảo AVD (Android Virtual Device)

- **Close hoàn toàn IntelliJ IDEA** 

- **Xác minh** công cụ `emulator` và `avdmanager` có tồn tại trong môi trường hay không
		
	```bash
	which emulator
	which avdmanager
	```
		
	- Nếu kết quả có các đường dẫn trỏ tới `/nix/store/...` cho cả 2 lệnh thì xin chúc mừng
		
	- Nếu không thấy kết quả -> Điều này có nghĩa là `flake.nix` của bạn đang có vấn đề, hoặc có thể bạn chưa truy cập và `nix develop`
		
- **Kiểm tra System Image**

	- Run command
		```bash
		sdkmanager --list_installed
		```
	- Kết quả đúng sẽ có dạng như này
		```bash
		Installed packages: --------------------------------------
		...
		platforms;android-36                          | 1 | Android SDK Platform 36
		system-images;android-36;google_apis;x86_64   | 1 | Google APIs Intel x86_64 Atom System Image
		...
		```

- **Create máy ảo (AVD)** thông qua `andmanager`. `package` là system image đã được cài ở phía trên
	
	```bash
	avdmanager create avd --name "Pixel_API36" --package "system-images;android-36;google_apis;x86_64" --device "pixel_7_pro"
	```
	- `name`: Tên AVD

	- `package`: System image

	- `device`: Loại thiết bị, nếu muốn kiểm tra có các thiết bị nào, hãy dùng lệnh `avdmanager list device`
### Bước 5: Khởi chạy tạo máy ảo AVD

- Khởi động lại IntelliJ IDEA trong môi trường `nix-shell`

	```bash
	idea-community .
	```

- **Open project** mà khi nãy đã tạo (nếu đã bị thoát ra)

	- Lúc này bạn sẽ nhìn thấy máy ảo AVD trong phần **devices**
		
		![Image Description](/images/Pasted%20image%2020250909203943.png)
		
	- Tuy nhiên, bạn có thể thấy xuất hiện dấu `!`, điều này là bình thường vì chưa run AVD
		
- **Khởi chạy máy ảo AVD**

	- Open `terminal` bên trong IntelliJ IDEA

	- **Run command**

		```bash
		emulator -avd [avd-name] &
		```

		Sau khi run AVD thành công sẽ xuất hiện cửa sổ AVD đồng thời máy ảo AVD trong phần **Devices** sẽ mất dấu `!`

Tới đây là đã xong, bạn chỉ cần run project là sẽ nhìn thấy dòng chữ `Hello World!` bên trong cửa sổ máy ảo.

---
## Các lỗi phổ biến
### 1. Lỗi khi tạo dự án

![Image Description](/images/Pasted%20image%2020250911225113.png)
#### Nguyên nhân

Lỗi này xảy ra do IntelliJ mặc định sử dụng template có sẵn (API 34) nhưng trong `flake.nix` difine API khác

- **Cố gắng tải API 34:** Khi thấy công thức yêu cầu API 34 mà trong bếp không có, nó sẽ cố gắng tự đi "chợ" (tự tải về) và đặt vào kho (`/nix/store`).
    
- **Bị NixOS chặn lại:** NixOS thấy IntelliJ đang cố ghi vào "kho" chỉ đọc, nên đã chặn lại và báo lỗi `Failed to read or create install properties file`.34
#### Giải pháp

Truy cập vào môi trường `nix-shell` 

1. **Copy lấy đường dẫn của `$ANDROID_SDK_ROOT`**
	
	```bash
	echo $ANDROID_SDK_ROOT
	```
	
2. **Cấu hình cho IntelliJ**
	
	- Truy cập `File` -> `Project Structure...`
		
	- Vào tab `Platform Settings` -> `SDKs`
		
	- Nhấn **`+` -> Add Android SDK...** và dán đường dẫn `$ANDROID_SDK_ROOT` (đường dẫn này đang trỏ đến SDK của bạn).
		
	- Trong phần `Build target` sẽ xuất hiện SDK của bạn
	
3. **Cập nhật `build.gradle`**
	
	- Mở file `app/build.gradle.kts`
    
	- Thay đổi `compileSdk` và `targetSdk` thành SDK mà bạn đã define (36)
	
4. **Đồng bộ Gradle:**
	
	- Nhấn nút **"Sync Now"**.
	

### 2. "The skin directory, does not point to valid skin"

Lỗi này có nghĩa là máy ảo (AVD) đang cố gắng sử dụng một **"skin"** (bộ giao diện mô phỏng viền cứng của điện thoại), nhưng không thể tìm thấy các file của skin đó ở đường dẫn được chỉ định.

#### Giải pháp 1: Tắt Skin trong Cài đặt Máy ảo (Cách dễ nhất)

Cách đơn giản và hiệu quả nhất là yêu cầu máy ảo không cần tải skin nữa.

1. Mở **Device Manager** trong IntelliJ.
    
2. Tìm đến máy ảo đang bị lỗi của bạn và nhấn vào biểu tượng **Edit** (hình cây bút chì) ở cột Actions.
    
3. Cửa sổ "Virtual Device Configuration" sẽ hiện ra. Hãy tìm đến mục **"Enable Device Frame"** (Bật khung thiết bị).
    
4. **Bỏ dấu tick** ở ô này.
    
5. Nhấn **Finish** để lưu lại thay đổi.
    

Sau khi tắt skin, hãy thử khởi động lại máy ảo. Lỗi sẽ biến mất và máy ảo sẽ hiển thị dưới dạng một cửa sổ đơn giản chỉ có màn hình.

---

#### Giải pháp 2: Sửa file cấu hình thủ công (Cách trực tiếp)

Nếu bạn không tìm thấy tùy chọn trong giao diện, bạn có thể chỉnh sửa file cấu hình trực tiếp.

1. Mở terminal và điều hướng đến thư mục cấu hình của máy ảo. Thay `TenMayAo.avd` bằng tên máy ảo của bạn (ví dụ: `Pixel8Pro_API35.avd`):
    
    ```bash
    cd ~/.android/avd/TenMayAo.avd/
    ```
    
2. Mở file `config.ini` bằng một trình soạn thảo văn bản (ví dụ: `nano config.ini`).
    
3. Tìm các dòng bắt đầu bằng `skin.name` và `skin.path`.
    
4. Thay đổi giá trị của chúng thành `_no_skin` hoặc xóa cả hai dòng đó đi.
    
    **Ví dụ, sửa từ:**
    
    ```
    skin.name = pixel_8_pro
    skin.path = /some/invalid/nix/store/path
    ```
    
    **Thành:**
    
    ```
    skin.name = _no_skin
    skin.path = _no_skin
    ```
    
5. Lưu file và thử khởi động lại máy ảo.