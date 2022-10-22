"""
`audio-data` router handling all routes to /audio-data
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import server.database
import psql_db.crud

router = APIRouter(
    prefix="/audio-data",
    tags=["Audio Data API"],
    responses={404: {"description": "not found"}}
)


@router.get('/', status_code=status.HTTP_200_OK)
def audio_data_root(db: Session = Depends(server.database.get_db)):
    all_audio_files = psql_db.crud.get_audio_files(db=db)
    return {"all audio data": all_audio_files}
