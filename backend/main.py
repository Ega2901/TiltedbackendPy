from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import shutil
from fastapi.middleware.cors import CORSMiddleware

from models import Base, User, Task
from schemas import UserCreate, UserOut, TaskOut, TaskCreate, TaskComplete
from database import engine, get_db
import crud

app = FastAPI()

# Создание всех таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Разрешение CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["tiltedxyz.ru", "www.tiltedxyz.ru"],  # Измените на конкретные домены в продакшене
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/users/by_telegram_id/{telegram_id}/", response_model=UserOut)
def get_user_by_telegram_id(telegram_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/register/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db), avatar: UploadFile = None):
    db_user = crud.get_user_by_telegram_id(db, user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    avatar_path = None
    if avatar:
        avatar_path = f"avatars/{user.telegram_id}_{avatar.filename}"
        with open(avatar_path, "wb") as buffer:
            shutil.copyfileobj(avatar.file, buffer)
    new_user = crud.create_user(db=db, user=user, avatar_path=avatar_path)
    return new_user

@app.patch("/users/{telegram_id}/start_farming/")
def start_farming(telegram_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Логика для запуска фермерства
    return {"message": "Farming started"}

@app.patch("/users/{telegram_id}/claim_rewards/")
def claim_rewards(telegram_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Логика для получения наград
    return {"message": "Rewards claimed"}

@app.get("/tasks/user_tasks", response_model=List[TaskOut])
def get_user_tasks(user_id: int, db: Session = Depends(get_db)):
    tasks = crud.get_user_tasks(db, user_id)
    return tasks

@app.post("/tasks/", response_model=TaskOut)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db=db, task=task)

@app.post("/tasks/{task_id}/complete/")
def complete_task(task_id: int, task_complete: TaskComplete, db: Session = Depends(get_db)):
    return crud.complete_task(db=db, task_id=task_id, user_id=task_complete.user_id)
