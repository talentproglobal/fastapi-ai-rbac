# FastAPI AI-RBAC Microservice

## Overview
This FastAPI microservice provides:
- **JWT Authentication** for secure login
- **Role-Based Access Control (RBAC)** using Oso
- **CRUD operations** for user management
- **AI-powered RAG Pipeline** for document processing
- **MongoDB Integration** for user data storage

## Features
✅ Secure **User Authentication & Authorization** (JWT-based)
✅ **Role-Based Access Control (RBAC)** for Admin/User permissions
✅ **Upload & Query Documents** using AI-powered RAG pipeline
✅ **MongoDB Database Integration** for user management
✅ **API Documentation via Swagger UI**

##  Installation Guide

### 🔹 1. Clone the Repository
```sh
git clone https://github.com/yourusername/fastapi-ai-rbac.git
cd fastapi-ai-rbac
```

### 🔹 2. Create a Virtual Environment
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 🔹 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 🔹 4. Start MongoDB
- **If MongoDB is installed locally:**
  ```sh
  mongod --dbpath=/data/db
  ```
- **Or use Docker:**
  ```sh
  docker run --name mongodb -d -p 27017:27017 mongo
  ```
- **Or use Docker-compose:**
  ```sh
  docker-compose up --build -d
  ```

### 🔹 5. Run FastAPI Application
```sh
uvicorn app.main:app --reload
```

### 🔹 6. Open Swagger UI for API Testing
**http://127.0.0.1:8000/docs**

## 🔗 API Endpoints

### 🔹 Authentication
| Method | Endpoint | Description |
|--------|----------|------------|
| `POST` | `/token` | User login & token generation |

### 🔹 User Management
| Method | Endpoint | Description |
|--------|----------|------------|
| `POST` | `/users/` | Create a new user |
| `GET` | `/users/{username}` | Retrieve user details |
| `DELETE` | `/users/{username}` | Delete a user (Admin only) |

### 🔹 AI Document Processing
| Method | Endpoint | Description |
|--------|----------|------------|
| `POST` | `/upload/` | Upload a document |
| `GET` | `/query?query=your_question` | Query AI model |

## Role-Based Access Control (RBAC)
| Role | Permissions |
|------|------------|
| **Admin** | Read, Write, Delete |
| **User** | Read, Write |

- **Only Admins** can delete users.
- Users **can only view/edit their own profile**.

## Deployment
### 🔹 Deploy with Docker
```sh
docker build -t fastapi-ai-rbac .
docker run -p 8000:8000 fastapi-ai-rbac
```

### 🔹 Deploy to AWS (Optional)
- Deploy via **EC2, ECS, or Lambda**.

## Running Tests
Run tests with **Pytest**:
```sh
pytest
```

## Running with pm2 
- pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4" --name fastapi-app


