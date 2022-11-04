"""
This module contains all the CRUD utils also known as DOA layer
"""
from sqlalchemy.orm import Session

from psql_db.models import User, AudioData
from psql_db.schemas import UserDbSchema, AudioDataDbSchema

from pydantic import EmailStr


# ---------- USER model's services ----------

# ---------- SELECT operations
# Get all users in the users_data table
def get_users(db: Session):
    users = db.query(User).all()

    return users


# Get user with email or id
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
def create_new_user(db: Session, user_data: UserDbSchema):
    new_user = User(**user_data.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# ---------- UPDATE operations
def update_user(db: Session, user_data: UserDbSchema):
    user_query = db.query(User).filter(User.id == user_data.id)
    user_query.update(user_data.dict())
    db.commit()

    return db.query(User).filter(User.id == user_data.id).first()


# ---------- DELETE operations
def delete_user(db: Session, user_email: EmailStr):
    user_query = db.query(User).filter((User.email == user_email))
    user_query.delete()
    db.commit()

    return True


# ---------- AudioData model's services ----------

# ---------- SELECT operations
def get_all_audio_data(db: Session):
    all_audio_data = db.query(AudioData).all()

    return all_audio_data


def audio_data_of_session_id(db: Session, session_id: int):
    return db.query(AudioData).filter(AudioData.session_id == session_id).all()


def audio_data_of_user(db: Session, user_id: str):
    user_audio_data_query = db.query(AudioData).filter(AudioData.user_id == user_id).all()

    return user_audio_data_query


# ---------- INSERT operations
def add_audio_data(db: Session, audio_data: AudioDataDbSchema):
    new_audio_data = AudioData(**audio_data.dict())

    db.add(new_audio_data)
    db.commit()
    db.refresh(new_audio_data)

    return new_audio_data


# ---------- UPDATE operations
def update_audio_data(db: Session, audio_data: AudioDataDbSchema):
    audio_data_query = db.query(AudioData).filter(AudioData.unique_id == audio_data.unique_id)
    audio_data_query.update(audio_data.dict())
    db.commit()

    return db.query(AudioData).filter(AudioData.unique_id == audio_data.unique_id).first()
