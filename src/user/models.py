from sqlalchemy import Column, String, BigInteger, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    email = Column(String(50), nullable=False)
    password = Column(String(100))
    nickname = Column(String(10))
    user_phone = Column(String(11))
    user_address = Column(String(256))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
