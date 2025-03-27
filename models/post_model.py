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
    #address = Column(String,nullable=True)
    #city = Column(String,nullable=True)
    #province = Column(String,nullable=True)
    #lon = Column(String,nullable=True)
    #lat = Column(String,nullable=True)
    imgId = Column(String,nullable=False)
    postDescription = Column(String,nullable=False)
    personDetails = Column(String,nullable=False)
    dateOfBirth = Column(DateTime, nullable=False, )
    dateOfDeath = Column(DateTime, nullable=False, )
    dateOfBurial= Column(DateTime, nullable=True, )
    creationDate = Column(DateTime, nullable=False,default=datetime.utcnow )
    address = Column(String,nullable=True)
    city = Column(String,nullable=True)
    province = Column(String,nullable=True)
    lon = Column(String,nullable=True)
    lat = Column(String,nullable=True)
    orbituary = Column(String,nullable=True)
    dateOfBurial = Column(DateTime, nullable=True, )


    #things to create after post
    #burial location
    #postDetails - burial location-city,province -orbituary-date of burial
    #Agenda -  speaker - occupation - postID - creationtime
    #discussion - condolenses - postID 
           

