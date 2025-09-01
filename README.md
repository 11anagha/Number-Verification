# 🚀 Armstrong Number Checker -- Django + DRF + JWT

This project is a **Django + Django REST Framework** application that
allows users to:

-   Register & Login with JWT Authentication\
-   Verify if a number is an **Armstrong Number**\
-   Save verified Armstrong numbers under their profile\
-   Retrieve personal saved numbers\
-   View all Armstrong numbers saved globally by all users

------------------------------------------------------------------------

## 🛠️ Setup & Installation

### 1. Clone the Repository

``` bash
git clone https://github.com/11anagha/Number-Verification.git
cd Number-Verification
```

### 2. Create Virtual Environment

``` bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure Database

By default, **SQLite** is used. To switch to **MYSQL**

``` python
# Create a .env file and add the following environment variables
DB_USER=YOUR_DB_USER
DB_NAME=YOUR_DB_NAME
DB_HOST=YOUR_DB_HOST
DB_PASS=YOU_DB_PASS
```

Run migrations:

``` bash
python manage.py migrate
```

### 5. Run the Development Server

``` bash
python manage.py runserver
```

The app will be available at:\
👉 `http://127.0.0.1:8000/`

------------------------------------------------------------------------

## 🗄️ Database Schema Design

### Models

1.  **CustomUser**
    -   Extends Django's AbstractUser or AbstractBaseUser.
    -   Fields: `id`, `email`, `password`, `is_active`, `date_joined`,
        etc.
2.  **ArmstrongNumber**
    -   Stores Armstrong numbers verified by users.\
    -   Fields:
        -   `id`: Primary key\
        -   `user`: ForeignKey → `CustomUser`\
        -   `number`: Integer (unique per user)\
        -   `created_at`: Timestamp

### Relationships

-   **One-to-Many**: Each `CustomUser` can have multiple saved
    `ArmstrongNumber` records.

------------------------------------------------------------------------

## 🌐 API Endpoints

  -------------------------------------------------------------------------
  Endpoint                           Method   Auth Required   Description
  ---------------------------------- -------- --------------- -------------
  `/api/register/`                   POST     ❌ No           Register a
                                                              new user

  `/api/login/`                      POST     ❌ No           Login and get
                                                              JWT tokens

  `/api/verify-number/`              POST     ✅ Yes          Verify if a
                                                              number is
                                                              Armstrong.
                                                              Optionally
                                                              save it

  `/api/verify-number/`              GET      ✅ Yes          Get user's
                                                              saved
                                                              Armstrong
                                                              numbers

  `/api/global-armstrong-numbers/`   GET      ❌ No           Get all users
                                                              with their
                                                              Armstrong
                                                              numbers
  -------------------------------------------------------------------------

### Example Requests

**Register**

``` http
POST /api/register/
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

**Login**

``` http
POST /api/login/
{
  "email": "user@example.com",
  "password": "StrongPass123!"
}
```

Response includes `access` and `refresh` JWT tokens.

**Verify Number**

``` http
POST /api/verify-number/
Authorization: Bearer <access_token>

{
  "number": 153,
  "save": true
}
```

**Get User's Numbers**

``` http
GET /api/verify-number/
Authorization: Bearer <access_token>
```

**Global Armstrong Numbers**

``` http
GET /api/global-armstrong-numbers/
```

------------------------------------------------------------------------

## ⚡ Performance Optimization Approaches

1.  **Efficient Armstrong Check**
    -   Armstrong check runs in O(d), where d = number of digits.\
    -   Implemented with `sum(int(d) ** power for d in digits)` to avoid
        redundant computations.
2.  **Database Query Optimization**
    -   Used `.values_list()` in `VerifyNumberAPIView.get()` to fetch
        only necessary fields.\
    -   Used `prefetch_related('armstrong_numbers')` in global view to
        avoid N+1 query problem.
3.  **JWT for Stateless Auth**
    -   Eliminates costly session lookups and scales well with
        distributed environments.
4.  **Error Handling & Timeouts**
    -   Requests to API endpoints include `timeout=5` to prevent hanging
        connections.

------------------------------------------------------------------------

## 🧩 Challenges & Solutions

### 1. **JWT Integration**

-   **Challenge**: Managing secure authentication between API and
    frontend views.\
-   **Solution**: Used `djangorestframework-simplejwt` for JWT handling.
    Tokens stored in Django session for frontend usage.

### 2. **Avoiding Duplicate Saves**

-   **Challenge**: Preventing duplicate Armstrong numbers for the same
    user.\
-   **Solution**: Applied `unique_together` constraint on
    `(user, number)` in `ArmstrongNumber`.

### 3. **API ↔ Form Handling**

-   **Challenge**: Bridging Django forms with DRF APIs.\
-   **Solution**: Used `requests` library inside normal views
    (`register_page`, `login_page`, `verify_number`) to call DRF
    endpoints, keeping separation of concerns.

### 4. **Global Data Retrieval**

-   **Challenge**: N+1 queries when fetching users with their Armstrong
    numbers.\
-   **Solution**: Used `prefetch_related` with serializer to minimize
    queries.

------------------------------------------------------------------------
