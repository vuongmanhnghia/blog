---
title: Hướng dẫn setup môi trường App Development trên nixos best practice
date: 2025-09-09
image: /thumb/app-development.png
categories:
    - environment
    - OS
tags:
    - app
    - NixOS
draft: false
---

Sử dụng triết lý của Nix ứng dụng trong việc triển khai môi trường lập trình ứng dụng sao cho tối ưu và tốt nhất.

<!--more-->

Trong bài viết này, tôi sẽ hướng dẫn các bạn setup môi trường lập trình ứng dụng trên **NixOS bằng IntelliJ IDEA và Nix Flakes** thay vì sử dụng **Android Studio**. Đây là quy trình hiệu quả và phù hợp với triết lý của NixOS

**Quá trình này quản lý 2 nguyên tắc cốt lõi của NixOS**

-   **Quản lý hệ thống bằng cách khai báo (Declarative System Management):** Mọi package, phần mềm, cấu hình hệ thống được define trong file `configuration.nix`, giúp hệ thống luôn có thể tái tạo và có tính nhất quán

-   **Môi trường phát triển biệt lập (Isolated Development Environments):** Sử dụng `nix-shell` để tạo ra môi trường chứa chính xác phiên bản của các công cụ đã được define cho từng project mà không làm ảnh hưởng tới hệ thống chính

---

## Các bước tiến hành

### Bước 1: Cài đặt các công cụ cơ bản trên hệ thống

Điều đầu tiên, vì sử dụng IntelliJ IDEA nên bắt buộc rằng nó được cài trên hệ thống của bạn và đã bật tính năng **Flakes của NixOS**

-   Mở file cấu hình hệ thống NixOS của bạn
-   Thêm package `jetbrains.idea-community` hoặc `idea-ultimate`(nếu có premium) vào danh sách `environment.systemPackages`
-   Trong bước này có thể thêm JDK mặc định nếu muốn, nhưng việc define JDK cho từng project sẽ tốt hơn nếu bạn không muốn cài trên hệ thống chính

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

-   **Rebuild NixOS** để áp dụng thay đổi: `sudo nixos-rebuild switch`

### Bước 2: Tạo môi trường phát triển riêng cho Project

Đây là bước quan trọng nhất và là nơi sức mạnh của nix được thể hiện rõ nhất

-   **Tạo thư mục chứa dự án**

    ```bash
    mkdir my-app
    cd my-app
    ```

-   Tạo file `flake.nix`. File này là trái tim của môi trường, nó sẽ define tất cả những công cụ cần thiết trong project: JDK, Maven, Gradle, ...

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
              platformVersions = [ "36" ];
              buildToolsVersions = [ "36.0.0" ];

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

    > **Lưu ý:** Có thể thay đổi các version máy ảo Android cho phù hợp, tuy nhiên các công cần sử dụng đúng version để có thể hoạt động được với nhau (platformVersions, buildToolsVersions , platformToolsVersion)

-   **Install và truy cập vào `nix-shell`**

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

1. **Khởi động IntelliJ:** Từ terminal, gõ lệnh

    ```bash
    idea-community .
    ```

2. **Cài đặt Plugin Android mới**: Nếu đây là lần đầu sử dụng IntelliJ cho Android, hãy vào `Plugins` -> `Marketplace`, Tìm kiếm `Android` và cài đặt

    ![Image Description](posts/imagespasted-image-20250909150919png)

3. **Tạo dự án mới**

    - Trong IntelliJ, vào `Projects` -> `New Project`
    - Chọn `Android` từ danh sách `Generators` bên trái
    - Chọn template, ví dụ `Empty Views Activity` và nhấn next

        ![Image Description](posts/imagespasted-image-20250909151418png)

    - Điền thông tin project
    - **Quan trọng:** Ở mục `Build configuration language` cần phù hợp với language đã được khai báo trong `flake.nix` (`kotlin` / `groovy`)

        ![Image Description](posts/imagespasted-image-20250909152633png)

    - Sau khi tạo project, nếu thấy hiển thị lỗi này, hãy sửa theo hướng dẫn của phần **Các lỗi phổ biến** ở phía dưới

        ![Image Description](posts/imagespasted-image-20250911225113png)

### Bước 4: Tạo và khởi chạy máy ảo AVD (Android Virtual Device)

- **Phương pháp 1: Tạo trong intelliJ (Recommand)**
	
	1. **Truy cập** `Device Manager`
	
	2. **Nhấn `+`** để thêm mới AVD
	
	3. **Chọn thiết bị** mà bạn muốn sử dụng
	
	4. **Chọn `System Image`**
	
	    - **Chọn** tab `x86 Images`
			
	    - **Chọn** `System Image` mà bạn đã cài đặt (Không chọn bất kỳ system image nào có nút `Install`)
			
        - **Chọn lấy 1** `System Image` trong phần `x86 Images` (Không `Install`)
			
        - Thoát khỏi IntelliJ và `nix-shell`
			
        - Sửa file `flake.nix` theo `System Image` mà bạn đã chọn ở trên
			
        - **Kích hoạt** `nix develop` và **tiếp tục**
		
	5. **Khởi chạy** máy ảo
		
	    Sau khi tạo thành công máy ảo, có thể chưa hiện ngay trong phần `Device Manager`, lúc này hãy thoát IntelliJ và mở lại, bạn sẽ thấy nó. Sau đó chỉ cần nhấn nút `Run`.
	
- **Phương pháp 2: Sử dụng CLI (Chạy máy ảo với cửa sổ riêng)**
	
	1. **Close hoàn toàn IntelliJ IDEA**
	
	2. **Xác minh** công cụ `emulator` và `avdmanager` có tồn tại trong môi trường hay không
		
	    ```bash
	    which emulator
	    which avdmanager
	    ```
		
	    - Nếu kết quả có các đường dẫn trỏ tới `/nix/store/...` cho cả 2 lệnh thì xin chúc mừng
	    - Nếu không thấy kết quả -> Điều này có nghĩa là `flake.nix` của bạn đang có vấn đề, hoặc có thể bạn chưa truy cập và `nix develop`
		
	3. **Kiểm tra System Image**
	
	    ```bash
	    sdkmanager --list_installed
	    ```
	
	4. **Tạo máy ảo (AVD)** thông qua `andmanager`

	    ```bash
	    avdmanager create avd --name "Pixel_API36" --package "system-images;android-36;google_apis;x86_64" --device "pixel_7_pro"
	    ```
		
	    - `name`: Tên AVD
			
	    - `package`: System image
			
	    - `device`: Loại thiết bị, nếu muốn kiểm tra có các thiết bị nào, hãy dùng lệnh `avdmanager list device`
		
	5. **Khởi động IntelliJ**
		
	    - **Khởi động** lại IntelliJ IDEA trong môi trường `nix-shell`
		
	        ```bash
	        idea-community .
	        ```
		
	    - **Open project** mà khi nãy đã tạo (nếu đã bị thoát ra)
		
	    - Máy ảo AVD sẽ xuất hiện trong phần `Device Manager`. Bạn có thể thấy xuất hiện dấu `!`, điều này là bình thường vì chưa run AVD
			
	        ![Image Description](posts/imagespasted-image-20250909203943png)
		
	-   **Khởi chạy máy ảo AVD**
		
	    Open `terminal` bên trong IntelliJ IDEA
		
	    ```bash
	    emulator -avd [avd-name] &
	    ```
		
---

## Các lỗi phổ biến

### 1. Lỗi khi tạo dự án

![Image Description](posts/imagespasted-image-20250911225113png)

**Nguyên nhân**

Lỗi này xảy ra do IntelliJ mặc định sử dụng template có sẵn (API 34) nhưng trong `flake.nix` difine API khác

-   **Cố gắng tải API 34:** Khi thấy công thức yêu cầu API 34 mà trong bếp không có, nó sẽ cố gắng tự đi "chợ" (tự tải về) và đặt vào kho (`/nix/store`).
-   **Bị NixOS chặn lại:** NixOS thấy IntelliJ đang cố ghi vào "kho" chỉ đọc, nên đã chặn lại và báo lỗi `Failed to read or create install properties file`.34

**Giải pháp**

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

**Giải pháp 1: Tắt Skin trong Cài đặt Máy ảo (Cách dễ nhất)**

Cách đơn giản và hiệu quả nhất là yêu cầu máy ảo không cần tải skin nữa.

1. Mở **Device Manager** trong IntelliJ.
	
2. Tìm đến máy ảo đang bị lỗi của bạn và nhấn vào biểu tượng **Edit** (hình cây bút chì) ở cột Actions.
	
3. Cửa sổ "Virtual Device Configuration" sẽ hiện ra. Hãy tìm đến mục **"Enable Device Frame"** (Bật khung thiết bị).
	
4. **Bỏ dấu tick** ở ô này.
	
5. Nhấn **Finish** để lưu lại thay đổi.

Sau khi tắt skin, hãy thử khởi động lại máy ảo. Lỗi sẽ biến mất và máy ảo sẽ hiển thị dưới dạng một cửa sổ đơn giản chỉ có màn hình.

---

**Giải pháp 2: Sửa file cấu hình thủ công (Cách trực tiếp)**

Nếu bạn không tìm thấy tùy chọn trong giao diện, bạn có thể chỉnh sửa file cấu hình trực tiếp.

1. Mở terminal và điều hướng đến thư mục cấu hình của máy ảo. Thay `TenMayAo.avd` bằng tên máy ảo của bạn (ví dụ: `Pixel8Pro_API35.avd`):
	
    ```bash
    cd ~/.android/avd/TenMayAo.avd/
    ```
	
1. Mở file `config.ini` bằng một trình soạn thảo văn bản (ví dụ: `nano config.ini`).
	
2. Tìm các dòng bắt đầu bằng `skin.name` và `skin.path`.
	
3. Thay đổi giá trị của chúng thành `_no_skin` hoặc xóa cả hai dòng đó đi.
	
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
	
4. Lưu file và thử khởi động lại máy ảo.
