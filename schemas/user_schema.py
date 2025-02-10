
from pydantic import BaseModel,EmailStr
from typing import Optional

class UserBase(BaseModel):
    name:str
    surname:str
    cellNumber:str
    email:EmailStr
    city:str
    profile_pic_url:Optional[str]
    password: str

class LoginBase(BaseModel):
    email:str
    password:str
class ForgotPasswordBase(BaseModel):
    email:str
class ConfirmNewPasswordBase(BaseModel):
    processId: str
    newPassword:str