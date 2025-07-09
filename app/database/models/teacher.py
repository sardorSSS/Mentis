from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum, Table
from sqlalchemy.orm import relationship
from .base import Base
import enum


class StudentStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

teacher_subject_table = Table(
    'teacher_subject',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.teacher_id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.subject_id'), primary_key=True))

class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    teacher_schedule = Column(Text)
    teacher_status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)

    # Связи
    user = relationship("User", back_populates="teacher")
    subjects = relationship("Subject", secondary=teacher_subject_table, back_populates="teachers")
    groups = relationship("Group", back_populates="teacher")
    attendances = relationship("Attendance", back_populates="teacher")
    comments = relationship("Comments", back_populates="teacher")

class TeacherInfo(Base):
    __tablename__ = 'teacherinfo'
    teacher_employment = Column(String)
    teacher_number = Column(String(15))
    dop_info = Column(String(100))



