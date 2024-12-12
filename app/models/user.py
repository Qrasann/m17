# user.py
from app.backend.db import Base
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    is_active = Column(Boolean, default=True)

    tasks = relationship("Task", back_populates="user")


from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))

