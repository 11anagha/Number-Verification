# 🚀 Armstrong Number Checker (Django + DRF + JWT)

A **Django + Django REST Framework** application that allows users to:

- 🔐 Register & Login with **JWT Authentication**  
- 🔢 Verify if a number is an **Armstrong Number**  
- 💾 Save verified Armstrong numbers under their profile  
- 📂 Retrieve personal saved numbers  
- 🌍 View all Armstrong numbers saved globally by all users  

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/11anagha/Number-Verification.git
cd Number-Verification
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database

By default, the project uses **SQLite**.  
To switch to **MySQL**:

- Create a database in MySQL Workbench (e.g., `number_verification`).  
- Create a `.env` file in the project root with the following variables:

```env
DB_USER=YOUR_DB_USER
DB_NAME=YOUR_DB_NAME
DB_HOST=YOUR_DB_HOST
DB_PASS=YOUR_DB_PASS
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

The app will be available at 👉 **http://127.0.0.1:8000/**

---

## 📬 Postman Collection

You can test the APIs using **Postman**:  
🔗 [Postman Collection Link](https://elements.getpostman.com/redirect?entityId=48096872-89e6e07b-4650-4cea-87bd-a03a33ae071c&entityType=collection)

> ⚠️ Before hitting the APIs, make sure you activate **"Number Verification Env"** in Postman.

---

## 🌐 API Endpoints

| Endpoint                         | Method | Auth Required | Description                                   |
|----------------------------------|--------|---------------|-----------------------------------------------|
| `/api/register/`                 | POST   | ❌ No         | Register a new user                           |
| `/api/login/`                    | POST   | ❌ No         | Login and get JWT tokens                      |
| `/api/verify-number/`            | POST   | ✅ Yes        | Verify if a number is Armstrong. Optionally save it |
| `/api/get-numbers/`              | GET    | ✅ Yes        | Get user's saved Armstrong numbers            |
| `/api/global-armstrong-numbers/` | GET    | ❌ No         | Get all users with their Armstrong numbers    |

---

## 📖 Example Requests

### 🔹 Register
```http
POST /api/register/
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

### 🔹 Login
```http
POST /api/login/
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

**Response**
```json
{
  "access": "<access_token>",
  "refresh": "<refresh_token>"
}
```

### 🔹 Verify Number
```http
POST /api/verify-number/
Authorization: Bearer <access_token>

{
  "number": 153,
  "save": true
}
```

### 🔹 Get User's Numbers
```http
GET /api/get-numbers/
Authorization: Bearer <access_token>
```

### 🔹 Global Armstrong Numbers
```http
GET /api/global-armstrong-numbers/
```

---
