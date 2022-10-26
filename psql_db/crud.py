"""
This module contains all the CRUD utils
"""
from sqlalchemy.orm import Session
from psql_db.models import User, AudioDataFile
from psql_db.schemas import UserNewSchema, UserRegisterInDB

from pydantic import EmailStr


# ---------- USER model's services ----------

# ---------- SELECT operations
def get_users(db: Session):
    users = db.query(User).all()
    return users


def get_user(db: Session, user_id: str = None, user_email: EmailStr = None):
    user = None
    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    elif user_email:
        user = db.query(User).filter(User.email == user_email).first()
    return user


def get_by_email(db: Session, user_email: str):
    user = db.query(User).filter(User.email.like(f'%{user_email}%')).all()

    return user


# ---------- INSERT operations
def create_new_user(user_data: UserRegisterInDB, db: Session):
    new_user = User(**user_data.dict())
    print("here in crud.py create_new_user func. I got new_user", new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------- AudioData model's services ----------

# ---------- SELECT operations
def get_audio_files(db: Session):
    audio_files = db.query(AudioDataFile).all()
    return audio_files
