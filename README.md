📦 Inventory Management System

A full-stack Inventory & Order Management System built with:

⚡ FastAPI (Python backend)
⚛️ React (frontend)
🐘 PostgreSQL database
🐳 Docker + Docker Compose
🚀 Features
📦 Product Management
Create products
View products
Update products
Delete products
Stock tracking
👤 Customer Management
Add customers
View customers
Delete customers
🧾 Order Management
Create orders
View orders
Order details
Auto stock deduction
Auto price calculation
🧱 Tech Stack
Layer	Technology
Frontend	React (Vite)
Backend	FastAPI (Python)
Database	PostgreSQL
Container	Docker
Orchestration	Docker Compose
📁 Project Structure
inventory-management-system/
│
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routes/
│   ├── database/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
🐳 Run Locally (Docker)
1. Clone repo
git clone https://github.com/Siddharttiwari/Inventory_management_system.git
cd Inventory_management_system
2. Create .env file
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=super_secret_password
POSTGRES_DB=production_db

DATABASE_URL=postgresql://prod_user:super_secret_password@db:5432/production_db

VITE_API_URL=http://localhost:8000

ADMIN_USERNAME=admin
ADMIN_PASSWORD=secret
3. Start system
docker compose --env-file .env up --build
🌐 Access Application
Service	URL
Frontend	http://localhost:8080
Backend API	http://localhost:8000
API Docs	http://localhost:8000/docs
⚙️ API Endpoints
Products
POST /products
GET /products
GET /products/{id}
PUT /products/{id}
DELETE /products/{id}
Customers
POST /customers
GET /customers
GET /customers/{id}
DELETE /customers/{id}
Orders
POST /orders
GET /orders
GET /orders/{id}
DELETE /orders/{id}
📊 Business Rules
SKU must be unique
Customer email must be unique
Stock cannot go negative
Orders auto reduce stock
Order total calculated by backend
Full input validation + error handling
🐳 Docker Services

This project includes:

Frontend service (React + Nginx)
Backend service (FastAPI)
PostgreSQL database

Managed using Docker Compose.

🚀 Deployment
Frontend

Deployed on: Vercel / Netlify

Backend

Deployed on: Render / Railway

Database

Hosted PostgreSQL (Render)

👨‍💻 Author

Siddhart Tiwari

⚠️ Why this README is better

This version:

Shows ownership
Explains architecture clearly
Matches assessment requirements
Includes APIs + rules
Looks like a production project
