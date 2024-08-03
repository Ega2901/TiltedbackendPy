# models.py
from sqlalchemy import Column, Integer, String, DECIMAL, BLOB, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String(255), unique=True, index=True, nullable=False)
    tg_username = Column(String(255))
    nickname = Column(String(255))
    points = Column(DECIMAL(10, 2), default=0.00)
    referral_code = Column(String(255))
    avatar = Column(BLOB)
    is_farming = Column(Boolean, default=False)
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    task_name = Column(String(255))
    task_description = Column(String(255))
    task_image = Column(String(255))
    completed = Column(Boolean, default=False)
    user = relationship("User", back_populates="tasks")


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
