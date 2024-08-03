# schemas.py
from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    telegram_id: str
    tg_username: Optional[str] = None
    nickname: Optional[str] = None
    points: Optional[float] = 0.00

class UserCreate(UserBase):
    referral_code: Optional[str] = None
    avatar: Optional[bytes] = None

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    task_name: str
    task_description: str
    task_image: str
    completed: bool

class TaskOut(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
