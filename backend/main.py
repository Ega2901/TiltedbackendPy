# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, dependencies
from database import engine
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register/", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_telegram_id(db, user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db, user)

@app.get("/users/by_telegram_id/{telegram_id}/", response_model=schemas.UserOut)
def get_user(telegram_id: str, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.patch("/users/{telegram_id}/start_farming/")
def start_farming(telegram_id: str, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.is_farming = True
    db.commit()
    return {"status": "farming started"}

@app.patch("/users/{telegram_id}/claim_rewards/")
def claim_rewards(telegram_id: str, db: Session = Depends(dependencies.get_db)):
    db_user = crud.get_user_by_telegram_id(db, telegram_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.points += 1000.00
    db.commit()
    return {"status": "points claimed", "points": db_user.points}

@app.get("/tasks/user_tasks", response_model=List[schemas.TaskOut])
def get_user_tasks(user_id: int, db: Session = Depends(dependencies.get_db)):
    tasks = crud.get_tasks_by_user_id(db, user_id)
    return tasks

@app.post("/tasks/{task_id}/complete/")
def complete_task(task_id: int, user_id: int, db: Session = Depends(dependencies.get_db)):
    task = crud.get_task_by_id(db, task_id)
    if task is None or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found or not assigned to user")

    task.completed = True
    db.commit()
    return {"status": "task claimed"}
