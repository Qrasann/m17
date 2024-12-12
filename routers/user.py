from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated

from models import *
from sqlalchemy import insert
from schemas import CreateUser

from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update

from models import User

router = APIRouter(prefix='/users', tags=['users'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User).where(User.is_active == True)).all()
    if users is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users'
        )
    return users

@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   rating=0.0,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.get('/{task_slug}')
async def user_by_task(db: Annotated[Session, Depends(get_db)], task_slug: str):
    task = db.scalar(select(Task).where(Task.slug == task_slug))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    subtasks = db.scalars(select(Task).where(Task.parent_id == task.id)).all()
    tasks_and_subtasks = [task.id] + [i.id for i in subtasks]
    users_task = db.scalars(
        select(User).where(User.task_id.in_(tasks_and_subtasks), User.is_active == True)).all()
    return users_task

@router.get('/detail/{user_slug}')
async def user_detail(db: Annotated[Session, Depends(get_db)], user_slug: str):
    user = db.scalar(
        select(User).where(User.slug == user_slug, User.is_active == True))
    if not user:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no users'
        )
    return user

@router.put('/detail/{user_slug}')
async def update_user(db: Annotated[Session, Depends(get_db)], user_slug: str,
                      update_user_model: CreateUser):
    user_update = db.scalar(select(User).where(User.slug == user_slug))
    if user_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )

    db.execute(update(User).where(User.slug == user_slug)
               .values(username=update_user_model.username,
                       firstname=update_user_model.firstname,
                       lastname=update_user_model.lastname,
                       age=update_user_model.age,
                       slug=slugify(update_user_model.username)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }

@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user_delete = db.scalar(select(User).where(User.id == user_id))
    if user_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )
    db.execute(update(User).where(User.id == user_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User delete is successful'
    }
