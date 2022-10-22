"""
This module contains all the CRUD utils
"""
from sqlalchemy.orm import Session
from psql_db.models import User, AudioDataFile


# ---------- USER model's services ----------

# ---------- SELECT operations
def get_users(db: Session):
    users = db.query(User).all()
    return users
