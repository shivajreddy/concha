"""
`user` router handling all routes to /user
"""
from fastapi import APIRouter, Depends, status, HTTPException, Request

from sqlalchemy.orm import Session

from server.database import get_db
from psql_db.schemas import UserNewSchema, UserAllSchema, UserSchema, UserResponseSchema, EmailBase

# Crud Utils
from psql_db.crud import get_users, create_new_user, get_user, get_by_email

router = APIRouter(
    prefix="/user",
    tags=["User API"],
    responses={404: {"description": "not found"}}
)


@router.get('/all', response_model=UserAllSchema, status_code=status.HTTP_200_OK)
def user_root(db: Session = Depends(get_db)):
    all_users = get_users(db=db)
    return {"all_users": all_users}


# fuzzy search by email
@router.get('/search', status_code=status.HTTP_200_OK)
async def find_user_by_email(given_query: EmailBase, request: Request, db: Session = Depends(get_db)):
    users_by_email = get_by_email(db, given_query.email)
    return {"result": users_by_email}


@router.get('/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=400, detail=f"No user with id:{user_id}")
    return user


@router.post('/new', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def new_user(payload: UserNewSchema, db: Session = Depends(get_db)):
    # Validate for pre-existing user with same user_id
    existing_user = get_user(db=db, user_id=payload.id)
    if existing_user:
        raise HTTPException(status_code=404, detail=f"User already exists with id: {payload.id}")

    # Validate for pre-existing user with same user_id
    existing_user_with_same_email = get_user(db=db, user_email=payload.email)
    if existing_user_with_same_email:
        raise HTTPException(status_code=404, detail=f"User already exists with email: {payload.email}")

    created_user = create_new_user(user_data=payload, db=db)
    return created_user
