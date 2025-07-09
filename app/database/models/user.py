from sqlalchemy import Column, Integer, DateTime, String, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime

class UserRole(enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key = True , autoincrement = True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    photo = Column(String(255), nullable=True)
    # Полиморфные связи
    student = relationship("Student", back_populates="user", uselist=False)
    parent = relationship("ParentInfo", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)


    # Связи с экзаменами и оценками
    dtm_exams = relationship("DTM_exam", back_populates="student")
    section_exams = relationship("Section_exam", back_populates="student")
    block_exams = relationship("Block_exam", back_populates="student")
    topic_tests = relationship("Topic_test", back_populates="student")
    current_ratings = relationship("Current_rating", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    comments = relationship("Comments", back_populates="student")
