---
title: Docker Practical Guide
date: 2025-08-14
draft: false
tags:
  - docker
---
Hướng dẫn Thực hành: Container hóa Ứng dụng Dịch vụ đơn
<!--more-->

Phần 1: [Docker Principle](https://blog.nagih.io.vn/post/docker/docker/) 

Phần 2: [Docker CLI](https://blog.nagih.io.vn/post/docker/docker-cli/)

Phần 3: [Docker Dockerfile](https://blog.nagih.io.vn/post/docker/docker-dockerfile/)

Phần 4: [Docker Compose](https://blog.nagih.io.vn/post/docker/docker-compose/)

## Phần 5: Hướng dẫn Thực hành: Container hóa Ứng dụng Dịch vụ đơn

Lý thuyết là nền tảng, nhưng thực hành mới là cách tốt nhất để củng cố kiến thức. Phần này cung cấp các hướng dẫn từng bước để container hóa các ứng dụng đơn giản được viết bằng Go, Node.js và Python, ba trong số các ngôn ngữ phổ biến nhất trong phát triển web hiện đại.

### 4.1 Ví dụ 1: Máy chủ Web Go nhẹ

Go nổi tiếng với việc biên dịch ra các tệp nhị phân tĩnh, độc lập, rất phù hợp với container. Chúng ta sẽ tận dụng tính năng multi-stage build của Docker để tạo ra một image production siêu nhỏ.

1. Mã nguồn (main.go)

Tạo một tệp main.go với nội dung sau. Đây là một máy chủ web đơn giản lắng nghe trên cổng 8080.

Go

```
package main

import (
    "fmt"
    "log"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello from Go in a Docker Container!")
}

func main() {
    http.HandleFunc("/", handler)
    log.Println("Go web server starting on port 8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

2. Dockerfile

Tạo một tệp tên là Dockerfile (không có phần mở rộng) với nội dung sau:

Dockerfile

```
# Stage 1: Build the application
FROM golang:1.21-alpine AS builder

# Set the Current Working Directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum./

# Download all dependencies. Dependencies will be cached if the go.mod and go.sum files are not changed
RUN go mod download

# Copy the source code
COPY . .

# Build the Go app
# CGO_ENABLED=0 is for static builds
# -o /go-app builds the executable to /go-app
RUN CGO_ENABLED=0 GOOS=linux go build -o /go-app.

# Stage 2: Create the final, lightweight image
FROM alpine:latest

# Copy the pre-built binary file from the previous stage
COPY --from=builder /go-app /go-app

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the executable
CMD ["/go-app"]
```

**Giải thích Dockerfile:**

- **Stage 1 (`builder`):** Chúng ta bắt đầu với image `golang:1.21-alpine`, chứa tất cả các công cụ cần thiết để biên dịch mã Go. Chúng ta sao chép mã nguồn và biên dịch nó thành một tệp nhị phân tĩnh duy nhất tại `/go-app`.
    
- **Stage 2 (final):** Chúng ta bắt đầu lại với một image `alpine:latest` siêu nhẹ. Sau đó, chúng ta chỉ sao chép tệp nhị phân đã được biên dịch từ stage `builder` vào image cuối cùng này. Kết quả là một image production chỉ chứa ứng dụng của bạn và không có bất kỳ công cụ build nào.
    

3. Xây dựng và Chạy

Trước tiên, khởi tạo Go module:

Bash

```
go mod init go-webapp
```

Bây giờ, xây dựng image và chạy container:

Bash

```
# Build the Docker image
docker build -t go-webapp.

# Run the container, mapping port 8080 on the host to 8080 in the container
docker run -p 8080:8080 go-webapp
```

Mở trình duyệt và truy cập `http://localhost:8080` để thấy thông điệp của bạn.

### 4.2 Ví dụ 2: API Node.js & Express năng động

Node.js là một lựa chọn phổ biến cho các API. Quy trình làm việc với Docker cho Node.js tập trung vào việc quản lý các dependencies `npm` một cách hiệu quả.

1. Mã nguồn và Dependencies

Tạo một thư mục dự án và khởi tạo một dự án Node.js:

Bash

```
mkdir node-api && cd node-api
npm init -y
npm install express
```

Tạo một tệp `app.js`:

JavaScript

```
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Node.js & Express in a Docker Container!');
});

app.listen(port, () => {
  console.log(`Node.js API listening on port ${port}`);
});
```

2. Dockerfile

Tạo một tệp Dockerfile:

Dockerfile

```
# Use an official Node.js runtime as a parent image
FROM node:18-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
# This is done separately to take advantage of Docker's layer caching.
# The npm install step will only be re-run if these files change.
COPY package*.json./

# Install app dependencies
RUN npm install

# Bundle app source
COPY..

# Expose the port the app runs on
EXPOSE 3000

# Define the command to run the app
CMD [ "node", "app.js" ]
```

**Giải thích Dockerfile:**

- Chúng ta sao chép `package*.json` và chạy `npm install` trước khi sao chép phần còn lại của mã nguồn. Đây là một kỹ thuật tối ưu hóa quan trọng. Vì các dependencies ít thay đổi hơn mã nguồn, Docker có thể tái sử dụng lớp (layer) đã được cache của `npm install`, giúp các lần build sau nhanh hơn đáng kể.
    

**3. Xây dựng và Chạy**

Bash

```
# Build the Docker image
docker build -t node-api.

# Run the container, mapping port 3000 to 3000
docker run -p 3000:3000 node-api
```

Truy cập `http://localhost:3000` trên trình duyệt của bạn.

### 4.3 Ví dụ 3: Ứng dụng Python & FastAPI hướng dữ liệu

FastAPI là một framework Python hiện đại để xây dựng API. Tương tự như Node.js, việc quản lý dependencies là chìa khóa.

1. Mã nguồn và Dependencies

Tạo một thư mục dự án. Bên trong, tạo tệp requirements.txt:

```
fastapi
uvicorn[standard]
```

Tạo tệp `main.py`:

Python

```
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Python & FastAPI in a Docker Container!"}
```

2. Dockerfile

Tạo một tệp Dockerfile:

Dockerfile

```
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /code

# Copy the dependencies file to the working directory
COPY requirements.txt.

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY..

# Expose port 8000
EXPOSE 8000

# Run uvicorn server when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Giải thích Dockerfile:**

- Quy trình này tương tự như ví dụ Node.js. Chúng ta cài đặt các dependencies từ `requirements.txt` trước, sau đó sao chép mã nguồn để tận dụng cơ chế cache của Docker.
    
- Chúng ta sử dụng `python:3.11-slim` làm image cơ sở, đây là một biến thể nhỏ gọn hơn so với image mặc định, giúp giảm kích thước image cuối cùng.
    

**3. Xây dựng và Chạy**

Bash

```
# Build the Docker image
docker build -t python-api.

# Run the container, mapping port 8000 to 8000
docker run -p 8000:8000 python-api
```

Truy cập `http://localhost:8000` để xem kết quả.


Phần 6: [Docker Fullstack Example](https://blog.nagih.io.vn/post/docker/docker-fullstack-example/)

Phần 7: [Docker Best Practice for Production](https://blog.nagih.io.vn/post/docker/docker-best-practice-for-production/)

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*