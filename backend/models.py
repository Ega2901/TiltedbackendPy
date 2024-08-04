from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String(255), index=True)
    avatar = Column(String(255), nullable=True)
    points = Column(Integer, default=0)
    referrals = relationship("Referral", back_populates="user")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(255), index=True)
    task_description = Column(String(255))
    task_image = Column(String(255), nullable=True)
    task_url = Column(String(255), nullable=True)
    task_points = Column(Integer, default=0)
    completed_by = relationship("UserTask", back_populates="task")


class UserTask(Base):
    __tablename__ = "user_tasks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    completed = Column(Boolean, default=False)


class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    referral_code = Column(String(255), unique=True)
    user = relationship("User", back_populates="referrals")
