from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base  # New

Base = declarative_base()

engine = create_engine('sqlite:///taskmanager.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

