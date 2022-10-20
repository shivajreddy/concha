"""
Driver for PSQL using SQLAlchemy
Session creator for every request
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from server.config import settings

DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to create a new session, close after using
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
