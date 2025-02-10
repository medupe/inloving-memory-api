from fastapi import APIRouter, FastAPI,Depends,HTTPException,status
from datetime import datetime
from models.otp_model import OtpType,OTPModel
from models.user_model import UserModel
import models

from schemas.user_schema import UserBase,LoginBase,ForgotPasswordBase,ConfirmNewPasswordBase
from schemas.otp_schema import OtpSchema,GetOtpSchema
from database import db_dependency
from utils.email_service import email_dependency
from utils.otp_service import otp_dependency
from passlib.context import CryptContext

router = APIRouter(tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)







@router.post("/register",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase,db:db_dependency,otp:otp_dependency):

    hashed_pw = hash_password(user.password) 
    userData= user.model_copy(update={"password": hashed_pw}) # Hash the password
    db_user = models.user_model.UserModel(**userData.dict())
    user_exist_not_verified =   db.query(UserModel).filter(UserModel.email == user.email,UserModel.isVerified ==False).first()
    if db.query(UserModel).filter(UserModel.email == user.email,UserModel.isVerified ==True).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    elif  user_exist_not_verified:
        db.delete(user_exist_not_verified)
    db.add(db_user) 
    db.commit()
    db.refresh(db_user)
    otpInfo =await  otp.sendOtp(userData.name,userData.email,"OTP sent",db,db_user.id)
    return {"processId" : otpInfo}

@router.post("/login",status_code=status.HTTP_201_CREATED)
async def login(login:LoginBase,db:db_dependency):
    user=  db.query(UserModel).filter(UserModel.email == login.email ,UserModel.isVerified==True).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    if not verify_password(login.password, UserModel.password):
        raise HTTPException(status_code=400, detail="Password does not match")

    return {"data": user}
@router.post("/confirm-otp-register",status_code=status.HTTP_201_CREATED)
async def confirmOtp(otpSchema:GetOtpSchema,db:db_dependency):
        if db.query(OTPModel).filter(OTPModel.id == otpSchema.processId,    OTPModel.expireTime <  datetime.now(),OTPModel.isVerified ==False).first():
            raise HTTPException(status_code=400, detail="Otp expired")
        elif  db.query(OTPModel).filter( OTPModel.id == otpSchema.processId,  OTPModel.otp !=  otpSchema.otp,OTPModel.isVerified ==False).first():
            raise HTTPException(status_code=400, detail="Invalid otp")
        elif  db.query(OTPModel).filter(OTPModel.id == otpSchema.processId,OTPModel.otp ==  otpSchema.otp,OTPModel.isVerified ==False, ).first():
             otp =  db.query(OTPModel).filter(OTPModel.id == otpSchema.processId,OTPModel.otp ==  otpSchema.otp,OTPModel.isVerified ==False, ).first()
             userTable = db.query(UserModel).filter(UserModel.id == otp.userId ).first()
             otp.isVerified = True
             userTable.isVerified = True
             db.commit()
        else :
            raise HTTPException(status_code=400, detail="Error occured confirming your otp")

@router.post("/forgot-password",status_code=status.HTTP_201_CREATED)
async def forgot_password(user:ForgotPasswordBase,db:db_dependency,otp:otp_dependency):
    user_exist =   db.query(UserModel).filter(UserModel.email == user.email,UserModel.isVerified ==True).first()
    if not user_exist:
        raise HTTPException(status_code=400, detail="User does not exist")
    otpInfo =await  otp.sendOtp(user_exist.name,user_exist.email,"OTP sent",db,user_exist.id)
    return {"processId" : otpInfo}

@router.post("/confirm-otp-password",status_code=status.HTTP_201_CREATED)
async def confirmOtp(otpSchema:GetOtpSchema,db:db_dependency):
        if db.query(OTPModel).filter(OTPModel.id == otpSchema.processId,    OTPModel.expireTime <  datetime.now(),OTPModel.isVerified ==False).first():
            raise HTTPException(status_code=400, detail="Otp expired")
        elif  db.query(OTPModel).filter( OTPModel.id == otpSchema.processId,  OTPModel.otp !=  otpSchema.otp,OTPModel.isVerified ==False).first():
            raise HTTPException(status_code=400, detail="Invalid otp")
        elif  db.query(OTPModel).filter(OTPModel.id == otpSchema.processId,OTPModel.otp ==  otpSchema.otp,OTPModel.isVerified ==False, ).first():
             otp =  db.query(OTPModel).filter(OTPModel.id == otpSchema.processId,OTPModel.otp ==  otpSchema.otp,OTPModel.isVerified ==False, ).first()
             otp.isVerified = True
             db.commit()
        else :
            raise HTTPException(status_code=400, detail="Error occured confirming your otp")

@router.post("/change-password",status_code=status.HTTP_201_CREATED)
async def change_password(user:ConfirmNewPasswordBase,db:db_dependency):
    otpExist =  db.query(OTPModel).filter(OTPModel.id == user.processId,   OTPModel.isVerified ==True).first()
  
    if not otpExist:
        raise HTTPException(status_code=400, detail="process id is wrong")
    otpExist.isVerified = True
    db.commit()
    hashed_new_pw = hash_password(user.newPassword) 
    user_exist =db.query(UserModel).filter(UserModel.id == otpExist.userId,UserModel.isVerified ==True).first()
    user_exist.password = hashed_new_pw
    db.commit()
    db.query(OTPModel).filter(OTPModel.id == user.processId,   OTPModel.isVerified ==True).delete()
  
    db.commit()
