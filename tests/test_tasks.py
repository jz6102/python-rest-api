import os
import tempfile
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Use a temp sqlite file DB for tests
db_fd, db_path = tempfile.mkstemp(suffix=".db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_register_login_and_task_crud():
    # register
    r = client.post("/auth/register", json={"email": "test@example.com", "password": "strongpass"})
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "test@example.com"

    # login (OAuth2 form fields)
    r = client.post("/auth/login", json={"username": "test@example.com", "password": "strongpass"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # create task
    r = client.post("/tasks/", json={"title": "T1", "description": "desc"}, headers=headers)
    assert r.status_code == 200
    task = r.json()
    assert task["title"] == "T1"

    # list tasks
    r = client.get("/tasks/", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1

    # update task
    task_id = task["id"]
    r = client.put(f"/tasks/{task_id}", json={"completed": True}, headers=headers)
    assert r.status_code == 200
    assert r.json()["completed"] is True

    # delete
    r = client.delete(f"/tasks/{task_id}", headers=headers)
    assert r.status_code == 204
