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

### Quá trình này quản lý 2 nguyên tắc cốt lõi của NixOS

- **Quản lý hệ thống bằng cách khai báo (Declarative System Management):** Mọi package, phần mềm, cấu hình hệ thống được define trong file `configuration.nix`, giúp hệ thống luôn có thể tái tạo và có tính nhất quán

- **Môi trường phát triển biệt lập (Isolated Development Environments):** Sử dụng `nix-shell` để tạo ra môi trường chứa chính xác phiên bản của các công cụ đã được define cho từng project mà không làm ảnh hưởng tới hệ thống chính

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

- **Tạo thư mục dự án và cd vào đó**

```bash
mkdir my-app
cd my-app
```

- Trong folder này, tạo một file là `flake.nix`. File này là trái tim của môi trường, nó sẽ define tất cả những công cụ cần thiết trong project: JDK, Maven, Gradle, ... 

```nix
{
  description = "Môi trường phát triển Android trên NixOS";

  # Khai báo các nguồn đầu vào
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  # Định nghĩa đầu ra của flake
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config = {
            allowUnfree = true;
            android_sdk.accept_license = true;
          };
        };
        
        # Lắp ráp môi trường SDK từ các linh kiện của androidenv
        android-sdk-env = pkgs.androidenv.composeAndroidPackages {
          platformVersions = [ "34" ];           # API level
          buildToolsVersions = [ "34.0.0" ];     # Version build-tools
          
          # Máy ảo và CLI (Chú ý nếu muốn thay đổi)
          includeEmulator = true;
          includeSystemImages = true;
          systemImageTypes = [ "google_apis" ];  # Loại system image
          abiVersions = [ "x86_64" ];            # Architechture
          platformToolsVersion = "34.0.5";
          cmdLineToolsVersion = "11.0";
        };
      in
      {
        # Định nghĩa môi trường shell cho lệnh `nix develop`
        devShells.default = pkgs.mkShell {
          # Các gói sẽ có trong môi trường
          buildInputs = [
            # Môi trường SDK đã lắp ráp ở trên
            android-sdk-env.androidsdk
            # pkgs.qt6.qtwayland # Nếu sử dụng wayland
            
            # Java Development Kit
            pkgs.jdk
            pkgs.gradle
            
            # Build configuration language
            pkgs.groovy             
          ];
          # Thiết lập biến môi trường để IntelliJ/Gradle tự tìm thấy SDK
          shellHook = ''
            export ANDROID_SDK_ROOT="${android-sdk-env.androidsdk}/libexec/android-sdk"
            export ANDROID_HOME="$ANDROID_SDK_ROOT"
            export PATH="$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools:$ANDROID_SDK_ROOT/emulator:$PATH"
			export QT_QPA_PLATFORM=xcb
            echo "✅ Môi trường Android đã sẵn sàng."
          '';
        };
      });
}
``````



> **Lưu ý:** Có thể thay đổi các version máy ảo Android cho phù hợp, tuy nhiên các công cần sử dụng đúng version để có thể hoạt động được với nhau (platformVersions, buildToolsVersions , platformToolsVersion) 

```bash
nix develop
```

- Lần đầu chạy, Nix sẽ install tất cả các công cụ được define

> **Nguyên lý hoạt động:** `flake.nix` định nghĩa chính xác những công cụ nào (JDK 17, Android SDK Platform 34, Build Tools 34.0.0, Emulator...) cần cho dự án. Lệnh `nix develop` đọc file này và tạo ra một shell tạm thời chứa đầy đủ và duy nhất các công cụ đó, cùng với các biến môi trường đã được cấu hình sẵn.

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

> Mỗi version IntelliJ sẽ có giao diện khác nhau nhưng cách thức hoạt động vẫn vậy nên đừng lo lắng nếu không giao diện không giống như mô tả nhé.



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

> Thông thường, AVD (Android Virtual Devices) sẽ được install thông qua `sdkmanager`
> ```bash
> sdkmanager "system-images;android-34;google_apis;x86_64"
> ```
> Tuy nhiên, do sự bất biến trong Nix Store, môi trường `nix-shell` được build từ các gói trong `/nix/store`, một thư mục chỉ `read-only`, `sdkmanager` được thiết kế để tải về và giải nén system image, platform-tools,... vào trong 1 thư mục SDK duy nhất và có thể bị ghi đè nên `sdkmanager` không thể sử dụng vì không có quyền ghi. Vì vậy nên trong `flake.nix` define system image. Dưới đây là minh họa khi sử dụng trực tiếp `sdkmanager`

```bash
[nagih@nixos:~/Workspaces/noob/app/my-app]$ sdkmanager "system-images;android-34;google_apis;x86_64" 
Warning: Failed to read or create install properties file.                      
[===                                    ] 10% Installing Google APIs Intel x86_6
```

- **Close hoàn toàn IntelliJ IDEA** 

- Xác minh công cụ `emulator` và `avdmanager` có tồn tại trong môi trường hay không
		
	```bash
	which emulator
	which avdmanager
	```
		
	- Nếu kết quả có các đường dẫn trỏ tới `/nix/store/...` cho cả 2 lệnh thì xin chúc mừng
		
	- Nếu không thấy kết quả -> Điều này có nghĩa là `flake.nix` của bạn đang có vấn đề, hoặc có thể bạn chưa truy cập và `nix develop`
		
- **Create máy ảo (AVD) thông qua `andmanager`

```bash
avdmanager create avd --name "TestAVD" --package "system-images;android-34;google_apis;x86_64"
```

> **Lưu ý:** `--package "system-images;android-34;google_apis;x86_64"`  package cần được match với package đã được defind trong `flake.nix`

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

		- Lúc này sẽ xuất hiện cửa sổ AVD đồng thời máy ảo AVD trong phần **Devices** sẽ mất dấu `!`
			
			![Image Description](/images/Pasted%20image%2020250909204618.png)
			

Tới đây là đã xong, bạn chỉ cần run project là sẽ nhìn thấy dòng chữ `Hello World!` bên trong cửa sổ máy ảo.


