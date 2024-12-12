from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from sqlalchemy import insert
from schemas import CreateTask
from slugify import slugify

from models import Task

router = APIRouter(prefix='/task', tags=['task'])

@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    db.execute(insert(Task).values(name=create_task.name,
                                       parent_id=create_task.parent_id,
                                       slug=slugify(create_task.name)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }
#---------------------------------
from sqlalchemy import select


@router.get('/all_tasks')
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task).where(Task.is_active == True)).all()
    return tasks
#-----------------------------
@router.put('/update_task')
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: CreateTask):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )

    db.execute(update(Task).where(Task.id == task_id).values(
            name=update_task.name,
            slug=slugify(update_task.name),
            parent_id=update_task.parent_id))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }
#-----------------------------------------------
from sqlalchemy import update


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )
    db.execute(update(Task).where(Task.id == task_id).values(is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }