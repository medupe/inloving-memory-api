from fastapi import FastAPI,Depends,HTTPException,status

from database import engine,SessionLocal,Base
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy.orm import Session
from routers import users

app = FastAPI()
app.include_router(users.router)


#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)




@app.get("/")
async def root():
    return {"message": "Hello World"}
'''

@app.post("/post",status_code=status.HTTP_201_CREATED)
async def create_post(post:PostBase,db:db_dependency):
    db_post = model.Post(**post.dict())
    db.add(db_post)
    db.commit()
@app.get("/post",status_code=status.HTTP_200_OK)
async def get_post(db:db_dependency):
    post = db.query(model.Post).all()
    return post
 '''