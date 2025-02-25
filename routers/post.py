from fastapi import APIRouter, FastAPI,Depends,HTTPException,status
from datetime import datetime
from models.otp_model import OtpType,OTPModel
from models.post_model import PostModel
from models.user_model import UserModel
import models
from schemas.post_schema import PostSchema

from schemas.user_schema import UserBase,LoginBase,ForgotPasswordBase,ConfirmNewPasswordBase
from schemas.otp_schema import OtpSchema,GetOtpSchema
from database import db_dependency
from utils.email_service import email_dependency
from utils.otp_service import otp_dependency
from passlib.context import CryptContext

router = APIRouter(tags=["Post"])

@router.post("/post",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostSchema,db:db_dependency,):
    db_post = models.post_model.PostModel(**post.dict())
    db.add(db_post) 
    db.commit()
    db.refresh(db_post)
    return {"message" : "Success"}

@router.get("/post",status_code=status.HTTP_201_CREATED)
async def get_post(db:db_dependency,):
    model =    db.query(PostModel).filter( PostModel.isEnabled ==True).first()
    return model


@router.put("/post/{post_id}",status_code=status.HTTP_201_CREATED)
async def update_post( post_id:str,   post_updater:PostSchema,db:db_dependency):
    # Update the event without checking specific fields
    post = db.query(PostModel).filter(PostModel.id == post_id)

    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    
    post.update(post_updater.model_dump(exclude_unset=True))
    db.commit()
    return {"message": f"Event with ID {post_id} updated successfully"}

@router.delete("/post/{post_id}",status_code=status.HTTP_201_CREATED)
async def delete_post(post_id: str,db:db_dependency):
        # Find the event by ID
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Event not found")

    # Delete the event
    db.delete(post)
    db.commit()

    return {"message": f"Event with ID {post_id} deleted successfully"}

    