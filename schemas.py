from pydantic import BaseModel
from pydantic import BaseModel

class CreateUser(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    age: int



class CreateTask(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
