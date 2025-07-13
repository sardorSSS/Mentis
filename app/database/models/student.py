from sqlalchemy import Date, Column, Integer, ForeignKey, String, Text, Enum, Table
from sqlalchemy.orm import relationship
from .base import Base
import enum
from app.database.models.exam import ModulExam

class StudentStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


# Связь Teacher-Subject (простая связь)
teacher_subject_table = Table(
    'teacher_subject',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.teacher_id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.subject_id'), primary_key=True))

# Связь Student-University (с приоритетом)
student_university_table = Table(
    'student_university',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id'), primary_key=True),
    Column('university_id', Integer, ForeignKey('universities.university_id'), primary_key=True),
    Column('priority_order', Integer, nullable=False))

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    direction = Column(String(200))
    student_status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)
    group_id = Column(Integer, ForeignKey('groups.group_id'))
    # Связи
    user = relationship("User", back_populates="student", uselist=False,
        cascade="all, delete-orphan")
    group = relationship("Group", back_populates="students")
    universities = relationship("University", secondary=student_university_table, back_populates="students")
    student_info = relationship("StudentInfo", back_populates="student")
    moduls_exam = relationship("ModulsExam", back_populates="student")

class StudentInfo(Base):
    __tablename__ = 'student_info'
    student_id = Column(Integer, ForeignKey("students.student_id") ,primary_key = True)
    hobby = Column(String(500))
    sex = Column(String(10))
    address = Column(Text)
    birthday = Column(Date)
    student = relationship("Student", back_populates="student_info")
