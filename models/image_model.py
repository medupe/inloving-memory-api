from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,Enum, Integer, String, TIMESTAMP, Boolean, text,DateTime
from datetime import datetime, timedelta
import enum

class ImageModel(Base):
    __tablename__ = "image"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    otp = Column(String,nullable=False)
    createdAt = Column(DateTime, nullable=False,)
    fileName = Column(String,nullable=False)
    fileUrl = Column(String,nullable=False)
    userId = Column(String,nullable=False)
    
    