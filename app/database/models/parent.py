from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class ParentInfo(Base):
    __tablename__ = 'parents'
    parent_id =  Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    profession = Column(String(200), nullable=True)
    parent_phone = Column(String(15), nullable=True)

