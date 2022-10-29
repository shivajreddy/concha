"""
Router for endpoint: /audio-data
"""
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from server.database import get_db

from server.oauth2 import get_current_user, get_token_data

from psql_db.crud import audio_data_of_session_id, get_all_audio_data, add_audio_data, get_user
from psql_db.schemas import AudioDataSchema, UserSchema, TokenPayloadSchema, AudioDataDbSchema

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


# ----- create audio_data ------
@router.post('/new')
def new_audio_data(audio_data: AudioDataSchema,
                   user_id: str = None,
                   db: Session = Depends(get_db),
                   current_user: UserSchema = Depends(get_current_user),
                   token_data: TokenPayloadSchema = Depends(get_token_data)):
    # validate: if user adding their account, or has admin privileges, and user_id should be valid
    if user_id:
        if (user_id != current_user.id) and (not token_data.is_admin):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=f"You can only add audio_data to your account, or have admin privileges")
        if not get_user(db=db, user_id=user_id):
            raise HTTPException(status_code=404, detail=f"No user with id: {user_id}")

    # id of the user to whom the audio data should be added
    if user_id:
        assign_to_user_with_id = user_id
    else:
        assign_to_user_with_id = current_user.id

    # find all audio data of given session_id and validate for duplicate step_count
    all_audios_of_session_id = audio_data_of_session_id(db=db, session_id=audio_data.session_id)

    if all_audios_of_session_id:

        # validate: given session_id can be assigned to pre-existing user only
        if all_audios_of_session_id[0].user_id != assign_to_user_with_id:
            raise HTTPException(status_code=422,
                                detail=f"session_id:{audio_data.session_id} is taken by user with email: {all_audios_of_session_id[0].user.email}")

        # validate: for the given session_id, only new step_count(0-9) are allowed
        for audio in all_audios_of_session_id:
            if audio.step_count == audio_data.step_count:
                raise HTTPException(status_code=422,
                                    detail=f"Step count:{audio.step_count} already exists for session_id:{audio_data.session_id}")

    final_audio_data = AudioDataDbSchema.parse_obj(audio_data)
    final_audio_data.user_id = assign_to_user_with_id
    final_audio_data.unique_id = audio_data.session_id + "-" + audio_data.step_count

    created_audio_data = add_audio_data(db=db, audio_data=final_audio_data)

    return {"created_audio_data": created_audio_data}
