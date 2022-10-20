"""
`user` router handling all routes to /user
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["User API"],
    responses={404: {"description": "not found"}}
)


@router.get('/')
def user_root():
    return {"user": "home"}
