from sqlalchemy.orm import Session
from models import User, Task, UserTask, Referral
from schemas import UserCreate, TaskCreate

def get_user_by_telegram_id(db: Session, telegram_id: int):
    return db.query(User).filter(User.telegram_id == telegram_id).first()

def create_user(db: Session, user: UserCreate, avatar_path: str = None):
    db_user = User(
        telegram_id=user.telegram_id,
        username=user.username,
        avatar=avatar_path,
        points=0
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_tasks(db: Session, user_id: int):
    return db.query(Task).join(UserTask).filter(UserTask.user_id == user_id, UserTask.completed == False).all()

def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        task_name=task.task_name,
        task_description=task.task_description,
        task_image=task.task_image,
        task_url=task.task_url,
        task_points=task.task_points
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def complete_task(db: Session, task_id: int, user_id: int):
    user_task = db.query(UserTask).filter(UserTask.task_id == task_id, UserTask.user_id == user_id).first()
    if user_task:
        user_task.completed = True
        db.commit()
    return {"status": "task claimed"}
