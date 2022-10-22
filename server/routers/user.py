"""
`user` router handling all routes to /user
"""
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

import server.database
import psql_db.crud


router = APIRouter(
    prefix="/user",
    tags=["User API"],
    responses={404: {"description": "not found"}}
)


@router.get('/')
def user_root(db: Session = Depends(server.database.get_db)):
    all_users = psql_db.crud.get_users(db=db)
    return {"users": all_users}
