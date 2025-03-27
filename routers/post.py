from fastapi import APIRouter,Form,File, FastAPI,Depends,HTTPException, UploadFile,status
from datetime import datetime
from models.post_model import PostModel
import models
from schemas.post_schema import PostSchema
from database import db_dependency
from utils.image_service import image_dependency


router = APIRouter(tags=["Post"])

@router.post("/post",status_code=status.HTTP_201_CREATED)
async def create_post( db:db_dependency,image:image_dependency,          
    file: UploadFile = File(...),  # File upload
    userId: str = Form(...), 
    postDescription: str = Form(...),
    dateOfBirth: datetime = Form(...),
    dateOfDeath: datetime = Form(...) ):
        
 
        imageId =await  image.upload_to_gcs(file,db,"post_photo",userId)
        print(imageId)
        postData = PostSchema(
            userId=userId,
            postDescription=postDescription,
            imgId=str(imageId), 
            dateOfBirth=dateOfBirth,
            dateOfDeath=dateOfDeath
        )

        db_post = models.post_model.PostModel(**postData.dict())
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

    