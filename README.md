# ToDoApp

_A comprehensive planner application_

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/RaufMasoumi/ToDoApp?style=flat&logo=python&logoColor=orange&label=Python&labelColor=gray&color=orange)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/RaufMasoumi/ToDoApp/django?logo=Django&logoColor=white&label=Django&labelColor=gray&color=orange)
![GitHub Pipenv locked dependency version](https://img.shields.io/github/pipenv/locked/dependency-version/RaufMasoumi/ToDoApp/djangorestframework?style=flat&logo=DRF&logoColor=white&label=DjangoRestFramework&labelColor=gray&color=orange)
![GitHub last commit](https://img.shields.io/github/last-commit/RaufMasoumi/ToDoApp?color=blue&logo=github)


## 📑 Table of Contents
- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Project](#-running-the-project)
- [Docker Setup](#-docker-setup)
- [Testing](#-testing)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📖 About
ToDoApp is a comprehensive planning application that helps you organize your tasks and achieve your goals.It provides all the required endpoints through RESTful API. The project also includes a complete template-based frontend, making it possible to use independently.

The project is based on Django and Django REST Framework, and its main inspiration comes from the [Microsoft ToDo](https://to-do.office.com/) application.

---

## 🚀 Features
- Robust, thorough, and well-documented RESTful API endpoints
- Filtering, Ordering, and Searching tasks and task lists
- Complete template-based frontend 
- Secure authentication and permission system
- Comprehensive unit testing
- Well-designed database
- Dockerized and ready for production
- Neat mixin-based architecture using OOP 
- Clean and maintainable code  

---

## 🛠 Tech Stack
- Language: Python 3.10
- Framework: Django, Django REST Framework  
- Database: PostgreSQL / SQLite
- Deployment: Docker, Docker Compose, Gunicorn  

---

## 📂 Project Structure
````
ToDoApp/
├── accounts/
├── categories/
├── config/
├── tasklists/
│   ├── __init__.py
│   ├── migrations/
│   ├── admin.py
│   ├── api_tests.py
│   ├── api_urls.py
│   ├── api_views.py
│   ├── apps.py
│   ├── filters.py
│   ├── forms.py
│   ├── middlewares.py
│   ├── mixins.py
│   ├── models.py
│   ├── nested_serializers.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── validators.py
│   └── views.py
├── tasks/
├── templates/
│   ├── _base.html
│   ├── accounts/
│   ├── categories/
│   ├── snippets/
│   ├── tasklists/
│   └── tasks/
├── static/
├── staticfiles/
├── .gitignore
├── .idea/
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.dev
├── LICENSE.txt
├── manage.py
├── Pipfile
└── Pipfile.lock
````

---

## 📌 Prerequisites
Make sure you have the following installed:
- Python **3.10+**  
- Docker & Docker Compose (for containerized setup)  

---

## ⚡️ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/RaufMasoumi/ToDoApp.git
cd ToDoApp
```

### 2️⃣ Create and activate virtual environment
```bash
python -m pip install pipenv
pipenv shell
```

### 3️⃣ Install dependencies
```bash
pipenv install
```

### 4️⃣ Run migrations
Before running migrations, make sure you’ve set up the [Configuration](#-configuration)
```bash
python manage.py migrate
```

### 5️⃣ Create superuser
```bash
python manage.py createsuperuser
```

---

## 🔑 Configuration
First, create a Django secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Then add environment variables to a `.env` file:
```
DJANGO_SECRET_KEY="your-django-secret-key"
```

---

## ▶️ Running the Project
```bash
python manage.py runserver
```

---

## 🐳 Docker Setup
```bash
docker compose -f docker-compose-prod.yml up
```

---

## ✅ Testing
```bash
python manage.py test --pattern="*tests.py"
```

---

## 📌 API Documentation
- Schema file → `/api/schema/`  
- Swagger UI → `/api/schema/swagger-ui/`  
- Redoc → `/api/schema/redoc/`


---

## 🤝 Contributing
1. Fork the repo  
2. Create a branch (`git checkout -b feature/your-feature`)  
3. Commit changes (`git commit -m "Add feature"`)  
4. Push (`git push origin feature/your-feature`)  
5. Open a Pull Request  

---

## 📜 License
Distributed under the **MIT License**. See the [```LICENSE file```](./LICENSE) for more information.

Developed with ❤️ by Rauf Masoumi  
