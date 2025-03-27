from enum import Enum
from fastapi import UploadFile
from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, date, time

from models.otp_model import OtpType

class PostSchema(BaseModel):
    userId:str
    #isEnabled:bool
    postDescription:str
    imgId : str
    dateOfBirth:datetime
    dateOfDeath:datetime

class PostDetailSchema(BaseModel):
    postId:str
    address:str
    city:str
    province:str
    lon:str
    lat:str
    orbituary:str
    dateOfBurial:str
