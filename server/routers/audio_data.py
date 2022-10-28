"""
`audio-data` router handling all routes to /audio-data
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db

from server.oauth2 import get_current_user

from psql_db.crud import get_audio_data_by_session_id, get_all_audio_data, add_audio_data
from psql_db.schemas import AudioDataFileSchema, UserSchema

# Router config
router = APIRouter(
    prefix="/audio-data",
    tags=["Audio Data API"],
    responses={404: {"description": "not found"}}
)


@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_audio_files(db: Session = Depends(get_db)):
    all_data = get_all_audio_data(db)
    return all_data
    # return {"all_data": all_data}


# utility function to validate session_ids
def validation_checks(new_audio: AudioDataFileSchema, all_audio_data: list):
    print('validation')


# def user_root(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):

# @router.post('/new', dependencies=[Depends(get_current_user)])
@router.post('/new')
def new_audio_data(audio_data: AudioDataFileSchema, db: Session = Depends(get_db),
                   current_user: UserSchema = Depends(get_current_user)):
    # TODO if current_user is an admin, then take the given user_id instead of admins id
    # given_user_id = current_user.id   # for normal users
    # given_user_id = audio_data.user_id    # for admin

    # validations:2 ->
    # check if session_id exists
    # “Session_id” must be unique to a user
    # same session_id cant have same step_count
    existing_audios = get_audio_data_by_session_id(db=db, session_id=audio_data.session_id)

    if existing_audios:
        for existing_audio in existing_audios:
            if existing_audio.user_id != current_user.id:
                print("bro same session_id", existing_audios)
                raise HTTPException(status_code=422, detail=f"{current_user.email} cant add to another usedid")
        raise HTTPException(status_code=422, detail=f"{audio_data.session_id} already exits")

    # Finished the validations
    # call the service that adds the data
    audio_data.user_id = current_user.id
    created_audio_data = add_audio_data(db=db, audio_data=audio_data)

    return {"created_audio_data": created_audio_data}
