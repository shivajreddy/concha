"""
This module contains all the CRUD utils
"""
from sqlalchemy.orm import Session
from psql_db.models import User, AudioDataFile
from psql_db.schemas import UserRegisterInDB, AudioDataFileSchema

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


# Look up all similar entries of given email string
def get_users_by_email(db: Session, email_query: str):
    users = db.query(User).filter(User.email.like(f'%{email_query}%')).all()
    return users


# Look up all similar entries of given name string
def get_users_by_name(db: Session, name_query: str):
    users = db.query(User).filter(User.name.like(f'%{name_query}%')).all()
    return users


# ---------- INSERT operations
def create_new_user(db: Session, user_data: UserRegisterInDB):
    new_user = User(**user_data.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------- AudioData model's services ----------

# ---------- SELECT operations
def get_all_audio_data(db: Session):
    all_audio_data = db.query(AudioDataFile).all()
    return all_audio_data


def audio_data_of_session_id(db: Session, session_id: int):
    return db.query(AudioDataFile).filter(AudioDataFile.session_id == session_id).all()


def add_audio_data(db: Session, audio_data: AudioDataFileSchema):
    new_audio_data = AudioDataFile(**audio_data.dict())
    new_audio_data.unique_id = str(new_audio_data.session_id) + "-" + str(new_audio_data.step_count)
    db.add(new_audio_data)
    db.commit()
    db.refresh(new_audio_data)
    return new_audio_data
