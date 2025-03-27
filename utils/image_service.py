from fastapi import APIRouter, FastAPI,Depends,HTTPException,status
from typing import Annotated
from models.image_model import ImageModel
from fastapi import FastAPI, File, UploadFile
from google.cloud import storage
from dotenv import load_dotenv
import os
from PIL import Image
from io import BytesIO

import models
from google.oauth2 import service_account
from database import db_dependency
from schemas.image_schema import ImageSchema
load_dotenv()  # Load environment variables if using .env file

BUCKET_NAME = "in-loving-memory"

credentials = service_account.Credentials.from_service_account_file(
    "utils/storage-service-account.json"
)

class ImageService:
    async def upload_to_gcs(self,file: UploadFile,db:db_dependency,folder_name,userId):
        try:

            client = storage.Client(credentials=credentials)  # Authenticates using GOOGLE_APPLICATION_CREDENTIALS
            bucket = client.bucket(BUCKET_NAME)
            blob = bucket.blob(f"{userId}/{folder_name}/{file.filename}")
            
            blob.upload_from_file(file.file, content_type=file.content_type)
       
            imageData = {
        
                "fileName":file.filename,
                "userId":userId,
                "fileUrl":f"https://storage.googleapis.com/{BUCKET_NAME}/{userId}/{folder_name}/{file.filename}",   

            }
      

            db_image = ImageModel(**imageData)
            db.add(db_image)
            db.commit()
            db.refresh(db_image)
            print(db_image.id)

            return db_image.id
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        



def get_image_service():
    return ImageService()

image_dependency = Annotated[ImageService,Depends(get_image_service)]
