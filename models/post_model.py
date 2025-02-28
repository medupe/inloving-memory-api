from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,Enum, Integer, String, TIMESTAMP, Boolean, text,DateTime
from datetime import datetime, timedelta

class PostModel(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    userId = Column(String,nullable=False)
    isEnabled = Column(Boolean, server_default='True',default=True)
    address = Column(String,nullable=False)
    city = Column(String,nullable=False)
    province = Column(String,nullable=False)
    lon = Column(String,nullable=False)
    lat = Column(String,nullable=False)
    imgurl = Column(String,nullable=False)
    dateOfBirth = Column(DateTime, nullable=False, )
    dateOfDeath = Column(DateTime, nullable=False, )
    creationDate = Column(DateTime, nullable=False,default=datetime.utcnow )