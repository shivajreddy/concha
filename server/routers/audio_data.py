"""
Router for endpoint: /audio-data
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db

from server.oauth2 import get_current_user

from psql_db.crud import audio_data_of_session_id, get_all_audio_data, add_audio_data
from psql_db.schemas import AudioDataFileSchema, UserSchema

# Router config
router = APIRouter(
    prefix="/audio-data",
    tags=["Audio Data API"],
    responses={404: {"description": "not found"}}
)


# ----- get all audio_data------
@router.get('/all', status_code=status.HTTP_200_OK)
def get_all_audio_files(db: Session = Depends(get_db)):
    all_data = get_all_audio_data(db)
    return all_data
    # return {"all_data": all_data}


# utility function to validate session_ids
def validation_checks(new_audio: AudioDataFileSchema, all_audio_data: list, current_user):
    print('validation')

    # For the given all_audio_data, make sure existing user_id and given_user_id matches
    if current_user.id != all_audio_data[0].user_id:
        print("bro same session_id", all_audio_data)
        raise HTTPException(status_code=422,
                            detail=f"current user_id: {current_user.id} cant add session to another user with id: {all_audio_data[0].user_id}")

    # Each session must have unique step_count with range 0 to 9
    for audio in all_audio_data:
        if audio.step_count == new_audio.step_count:
            raise HTTPException(status_code=422,
                                detail=f"Step count:{new_audio.step_count} already exists")


# ----- create audio_data ------
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
    # ALl audio_data for a given session_id
    audios_of_session_id = audio_data_of_session_id(db=db, session_id=audio_data.session_id)

    if audios_of_session_id:
        validation_checks(new_audio=audio_data, all_audio_data=audios_of_session_id, current_user=current_user)

    # Finished the validations
    # call the service that adds the data
    audio_data.user_id = current_user.id
    created_audio_data = add_audio_data(db=db, audio_data=audio_data)

    return {"created_audio_data": created_audio_data}
