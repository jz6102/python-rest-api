import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import engine, Base, get_db

# create tables (simple approach; in real projects use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task API")

@app.post("/auth/register", response_model=schemas.UserRead)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    return user

@app.post("/auth/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # form_data.username should be email
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = auth.create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tasks/", response_model=schemas.TaskRead)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return crud.create_task(db, task_in, user_id=current_user.id)

@app.get("/tasks/", response_model=list[schemas.TaskRead])
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    return crud.get_tasks(db, current_user.id, skip=skip, limit=limit)

@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, updates)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)):
    task = crud.get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return None
