from sqlalchemy import DateTime, Column, Integer, ForeignKey, Enum,DateTime
from sqlalchemy.orm import relationship
from .base import Base
import enum

class AttendanceType(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class Attendance(Base):
    __tablename__ = 'attendances'
    attendance_id = Column(Integer, primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    lesson_date_time = Column(DateTime, nullable=False)
    type = Column(Enum(AttendanceType), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    topic_id = Column(Integer,ForeignKey('topics.topic_id'), primary_key = True)
    # Связи
    student = relationship("Student", back_populates="attendances")
    subject = relationship("Subject", back_populates="attendances")
    topic = relationship('Topic', back_populates="attendances" )

