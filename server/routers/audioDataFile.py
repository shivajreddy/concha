from fastapi import APIRouter

router = APIRouter(
    prefix="/audio",
    tags=["Audio Data API"],
    responses={404: {"description": "not found"}}
)


@router.get('/')
def audio_root():
    return {"user": "home"}
