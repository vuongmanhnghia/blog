---
title: Mẫu Documentation cho Backend
date: 2025-09-16
image:
categories:
  - docs
tags:
  - backend
draft: false
---

Chia sẻ mẫu Documentation cho lập trình viên Backend

<!--more-->

# E-Library Management System - Backend Documentation

## 📋 Table of Contents

[Backend Documentation](content/posts/docs/Backend%20Documentation.md)
[[Backend Documentation]]
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [API Documentation](#api-documentation)
4. [Database Schema](#database-schema)
5. [Authentication & Security](#authentication--security)
6. [Setup & Deployment](#setup--deployment)
7. [Testing](#testing)
8. [Monitoring & Logging](#monitoring--logging)

---

## 🎯 System Overview

**Project**: E-Library Management System  
**Version**: v2.1.0  
**Tech Stack**: Node.js, Express.js, MongoDB, Redis, Docker  
**Purpose**: Backend API cho hệ thống quản lý thư viện sách điện tử

### Core Features
- User authentication & authorization	
- Book catalog management
- Book borrowing/returning system
- Search & filtering
- User notifications
- Admin dashboard APIs

---

## 🏗️ Architecture
### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client Apps   │────│  Load Balancer  │────│   API Gateway   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                        ┌───────────────────────────────┼───────────────────────────────┐
                        │                               │                               │
                ┌───────▼───────┐              ┌───────▼───────┐              ┌───────▼───────┐
                │  Auth Service │              │  Book Service │              │ User Service  │
                └───────────────┘              └───────────────┘              └───────────────┘
                        │                               │                               │
                        └───────────────────────────────┼───────────────────────────────┘
                                                        │
                        ┌───────────────────────────────┼───────────────────────────────┐
                        │                               │                               │
                ┌───────▼───────┐              ┌───────▼───────┐              ┌───────▼───────┐
                │   MongoDB     │              │     Redis     │              │   File Store  │
                │   (Primary)   │              │   (Caching)   │              │   (Images)    │
                └───────────────┘              └───────────────┘              └───────────────┘
```

### Service Dependencies
- **Auth Service**: JWT token validation, user roles
- **Book Service**: Book CRUD operations, search, categorization
- **User Service**: User profile management, borrowing history
- **Notification Service**: Email/SMS notifications
- **File Service**: Book cover uploads, PDF handling

---

## 📡 API Documentation

### Base URL
```
Production: https://api.elibrary.com/v2
Staging: https://staging-api.elibrary.com/v2
Development: http://localhost:3000/v2
```

### Authentication
All protected endpoints require Bearer token:
```
Authorization: Bearer <jwt_token>
```

### Response Format
```json
{
  "success": true,
  "message": "Request processed successfully",
  "data": {},
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  },
  "timestamp": "2025-09-16T10:30:00.000Z"
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": [
      {
        "field": "email",
        "message": "Email format is invalid"
      }
    ]
  },
  "timestamp": "2025-09-16T10:30:00.000Z"
}
```

---

## 🔐 Authentication Endpoints
### POST /auth/register
**Description**: Đăng ký tài khoản mới

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "firstName": "John",
  "lastName": "Doe",
  "phoneNumber": "+84901234567"
}
```

**Response (201)**:
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "66e123456789abcdef123456",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user",
      "isVerified": false
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### POST /auth/login
**Description**: Đăng nhập hệ thống

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200)**:
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "66e123456789abcdef123456",
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "role": "user"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

## 📚 Book Management Endpoints

### GET /books
**Description**: Lấy danh sách sách với phân trang và filter

**Query Parameters**:
- `page` (integer, default: 1): Trang hiện tại
- `limit` (integer, default: 20): Số sách per page
- `category` (string): Filter theo danh mục
- `author` (string): Filter theo tác giả
- `search` (string): Tìm kiếm theo title/author
- `available` (boolean): Chỉ lấy sách còn available

**Example Request**:
```
GET /books?page=1&limit=10&category=fiction&available=true
```

**Response (200)**:
```json
{
  "success": true,
  "data": {
    "books": [
      {
        "id": "66e123456789abcdef123456",
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "978-0743273565",
        "category": "fiction",
        "publishYear": 1925,
        "description": "A classic American novel...",
        "coverImage": "https://cdn.elibrary.com/covers/great-gatsby.jpg",
        "totalCopies": 5,
        "availableCopies": 3,
        "rating": 4.5,
        "createdAt": "2025-09-01T10:00:00.000Z",
        "updatedAt": "2025-09-15T14:30:00.000Z"
      }
    ]
  },
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 156,
    "totalPages": 16
  }
}
```

### POST /books
**Description**: Thêm sách mới (Admin only)  
**Authentication**: Required (Admin role)

**Request Body**:
```json
{
  "title": "New Book Title",
  "author": "Author Name",
  "isbn": "978-1234567890",
  "category": "science",
  "publishYear": 2024,
  "description": "Book description here...",
  "totalCopies": 3,
  "coverImage": "base64_encoded_image_or_url"
}
```

**Response (201)**:
```json
{
  "success": true,
  "message": "Book created successfully",
  "data": {
    "book": {
      "id": "66e123456789abcdef123457",
      "title": "New Book Title",
      "author": "Author Name",
      "isbn": "978-1234567890",
      "category": "science",
      "publishYear": 2024,
      "description": "Book description here...",
      "totalCopies": 3,
      "availableCopies": 3,
      "rating": 0,
      "createdAt": "2025-09-16T10:30:00.000Z"
    }
  }
}
```

### PUT /books/:bookId
**Description**: Cập nhật thông tin sách (Admin only)  
**Authentication**: Required (Admin role)

### DELETE /books/:bookId
**Description**: Xóa sách (Admin only)  
**Authentication**: Required (Admin role)

---

## 📖 Borrowing System Endpoints

### POST /borrowings
**Description**: Mượn sách  
**Authentication**: Required

**Request Body**:
```json
{
  "bookId": "66e123456789abcdef123456",
  "borrowDuration": 14
}
```

**Response (201)**:
```json
{
  "success": true,
  "message": "Book borrowed successfully",
  "data": {
    "borrowing": {
      "id": "66e123456789abcdef123458",
      "userId": "66e123456789abcdef123456",
      "bookId": "66e123456789abcdef123456",
      "borrowDate": "2025-09-16T10:30:00.000Z",
      "dueDate": "2025-09-30T10:30:00.000Z",
      "status": "active",
      "renewalCount": 0
    }
  }
}
```

### PUT /borrowings/:borrowingId/return
**Description**: Trả sách  
**Authentication**: Required

**Response (200)**:
```json
{
  "success": true,
  "message": "Book returned successfully",
  "data": {
    "borrowing": {
      "id": "66e123456789abcdef123458",
      "returnDate": "2025-09-16T15:45:00.000Z",
      "status": "returned",
      "lateFee": 0
    }
  }
}
```

### GET /borrowings/my-books
**Description**: Lấy danh sách sách đang mượn của user  
**Authentication**: Required

---

## 🗄️ Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique, required),
  password: String (hashed, required),
  firstName: String (required),
  lastName: String (required),
  phoneNumber: String,
  role: String (enum: ['user', 'librarian', 'admin'], default: 'user'),
  isVerified: Boolean (default: false),
  avatar: String,
  address: {
    street: String,
    city: String,
    zipCode: String
  },
  preferences: {
    notifications: {
      email: Boolean (default: true),
      sms: Boolean (default: false)
    },
    favoriteCategories: [String]
  },
  createdAt: Date,
  updatedAt: Date
}
```

### Books Collection
```javascript
{
  _id: ObjectId,
  title: String (required, indexed),
  author: String (required, indexed),
  isbn: String (unique, required),
  category: String (required, indexed),
  publishYear: Number,
  publisher: String,
  language: String (default: 'vietnamese'),
  description: String,
  coverImage: String,
  pdfFile: String,
  totalCopies: Number (required, min: 1),
  availableCopies: Number (required),
  rating: Number (default: 0),
  reviewCount: Number (default: 0),
  tags: [String],
  createdAt: Date,
  updatedAt: Date,
  createdBy: ObjectId (ref: 'User')
}
```

### Borrowings Collection
```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref: 'User', required),
  bookId: ObjectId (ref: 'Book', required),
  borrowDate: Date (required),
  dueDate: Date (required),
  returnDate: Date,
  status: String (enum: ['active', 'returned', 'overdue'], required),
  renewalCount: Number (default: 0, max: 2),
  lateFee: Number (default: 0),
  notes: String,
  createdAt: Date,
  updatedAt: Date
}
```

### Categories Collection
```javascript
{
  _id: ObjectId,
  name: String (required, unique),
  slug: String (required, unique),
  description: String,
  parentCategory: ObjectId (ref: 'Category'),
  isActive: Boolean (default: true),
  sortOrder: Number (default: 0),
  createdAt: Date,
  updatedAt: Date
}
```

---

## 🔒 Authentication & Security

### JWT Configuration
```javascript
{
  secret: process.env.JWT_SECRET,
  algorithm: 'HS256',
  expiresIn: '24h',
  refreshTokenExpiresIn: '7d'
}
```

### Password Requirements
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter  
- At least 1 number
- At least 1 special character

### Rate Limiting
```javascript
{
  "/auth/login": "5 requests per 15 minutes per IP",
  "/auth/register": "3 requests per hour per IP", 
  "/books": "100 requests per 15 minutes per user",
  "/borrowings": "20 requests per hour per user"
}
```

### CORS Configuration
```javascript
{
  origin: [
    'https://elibrary.com',
    'https://admin.elibrary.com',
    'http://localhost:3000' // development only
  ],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}
```

---

## ⚙️ Setup & Deployment

### Environment Variables
```bash
# Database
MONGODB_URI=mongodb://localhost:27017/elibrary
REDIS_URL=redis://localhost:6379

# Authentication
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRES_IN=24h
REFRESH_TOKEN_SECRET=your-refresh-token-secret

# External Services
EMAIL_SERVICE_API_KEY=your-email-service-key
SMS_SERVICE_API_KEY=your-sms-service-key
CLOUDINARY_URL=cloudinary://your-cloudinary-url

# Server
PORT=3000
NODE_ENV=production
```

### Development Setup
```bash
# 1. Clone repository
git clone https://github.com/company/elibrary-backend.git
cd elibrary-backend

# 2. Install dependencies
npm install

# 3. Copy environment file
cp .env.example .env

# 4. Start MongoDB and Redis
docker-compose up -d mongo redis

# 5. Run database migrations
npm run migrate

# 6. Start development server
npm run dev
```

### Docker Deployment
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - MONGODB_URI=mongodb://mongo:27017/elibrary
      - REDIS_URL=redis://redis:6379
    depends_on:
      - mongo
      - redis
      
  mongo:
    image: mongo:6.0
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
      
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  mongo_data:
  redis_data:
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]
    
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test
      
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to server
        run: |
          ssh user@server "cd /app && git pull && docker-compose up -d --build"
```

---

## 🧪 Testing

### Test Structure
```
tests/
├── unit/
│   ├── controllers/
│   ├── services/
│   └── utils/
├── integration/
│   ├── auth.test.js
│   ├── books.test.js
│   └── borrowings.test.js
└── e2e/
    └── api.test.js
```

### Running Tests
```bash
# Unit tests
npm run test:unit

# Integration tests  
npm run test:integration

# E2E tests
npm run test:e2e

# All tests with coverage
npm run test:coverage
```

### Test Example
```javascript
// tests/integration/books.test.js
describe('Books API', () => {
  beforeEach(async () => {
    await Book.deleteMany({});
    await User.deleteMany({});
    
    // Create test user and admin
    testUser = await User.create({
      email: 'test@example.com',
      password: 'hashedpassword',
      firstName: 'Test',
      lastName: 'User'
    });
    
    userToken = jwt.sign({ userId: testUser._id }, process.env.JWT_SECRET);
  });

  describe('GET /books', () => {
    it('should return paginated books', async () => {
      // Create test books
      await Book.create([
        { title: 'Book 1', author: 'Author 1', isbn: '1111111111' },
        { title: 'Book 2', author: 'Author 2', isbn: '2222222222' }
      ]);

      const response = await request(app)
        .get('/v2/books?page=1&limit=10')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.books).toHaveLength(2);
      expect(response.body.pagination.total).toBe(2);
    });
  });
});
```

---

## 📊 Monitoring & Logging

### Logging Configuration
```javascript
// config/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});
```

### Metrics Collection
- **Response Time**: Average API response time
- **Request Rate**: Requests per second
- **Error Rate**: 4xx/5xx error percentage  
- **Database Connection**: MongoDB connection pool status
- **Memory Usage**: Node.js heap usage
- **Active Users**: Currently logged in users

### Health Check Endpoint
```javascript
// GET /health
{
  "status": "healthy",
  "timestamp": "2025-09-16T10:30:00.000Z",
  "services": {
    "database": "connected",
    "redis": "connected", 
    "external_apis": "operational"
  },
  "metrics": {
    "uptime": "72h 15m",
    "memory_usage": "245MB",
    "cpu_usage": "15%"
  }
}
```

### Alerting Rules
- Response time > 2000ms for 5 minutes
- Error rate > 5% for 3 minutes  
- Database connection lost
- Memory usage > 80%
- Disk space < 10%

---

## 📈 Error Codes Reference

| Code                  | HTTP Status | Description                       |
| --------------------- | ----------- | --------------------------------- |
| `VALIDATION_ERROR`    | 400         | Request validation failed         |
| `UNAUTHORIZED`        | 401         | Invalid or missing authentication |
| `FORBIDDEN`           | 403         | Insufficient permissions          |
| `NOT_FOUND`           | 404         | Resource not found                |
| `CONFLICT`            | 409         | Resource already exists           |
| `RATE_LIMIT_EXCEEDED` | 429         | Too many requests                 |
| `INTERNAL_ERROR`      | 500         | Server error                      |
| `SERVICE_UNAVAILABLE` | 503         | External service unavailable      |

## 🔄 Changelog

### v2.1.0 (2025-09-16)
**Added**
- Book rating and review system
- Advanced search with filters
- PDF file upload for digital books
- Notification system for due dates

**Changed** 
- Improved authentication with refresh tokens
- Enhanced error handling and logging
- Updated database schema for better performance

**Fixed**
- Memory leaks in file upload
- Race condition in book borrowing
- Timezone issues in due date calculations

### v2.0.0 (2025-08-01)
**Added**
- Complete API redesign
- Role-based access control
- Redis caching layer
- Docker containerization

---

## 📞 Support & Contact

**Development Team**: backend-team@company.com  
**DevOps Team**: devops@company.com  
**Documentation**: https://docs.elibrary.com  
**Issue Tracker**: https://github.com/company/elibrary-backend/issues

---

*Last updated: September 16, 2025*