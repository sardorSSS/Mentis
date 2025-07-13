from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database.models.user import User

from .base import Base

class ParentInfo(Base):
    __tablename__ = 'parents'
    parent_id =  Column(Integer, ForeignKey('users.user_id'), primary_key=True, ondelete='CASCADE')
    profession = Column(String(200), nullable=True)
    parent_phone = Column(String(15), nullable=True)
    user = relationship("User", back_populates="parent")


