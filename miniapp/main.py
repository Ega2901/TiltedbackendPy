from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Task
from app.schemas import UserCreate, UserResponse, TaskResponse
from pathlib import Path
import shutil
from typing import List, Optional

app = FastAPI()

# CORS настройка
origins = ["http://localhost:3000", "https://tiltedxyz.ru"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание базы данных
Base.metadata.create_all(bind=engine)


# Зависимость для получения базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Путь для сохранения аватаров
AVATAR_PATH = Path("avatars/")
AVATAR_PATH.mkdir(exist_ok=True)


@app.post("/register/", response_model=UserResponse)
def register_user(
        nickname: str,
        telegram_id: str,
        tg_username: str,
        referral_code: Optional[str] = None,
        avatar: Optional[UploadFile] = None,
        db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    avatar_url = None
    if avatar:
        avatar_filename = f"{telegram_id}_{avatar.filename}"
        avatar_path = AVATAR_PATH / avatar_filename
        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
        avatar_url = f"/avatars/{avatar_filename}"

    new_user = User(
        telegram_id=telegram_id,
        tg_username=tg_username,
        nickname=nickname,
        referral_code=referral_code,
        avatar_url=avatar_url,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/by_telegram_id/{telegram_id}/", response_model=UserResponse)
def get_user_by_telegram_id(telegram_id: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.patch("/users/{user_id}/start_farming/")
def start_farming(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Логика старта фарминга
    return {"status": "farming started"}


@app.patch("/users/{user_id}/claim_rewards/")
def claim_rewards(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    # Логика получения наград
    return {"status": "points claimed", "points": db_user.points}


@app.get("/tasks/user_tasks", response_model=List[TaskResponse])
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    return tasks


@app.post("/tasks/{task_id}/complete/")
def complete_task(task_id: int, user_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.completed = True
    db.commit()
    return {"status": "task claimed"}
