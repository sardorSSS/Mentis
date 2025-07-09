from sqlalchemy import Column, Integer, ForeignKey, String, Text, Table
from sqlalchemy.orm import relationship
from .base import Base

teacher_subject_table = Table(
    'teacher_subject',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.teacher_id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.subject_id'), primary_key=True))

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement = True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    # Связи
    teachers = relationship("Teacher", secondary=teacher_subject_table, back_populates="subjects")
    sections = relationship("Section", back_populates="subject")
    groups = relationship("Group", back_populates="subject")
    dtm_exams = relationship("DTM_exam", back_populates="subject")
    current_ratings = relationship("Current_rating", back_populates="subject")
    attendances = relationship("Attendance", back_populates="subject")
