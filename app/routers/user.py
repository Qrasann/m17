from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from models import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify
from typing import Annotated

router = APIRouter()


# Функция для получения всех пользователей
@router.get('/')
def all_users(db: Annotated[Session, Depends(get_db)]):
  users = db.scalars(select(User)).all()
  return users


# Функция для получения пользователя по его ID
@router.get('/{user_id}')
def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
  user = db.scalars(select(User).where(User.id == user_id)).first()
  if user:
    return user
  else:
    raise HTTPException(status_code=404, detail="User was not found")


# Функция для создания пользователя
@router.post('/create')
def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
  # Проверка на уникальность username или user_id (по вашему выбору)
  existing_user = db.scalars(select(User).where(User.username == user.username)).first()
  if existing_user:
    raise HTTPException(status_code=400, detail="Username already exists")

  new_user = User(username=user.username, firstname=user.firstname, lastname=user.lastname, age=user.age)
  new_user.slug = slugify(new_user.firstname + " " + new_user.lastname)  # Создание slug-строки
  db.add(new_user)
  db.commit()
  return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


# Функция для обновления пользователя
@router.put('/update/{user_id}')
def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
  existing_user = db.scalars(select(User).where(User.id == user_id)).first()
  if existing_user:
    existing_user.firstname = user.firstname
    existing_user.lastname = user.lastname
    existing_user.age = user.age
    existing_user.slug = slugify(user.firstname + " " + user.lastname)  # Обновление slug-строки
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
  else:
    raise HTTPException(status_code=404, detail="User was not found")


# Функция для удаления пользователя
@router.delete('/delete/{user_id}')
def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
  existing_user = db.scalars(select(User).where(User.id == user_id)).first()
  if existing_user:
    db.delete(existing_user)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User has been deleted!"}
  else:
    raise HTTPException(status_code=404, detail="User was not found")
