from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column,Enum, Integer, String, TIMESTAMP, Boolean, text,DateTime
from datetime import datetime, timedelta
import enum
# Get current UTC time
current_time = datetime.utcnow()

# Add 15 minutes
future_time = current_time + timedelta(minutes=15)

class OtpType(str, enum.Enum):  # Use str for JSON compatibility
    REGISTER = "register"

class OTPModel(Base):
    __tablename__ = "otp"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    otp = Column(String,nullable=False)
    createdAt = Column(DateTime, nullable=False, default=datetime.utcnow)
    expireTime = Column(DateTime, nullable=False, default=future_time)
    isVerified = Column(Boolean, server_default='False')
    #type = Column(Enum(OtpType), nullable=False)