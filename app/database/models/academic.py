from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum

class UniversityType(enum.Enum):
    STATE = "state"
    PRIVATE = "private"

# === УЧЕБНАЯ СТРУКТУРА ===

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Связи
    teachers = relationship("Teacher", secondary="teacher_subject", back_populates="subjects")
    sections = relationship("Section", back_populates="subject", cascade="all, delete-orphan")
    groups = relationship("Group", back_populates="subject")
    dtm_exams = relationship("DtmExam", back_populates="subject")
    current_ratings = relationship("CurrentRating", back_populates="subject")
    attendances = relationship("Attendance", back_populates="subject")
    block_exams = relationship("BlockExam", back_populates="subject")

class Section(Base):
    __tablename__ = 'sections'
    section_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    name = Column(String(200), nullable=False)
    
    # Связи
    subject = relationship("Subject", back_populates="sections")
    blocks = relationship("Block", back_populates="section")
    section_exams = relationship("SectionExam", back_populates="section", cascade="all, delete-orphan")
    section_materials = relationship('SectionMaterial', back_populates="section", cascade="all, delete-orphan")

class SectionMaterial(Base):
    __tablename__ = 'section_materials'
    section_material_id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    material_links = Column(Text)
    
    # Связи
    section = relationship("Section", back_populates="section_materials")

class Block(Base):
    __tablename__ = 'blocks'
    block_id = Column(Integer, primary_key=True, autoincrement=True)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Связи
    section = relationship("Section", back_populates="blocks")
    topics = relationship("Topic", back_populates="block", cascade="all, delete-orphan")
    block_exams = relationship("BlockExam", back_populates="block")

class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    block_id = Column(Integer, ForeignKey('blocks.block_id'), nullable=False)
    name = Column(String(200), nullable=False)
    homework = Column(Text)
    number = Column(Integer)
    additional_material = Column(Text)  # ссылки на видео
    
    # Связи
    block = relationship("Block", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
    topic_tests = relationship("TopicTest", back_populates="topic")
    attendances = relationship("Attendance", back_populates="topic")
    current_ratings = relationship("CurrentRating", back_populates="topic")
    group_progress = relationship("GroupProgress", back_populates="topic")

class Group(Base):
    __tablename__ = 'groups'
    group_id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    
    # Связи
    subject = relationship("Subject", back_populates="groups")
    teacher = relationship("Teacher", back_populates="groups")
    students = relationship("Student", back_populates="group")
    group_progress = relationship("GroupProgress", back_populates="group")

class GroupProgress(Base):
    __tablename__ = 'group_progress'
    group_progress_id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    data = Column(Text, nullable=False)
    
    # Связи
    group = relationship("Group", back_populates="group_progress")
    topic = relationship("Topic", back_populates="group_progress")

class University(Base):
    __tablename__ = 'universities'
    university_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(300), nullable=False)
    entrance_score = Column(Float)
    type = Column(Enum(UniversityType))
    location = Column(String(200), nullable=False)
    website = Column(String(300), nullable=False)
    
    # Связи
    students = relationship("Student", secondary="student_university", back_populates="universities")
    faculties = relationship("Faculty", back_populates="university")

class Faculty(Base):
    __tablename__ = 'faculties'
    faculty_id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(Integer, ForeignKey('universities.university_id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    entrance_score = Column(Float, nullable=True)
    
    # Связи
    university = relationship("University", back_populates="faculties")

class Moduls(Base):
    __tablename__ = 'moduls'
    modul_id = Column(Integer, primary_key=True, autoincrement=True)
    start_topic_chem = Column(Integer, nullable=False)
    start_topic_bio = Column(Integer, nullable=False)
    end_topic_chem = Column(Integer, nullable=False)
    end_topic_bio = Column(Integer, nullable=False)
    
    # Связи
    exams = relationship("ModulExam", back_populates="moduls")