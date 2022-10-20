"""
Driver for PSQL using SQLAlchemy
Session creator for every request
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:2106@localhost/fastapi_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency to create a new session, close after using
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
