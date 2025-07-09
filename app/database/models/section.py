from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Section(Base):
    __tablename__ = 'sections'
    section_id = Column(Integer, primary_key = True , autoincrement = True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    # Связи
    subject = relationship("Subject", back_populates="sections")
    blocks = relationship("Block", back_populates="section")
    section_exams = relationship("Section_exam", back_populates="section")
