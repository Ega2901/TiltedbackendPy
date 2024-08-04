from pydantic import BaseModel
from typing import List


class UserCreate(BaseModel):
    telegram_id: int
    username: str
    referral_code: str = None


class UserOut(BaseModel):
    telegram_id: int
    username: str
    points: int
    avatar: str = None

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    task_name: str
    task_description: str
    task_image: str = None
    task_url: str = None
    task_points: int


class TaskOut(BaseModel):
    id: int
    task_name: str
    task_description: str
    task_image: str
    task_url: str
    task_points: int

    class Config:
        orm_mode = True


class TaskComplete(BaseModel):
    user_id: int
