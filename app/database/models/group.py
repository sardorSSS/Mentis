from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import Base

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key = True , autoincrement = True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'), nullable=False)
    name = Column(String(100), nullable=False)
    academic_year = Column(String(20))
    # Связи
    subject = relationship("Subject", back_populates="groups")
    teacher = relationship("Teacher", back_populates="groups")
    students = relationship("Student", back_populates="group")
