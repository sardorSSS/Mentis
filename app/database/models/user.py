from sqlalchemy import Column, Integer, DateTime, String, Boolean, Enum, Text, ForeignKey, Date, Table, JSON
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import func
import enum

class UserRole(enum.Enum):
    STUDENT = "student"
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"

class StudentStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class TeacherStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class AdminStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# Связующие таблицы
teacher_subject_table = Table(
    'teacher_subject',
    Base.metadata,
    Column('teacher_id', Integer, ForeignKey('teachers.teacher_id'), primary_key=True),
    Column('subject_id', Integer, ForeignKey('subjects.subject_id'), primary_key=True))

student_university_table = Table(
    'student_university',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id'), primary_key=True),
    Column('university_id', Integer, ForeignKey('universities.university_id'), primary_key=True),
    Column('priority_order', Integer, nullable=False))

# === ОСНОВНЫЕ МОДЕЛИ ПОЛЬЗОВАТЕЛЕЙ ===

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True)
    email = Column(String(150), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    registration_date = Column(DateTime(timezone=True), server_default=func.now())
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    photo = Column(String(255), nullable=True)
    # Полиморфные связи
    student = relationship("Student", back_populates="user", uselist=False)
    parent = relationship("ParentInfo", back_populates="user", uselist=False)
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    admin = relationship("Admin", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    direction = Column(String(200))
    student_status = Column(Enum(StudentStatus), default=StudentStatus.ACTIVE)
    group_id = Column(Integer, ForeignKey('groups.group_id'), nullable=True)
    
    # Связи
    user = relationship("User", back_populates="student", uselist=False)
    group = relationship("Group", back_populates="students")
    universities = relationship("University", secondary=student_university_table, back_populates="students")
    student_info = relationship("StudentInfo", back_populates="student", uselist=False)
    
    # Связи с экзаменами и оценками
    modul_exams = relationship("ModulExam", back_populates="student")
    dtm_exams = relationship("DtmExam", back_populates="student")
    section_exams = relationship("SectionExam", back_populates="student")
    block_exams = relationship("BlockExam", back_populates="student")
    topic_tests = relationship("TopicTest", back_populates="student")
    current_ratings = relationship("CurrentRating", back_populates="student")
    attendances = relationship("Attendance", back_populates="student")
    comments = relationship("Comments", back_populates="student")
    student_skills = relationship("StudentSkill", back_populates="student")

class StudentInfo(Base):
    __tablename__ = 'student_info'
    student_id = Column(Integer, ForeignKey("students.student_id", ondelete='CASCADE'), primary_key=True)
    hobby = Column(String(500))
    sex = Column(String(10))
    address = Column(Text)
    birthday = Column(Date)
    
    # Связи
    student = relationship("Student", back_populates="student_info")

class StudentSkill(Base):
    __tablename__ = 'student_skills'
    student_skill_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    correct = Column(JSON)
    mistakes = Column(JSON)
    
    # Связи
    student = relationship("Student", back_populates="student_skills")

class Teacher(Base):
    __tablename__ = 'teachers'
    teacher_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    teacher_schedule = Column(Text)
    teacher_status = Column(Enum(TeacherStatus), default=TeacherStatus.ACTIVE)
    
    # Связи
    user = relationship("User", back_populates="teacher")
    subjects = relationship("Subject", secondary=teacher_subject_table, back_populates="teachers")
    groups = relationship("Group", back_populates="teacher")
    comments = relationship("Comments", back_populates="teacher")
    teacher_info = relationship("TeacherInfo", back_populates="teacher", uselist=False)

class TeacherInfo(Base):
    __tablename__ = 'teacher_info'
    teacher_info_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id", ondelete='CASCADE'), nullable=False)
    teacher_employment = Column(String(100))
    teacher_number = Column(String(15))
    dop_info = Column(String(100))
    
    # Связи
    teacher = relationship("Teacher", back_populates='teacher_info')

class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    schedule = Column(Text)
    admin_status = Column(Enum(AdminStatus), default=AdminStatus.ACTIVE)
    
    # Связи
    user = relationship("User", back_populates="admin")
    admin_info = relationship("AdminInfo", back_populates="admin", uselist=False)

class AdminInfo(Base):
    __tablename__ = 'admin_info'
    admin_id = Column(Integer, ForeignKey('admins.admin_id', ondelete='CASCADE'), primary_key=True)
    admin_number = Column(String(14))
    employment = Column(String(100), nullable=True)
    admin_hobby = Column(String(100), nullable=True)
    
    # Связи
    admin = relationship("Admin", back_populates="admin_info")

class ParentInfo(Base):
    __tablename__ = 'parents'
    parent_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    profession = Column(String(200), nullable=True)
    parent_phone = Column(String(15), nullable=True)
    
    # Связи
    user = relationship("User", back_populates="parent")