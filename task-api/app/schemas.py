from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class Login(BaseModel):
    username: str
    password: str

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: int
    owner_id: int
    class Config:
        orm_mode = True
