"""
Schemas/Pydantic models for the PSQL db
"""
from pydantic.main import BaseModel, Extra, Field
from pydantic import EmailStr
from pydantic.types import conint, confloat, conlist


# ----------  Schemas related to 'User' model   ----------

# Response schema for a single user
class UserSchema(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    id: str
    name: str
    email: EmailStr
    address: str
    image: str
    # is_admin: bool


class UserAllSchema(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    all_users: list[UserSchema]


class UserNewSchema(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    # id: int
    name: str
    email: EmailStr
    password: str
    address: str
    image: str


class UserRegisterInDB(BaseModel):
    class Config:
        orm_mode = True

    id: str | None = None
    name: str
    email: EmailStr
    hashed_password: str | None = None
    address: str
    image: str


class EmailBase(BaseModel):
    email: EmailStr


# Response schema for a group of users
class UserResponseSchema(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    id: str
    name: str
    email: EmailStr
    address: str
    image: str


# ----------  Schemas related to 'AudioDataFile' model   ----------

class TickBase(BaseModel):
    class Config:
        extra = Extra.forbid

    # each tick should be between -10 and -100
    tick: int = Field(..., ge=-100, le=-10)


class AudioDataFileSchema(BaseModel):
    class Config:
        extra = Extra.forbid

    session_id: conint(strict=True)
    ticks: conlist(confloat(strict=True, ge=-100.0, le=-10.0), min_items=15, max_items=15)
    selected_tick: conint(strict=True, ge=0, le=14)
    step_count: conint(strict=True, ge=0, le=9)

    user_id: str | None = None


# ---------- Authorization schema ----------

class TokenPayloadSchema(BaseModel):
    user_id: str | None
    user_email: str | None
    is_admin: bool = False


class Token(BaseModel):
    token: str
    token_type: str


class UserNewResponseSchema(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    created_user_details: UserResponseSchema
    token: str
