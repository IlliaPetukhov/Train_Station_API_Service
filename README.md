# 🚉 Train Station API Service

**Train Station API Service** is a RESTful backend built with **Django** and **Django REST Framework**.  
It provides endpoints for managing trains, passengers, and ticket bookings with JWT-based authentication and interactive API documentation.

---

## 🔧 Features

- 🔐 JWT authentication (Simple JWT)
- 👤 User registration and login
- 🧍 Full CRUD for passengers
- 🚆 Full CRUD for trains
- 🎫 Ticket booking and cancellation
- 📄 Interactive API documentation (Swagger / ReDoc)
- 🛠️ Modular project structure

---

## 🛠 Tech Stack

- **Python 3.x**
- **Django**, **Django REST Framework**
- **Simple JWT**
- **drf-yasg** (Swagger)
- **ReDoc**
- **SQLite / PostgreSQL**
- **Git**, **GitHub**
- **virtualenv**, **.env**

---

## ⚙️ Installation & Setup


# 1. Clone the repository
git clone https://github.com/IlliaPetukhov/Train_Station_API_Service.git
cd Train_Station_API_Service

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # For Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Start the development server
python manage.py runserver

## 🔑 Authentication Endpoints

| Method | Endpoint              | Description                   |
|--------|-----------------------|-------------------------------|
| POST   | `/api/token/`         | Get JWT access/refresh tokens |
| POST   | `/api/token/refresh/` | Refresh access token          |

---

## 📘 API Documentation

Once the server is running, access the auto-generated docs at:

- [http://localhost:8000/swagger/](http://localhost:8000/swagger/) — Swagger UI  
- [http://localhost:8000/redoc/](http://localhost:8000/redoc/) — ReDoc

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>
  
```
train_station_api_service/
├── authentication/ # JWT and user registration logic
├── passengers/ # Passenger CRUD API
├── tickets/ # Ticket booking logic
├── trains/ # Train CRUD API
├── core/ # Settings and base config
├── manage.py
├── requirements.txt
```
</details>

## Author Illia Petukhov
