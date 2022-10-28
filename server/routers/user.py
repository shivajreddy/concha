"""
Router for endpoint: /user
"""
from fastapi import APIRouter, Depends, status, HTTPException, Request

from sqlalchemy.orm import Session

from server.database import get_db
from server.oauth2 import get_current_user, get_token_data

from psql_db.schemas import UserAllSchema, UserSchema, SearchQueryBase, TokenPayloadSchema
from psql_db.crud import get_users, get_user, get_users_by_email, get_users_by_name

router = APIRouter(
    prefix="/user",
    tags=["User API"],
    responses={404: {"description": "not found"}}
)


# create user
@router.get('/all', response_model=UserAllSchema, status_code=status.HTTP_200_OK)
def user_root(db: Session = Depends(get_db)):
    all_users = get_users(db=db)
    return {"all_users": all_users}


# fuzzy search by email or name
@router.get('/search', status_code=status.HTTP_200_OK)
def find_user_by_email(given_query: SearchQueryBase, request: Request, db: Session = Depends(get_db)):
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


# update user
@router.patch('/update')
def update_user(db: Session = Depends(get_db),
                token_data: TokenPayloadSchema = Depends(get_token_data)):
    print(token_data)


# delete user


# read user
@router.get('/{user_id}', response_model=UserSchema, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=422, detail=f"No user with id:{user_id}")
    return user

#

# @router.post('/new', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
# def new_user(payload: UserNewSchema, db: Session = Depends(get_db)):
#     # Validate for pre-existing user with same user_id
#     existing_user_with_same_email = get_user(db=db, user_email=payload.email)
#     if existing_user_with_same_email:
#         raise HTTPException(status_code=404, detail=f"User already exists with email: {payload.email}")
#
#     user_payload = UserRegisterInDB.parse_obj(payload)
#
#     # Create Unique id for every user
#     user_payload.id = str(uuid.uuid1())
#
#     # hash the password
#     user_payload.hashed_password = "hash" + payload.password
#     print("after converting. user_payload = ", user_payload)
#
#     created_user = create_new_user(user_data=user_payload, db=db)
#     return created_user


# Other end points
# @router.get('/')
