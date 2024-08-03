# crud.py
from sqlalchemy.orm import Session
import models, schemas

def get_user_by_telegram_id(db: Session, telegram_id: str):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks_by_user_id(db: Session, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()
