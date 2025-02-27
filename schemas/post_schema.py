from enum import Enum
from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, date, time

from models.otp_model import OtpType

class PostSchema(BaseModel):
    userId: str
    isEnabled:bool
    address:str
    city:str
    province:str
    lon:str
    lat:str
    imgurl:str
    dateOfBirth:datetime
    dateOfDeath:datetime
    creationDate:datetime
    class Config:
        orm_mode = True  # Enables ORM serialization
        from_attributes = True