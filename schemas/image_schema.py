
from pydantic import BaseModel


class ImageSchema(BaseModel):
    fileName:str
    userId:str