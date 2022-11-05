"""
Router for endpoint: /user
"""
from fastapi import APIRouter, Depends, status, HTTPException, Request

from sqlalchemy.orm import Session

from pydantic import EmailStr

from server.database import get_db
from server.oauth2 import get_current_user, get_token_data
from server.utils import hash_password

from psql_db.schemas import UserAllSchema, UserSchema, SearchUserQueryBase, TokenPayloadSchema, UserUpdateSchema, \
    UserDbSchema, UserResponseSchema
from psql_db.crud import get_users, get_user, get_users_by_email, get_users_by_name, update_user, delete_user

# Router config
router = APIRouter(
    prefix="/user",
    tags=["User API"],
    responses={404: {"description": "not found"}}
)


# ----- create user ------
@router.get('/all', response_model=UserAllSchema, status_code=status.HTTP_200_OK)
def user_root(db: Session = Depends(get_db)):
    all_users = get_users(db=db)
    return {"all_users": all_users}


# ----- fuzzy search by email or name ------
@router.get('/search', status_code=status.HTTP_200_OK)
def find_user_by_email(given_query: SearchUserQueryBase, request: Request, db: Session = Depends(get_db)):
    # only email or name should be given
    if not ((given_query.email is None) ^ (given_query.name is None)):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Only email or name should be provided not both")

    if given_query.email:
        users_by_email = get_users_by_email(db, given_query.email)
        return {"search_result": users_by_email}

    if given_query.name:
        users_by_name = get_users_by_name(db, given_query.name)
        return {"search_result": users_by_name}


# ----- read user ------
# get a user by their id
@router.get('/id', response_model=UserSchema, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with id: {user_id}")
    return user


# get a user by their email
@router.get('/email', response_model=UserSchema, status_code=status.HTTP_200_OK)
def get_user_by_email(user_email: EmailStr, db: Session = Depends(get_db)):
    user = get_user(db=db, user_email=user_email)
    if not user:
        raise HTTPException(status_code=404, detail=f"No user with email: {user_email}")
    return user


# ----- update user -----
@router.patch('/update', response_model=UserResponseSchema)
def update_user_with_given_data(user_data: UserUpdateSchema, db: Session = Depends(get_db),
                                current_user: UserSchema = Depends(get_current_user)):
    # create final user object using UserDbSchema
    current_user_in_db = get_user(db=db, user_email=current_user.email)

    updated_user_data = UserDbSchema.from_orm(current_user_in_db)

    # id will be same uuid that was generated while creating the user
    updated_user_data.id = current_user.id

    # if trying to update email, check if email not taken
    if user_data.email and get_user(db=db, user_email=user_data.email):
        raise HTTPException(status_code=404, detail=f"User already exists with email: {user_data.email}")

    # update if new password is given, then hash it and save it
    if user_data.password:
        hashed_password = hash_password(user_data.password)
        updated_user_data.hashed_password = hashed_password
    else:
        updated_user_data.hashed_password = get_user(db=db, user_email=current_user.email).hashed_password

    # update name
    if user_data.name:
        updated_user_data.name = user_data.name

    # update email
    if user_data.email:
        updated_user_data.email = user_data.email

    # update address
    if user_data.address:
        updated_user_data.address = user_data.address

    # update image
    if user_data.image:
        updated_user_data.image = user_data.image

    updated_user = update_user(db=db, user_data=updated_user_data)
    return updated_user


# ------ delete user -----
@router.delete('/delete')
def delete_user_with_given_email(email: EmailStr, db: Session = Depends(get_db),
                                 current_user: UserSchema = Depends(get_current_user),
                                 token_data: TokenPayloadSchema = Depends(get_token_data)):
    # only admin or current_user can delete the given user
    user_with_email = get_user(db=db, user_email=email)
    if not user_with_email:
        raise HTTPException(status_code=404, detail=f"No user with email: {email}")

    if (current_user.email != email) and (not token_data.is_admin):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You can only delete your account, or have admin privileges")

    deleted = delete_user(db=db, user_email=email)
    if deleted:
        return {"result": f"user with email {email} is deleted"}
