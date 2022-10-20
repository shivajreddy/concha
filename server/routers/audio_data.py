"""
`audio-data` router handling all routes to /audio-data
"""
from fastapi import APIRouter

router = APIRouter(
    prefix="/audio-data",
    tags=["Audio Data API"],
    responses={404: {"description": "not found"}}
)


@router.get('/')
def audio_data_root():
    return {"user": "home"}
