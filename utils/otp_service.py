from datetime import datetime,timedelta,timezone
from typing import Annotated
from fastapi.params import Depends
import random
from models.otp_model import OtpType,OTPModel
from .email_service import email_dependency
from schemas.otp_schema import OtpSchema
import models
from database import db_dependency
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
file_path = os.path.join(base_dir, "email.html")  # Append the file name
       
# Get current UTC time
utc_plus_2 = timezone(timedelta(hours=2))  # UTC+2 timezone
current_time = datetime.now(utc_plus_2)

# Add 15 minutes
future_time = current_time + timedelta(minutes=15)
class OtpService: 
    async def sendOtp(self,name, email ,subject,db:db_dependency ,userId):
            otp = random.randint(1000, 9999)
            otp_data = {
                 "otp":str(otp),
                 "createdAt":current_time,
                 "expireTime":future_time,
                 "isVerified":False,
                 "userId" : userId
            }
            print(otp_data)
           
            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()
                html_content = html_content.replace("{{OTP_CODE}}", str(otp))
            db_otp = models.otp_model.OTPModel(**otp_data)
            db.add(db_otp)
            db.commit()
            db.refresh(db_otp)
            await email_dependency.sendEmail(self,name,email,subject,html_content)
            return db_otp.id
def get_otp_service():
    return OtpService()
otp_dependency = Annotated[OtpService,Depends(get_otp_service)]