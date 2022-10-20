"""
Schemas/Pydantic models for the PSQL db
"""

from pydantic.main import BaseModel, Extra, Field


# ----------  Schemas related to 'User' model   ----------

class UserBase(BaseModel):
    class Config:
        extra = Extra.forbid
        orm_mode = True

    id: int
    name: str
    email: str
    address: str
    image: str


# ----------  Schemas related to 'AudioDataFile' model   ----------

class TickBase(BaseModel):
    class Config:
        extra = Extra.forbid

    # each tick should be between -10 and -100
    tick: int = Field(..., ge=-100, le=-10)
