from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from server.database import get_db
from psql_db.models import User
from psql_db.schemas import UserRegisterInDB
from server.oauth2 import oauth2

from server.utils import verify_password

router = APIRouter(tags=['Authentication'], prefix='/auth')


@router.get('/login')
# def login(user_credentials: UserLoginSchema, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm -> {"username" :"", "password":""}
    user = db.query(User).filter(User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"No user found with email:{user_credentials.username}")

    print("comparing")
    print("plain given password = ", user_credentials.password)
    print("hashed password = ", user.password)
    if not verify_password(plain_password=user_credentials.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password"
        )

    # create a token
    access_token = oauth2.create_access_token(data={"user_id": user.id, "is_admin": False})

    return {"token": access_token, "token_type": "bearer"}
