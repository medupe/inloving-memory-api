from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text
    
class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String,nullable=False)
    surname = Column(String,nullable=False)
    cellNumber = Column(String,nullable=False)
    email = Column(String,nullable=False)
    city = Column(String,nullable=False)
    profile_pic_url =Column(String,nullable=True,default="https://www.gravatar.com/avatar/?d=identicon")
    blocked = Column(Boolean, server_default='False',default=True)
    password = Column(String,nullable=False)
    isVerified = Column(Boolean, server_default='False',default=False)
  
    