"""
Router for endpoint: /auth
"""
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from psql_db.crud import create_new_user, get_user
from psql_db.models import User
from psql_db.schemas import UserDbSchema, UserNewSchema, UserNewResponseSchema, Token

import uuid

from server.database import get_db
from server.oauth2 import create_access_token
from server.utils import verify_password, hash_password

# Router config
router = APIRouter(
    prefix="/auth",
    tags=["Authentication API"],
    responses={404: {"description": "not found"}}
)


# ----- Login with email and password ------
@router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm -> {"username" :"", "password":""}
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"No user found with email:{user_credentials.username}")

    if not verify_password(plain_password=user_credentials.password, hashed_password=user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password"
        )

    # data = {"user_id": user.id, "is_admin": False}
    data = {"user_id": user.id, "user_email": user.email, "is_admin": False}

    # Make only admin@concha.com as the admin
    if user.email == 'admin@concha.com':
        data["is_admin"] = True

    # create a token
    access_token = create_access_token(data=data)

    return {"token": access_token, "token_type": "bearer"}


# ----- Sign up for new user ------
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserNewResponseSchema)
def signup(payload: UserNewSchema, db: Session = Depends(get_db)):
    # Validate for pre-existing user with same user_email
    existing_user_with_same_email = get_user(db=db, user_email=payload.email)
    if existing_user_with_same_email:
        raise HTTPException(status_code=404, detail=f"User already exists with email: {payload.email}")

    user_payload = UserDbSchema.parse_obj(payload)

    # Create Unique id for every user
    user_payload.id = str(uuid.uuid1())

    # hash the plain_password
    hashed_password = hash_password(payload.password)
    user_payload.hashed_password = hashed_password

    data = {"user_id": user_payload.id, "user_email": user_payload.email, "is_admin": False}

    # Make only admin@concha.com as the admin
    if user_payload.email == 'admin@concha.com':
        data["is_admin"] = True

    token_details = create_access_token(data=data)

    created_user = create_new_user(db=db, user_data=user_payload)

    return {"created_user_details": created_user, "token": token_details}
