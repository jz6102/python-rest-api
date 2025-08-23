# FastAPI Task Management REST API

A production-style **Task Management REST API** built with **FastAPI**.  
This project demonstrates clean coding practices, test-driven development, CI/CD workflows, and containerized deployment.  

---

## 🚀 Features
- **CRUD Operations**: Create, Read, Update, Delete tasks.
- **Authentication**: JWT-based user authentication.
- **Database**: PostgreSQL for data persistence.
- **Testing**: Unit tests using `pytest`.
- **Linting**: Code quality checks with `flake8`.
- **CI/CD**: GitHub Actions pipeline for automated testing & linting.
- **Containerization**: Dockerized for consistent deployment.
- **Deployment**: Hosted on [Render](https://render.com).

---

## 🛠️ Tech Stack
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Auth**: JWT (JSON Web Tokens)
- **Testing**: pytest
- **Linting**: flake8
- **CI/CD**: GitHub Actions
- **Deployment**: Render with Docker

---

## 📂 Project Structure
```bash
python-rest-api/
│── app/
│   ├── main.py          # Entry point of the API
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── routes/          # API routes
│   ├── database.py      # Database connection
│   └── auth.py          # JWT authentication
│
│── tests/               # Unit tests
│── requirements.txt     # Project dependencies
│── Dockerfile           # Containerization
│── .github/workflows/   # CI/CD workflows
│── .gitignore
│── README.md
