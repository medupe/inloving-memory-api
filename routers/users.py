from fastapi import APIRouter, FastAPI,Depends,HTTPException,status
from datetime import datetime
from models.otp_model import OtpType,OTPModel
from models.user_model import UserModel
import models

from schemas.user_schema import UserBase,LoginBase
from schemas.otp_schema import OtpSchema,GetOtpSchema
from database import db_dependency
from utils.email_service import email_dependency
from utils.otp_service import otp_dependency
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)




@router.get("/users/", tags=["users"])
async def read_users(db : db_dependency,email:email_dependency,otp:otp_dependency):
    await otp.sendOtp(db,OtpType.REGISTER,email_dependency)
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def create_user(user:UserBase,db:db_dependency,otp:otp_dependency):

    hashed_pw = hash_password(user.password) 
    userData= user.model_copy(update={"password": hashed_pw}) # Hash the password
    db_user = models.user_model.UserModel(**userData.dict())
    if db.query(UserModel).filter(UserModel.email == user.email,UserModel.isVerified ==True).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    elif  db.query(UserModel).filter(UserModel.email == user.email,UserModel.isVerified ==False).first():
        db.delete(db_user)
    
    db.add(db_user)
    db.commit()
    
    otpInfo =await  otp.sendOtp(userData.name,userData.email,"OTP sent",db)
    return {"processId" : otpInfo}

@router.post("/login",status_code=status.HTTP_201_CREATED)
async def login(login:LoginBase,db:db_dependency):
    stored_user = db.get(login.email)
    hashed_pw = hash_password(login.password)  # Hash the password
    if not stored_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    if not verify_password(login.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    #db.add(db_user.model_copy(update={"password": hashed_pw}))
  #  db.commit()
@router.post("/confirm-otp",status_code=status.HTTP_201_CREATED)
async def confirmOtp(otpSchema:GetOtpSchema,db:db_dependency):
        if db.query(OTPModel).filter(OTPModel.expireTime <  datetime.now(),OTPModel.isVerified ==False).first():
            raise HTTPException(status_code=400, detail="Otp expired")
        
        elif  db.query(OTPModel).filter(OTPModel.otp !=  otpSchema.otp,OTPModel.isVerified ==False).first():
            raise HTTPException(status_code=400, detail="Invalid otp")
        elif  db.query(OTPModel).filter(OTPModel.otp ==  otpSchema.otp,OTPModel.isVerified ==False).first():
             otpTable = db.query(UserModel).filter(UserModel.id == GetOtpSchema.processId ).first()
             otpTable.isVerified = True
             db.commit()
             db.refresh(otpTable)
        else :
            raise HTTPException(status_code=400, detail="Error occured confirming your otp")



        
    #db.add(db_user.model_copy(update={"password": hashed_pw}))
  #  db.commit()