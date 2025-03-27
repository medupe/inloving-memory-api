from fastapi import APIRouter, FastAPI,Depends,HTTPException,status
from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from google.cloud import storage
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
load_dotenv()  # Load environment variables if using .env file
BUCKET_NAME = "omnicient_bucket-1"
router = APIRouter(tags=["Post"])
credentials = service_account.Credentials.from_service_account_file(
    "./utils/storage-service-account.json"
)

router = APIRouter(tags=["Post"])
from fastapi import APIRouter, FastAPI,Depends,HTTPException,status

router = APIRouter(tags=["image"])
@router.post("/image/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@router.post("/upload/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

def upload_to_gcs(file: UploadFile):
    """Uploads a file to Google Cloud Storage"""
    try:
        client = storage.Client(credentials=credentials)  # Authenticates using GOOGLE_APPLICATION_CREDENTIALS
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file.filename)
        
        blob.upload_from_file(file.file, content_type=file.content_type)

        return f"https://storage.googleapis.com/{BUCKET_NAME}/{file.filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/uploadGCM")
async def upload_imageGCS(file: UploadFile = File(...)):
    """API endpoint to upload an image"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    file_url = upload_to_gcs(file)
    return {"filename": file.filename, "url": file_url}