from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    tg_username = Column(String, index=True)
    nickname = Column(String, index=True)
    points = Column(Float, default=0.0)
    referral_code = Column(String, unique=True, index=True)
    avatar_url = Column(String, nullable=True)  # Поле для URL аватара

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    task_name = Column(String)
    task_description = Column(String)
    task_image = Column(String)
    task_url = Column(String)  # Поле для URL задачи
    completed = Column(Boolean, default=False)
