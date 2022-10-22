"""
This module contains all the CRUD utils
"""
from sqlalchemy.orm import Session
from psql_db.models import User, AudioDataFile
from psql_db.schemas import UserNewSchema


# ---------- USER model's services ----------

# ---------- SELECT operations
def get_users(db: Session):
    users = db.query(User).all()
    return users


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


# ---------- INSERT operations
def create_new_user(user_data: UserNewSchema, db: Session):
    print(user_data.dict())
    # new_post = Post(**post.dict())
    # new_post = Post(id=post.id, title=post.title, content=post.title, published=post.published)
    new_user = User(**user_data.dict())
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ---------- AudioData model's services ----------

# ---------- SELECT operations
def get_audio_files(db: Session):
    audio_files = db.query(AudioDataFile).all()
    return audio_files
