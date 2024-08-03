from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: str
    tg_username: str
    nickname: str
    referral_code: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    telegram_id: str
    tg_username: str
    nickname: str
    points: float
    referral_code: str
    avatar_url: Optional[str] = None  # Поле для URL аватара

    class Config:
        orm_mode = True

class TaskResponse(BaseModel):
    id: int
    user_id: int
    task_name: str
    task_description: str
    task_image: str
    task_url: str  # Поле для URL задачи
    completed: bool

    class Config:
        orm_mode = True
