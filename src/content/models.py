from sqlalchemy import Column, String, BigInteger, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from core.database import Base
from sqlalchemy.orm import relationship
from src.user.models import User

class Sketch(Base):
    __tablename__ = "sketch"

    sketch_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    sketch_title = Column(String(50), nullable=False)
    sketch_url = Column(String(256), nullable=False)
    is_removed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
    removed_at = Column(DateTime(timezone=True))
    content_id = Column(BigInteger)
    user_id = Column(BigInteger, ForeignKey('user.user_id'))

    user = relationship('User', back_populates='sketch')

User.sketch = relationship('Sketch', back_populates='user')


class Content(Base):
    __tablename__ = "content"

    content_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    content_title = Column(String(50), nullable=False)
    content_type = Column(Boolean, default=False)
    content_url = Column(String(256), nullable=False)
    is_removed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
    removed_at = Column(DateTime(timezone=True))
    user_id = Column(BigInteger, ForeignKey('user.user_id'))

    user = relationship('User', back_populates='content')

User.content = relationship('Content', back_populates='content')


class Design(Base):
    __tablename__ = "design"

    design_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    design_url = Column(String(256), nullable=False)
    is_removed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
    removed_at = Column(DateTime(timezone=True))
    content_id = Column(BigInteger, ForeignKey('content.content_id'))

    content = relationship('Content', back_populates='design')

Content.design = relationship('Design', back_populates='design')
