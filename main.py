from routers import task, user
from fastapi import FastAPI
from backend.db import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)
@app.get("/")
async def welcome() -> dict:
    return {"message": "Taskmanager"}


app.include_router(task.router)
app.include_router(user.router)