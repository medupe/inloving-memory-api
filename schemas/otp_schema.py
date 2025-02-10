from enum import Enum
from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from models.otp_model import OtpType

class OtpSchema(BaseModel):
    id :UUID
    otp : str
    createdAt :datetime
    expireTime : datetime
    isVerified : bool
  #  type :Optional[OtpType]=OtpType.REGISTER
class GetOtpSchema(BaseModel):
    processId :str
    otp : str