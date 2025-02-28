from fastapi import APIRouter, FastAPI,Depends,HTTPException,status
from typing import Annotated

from fastapi import FastAPI, File, UploadFile


router = APIRouter(tags=["Post"])


router = APIRouter(tags=["Post"])
from fastapi import APIRouter, FastAPI,Depends,HTTPException,status

router = APIRouter(tags=["image"])
@router.post("/image/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@router.post("/upload/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}