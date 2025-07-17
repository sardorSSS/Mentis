from sqlalchemy import (Float, DateTime, Column, Integer, ForeignKey, Text,
                        Enum, JSON, String)
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime
from sqlalchemy import func
import enum
from enum import Enum as PyEnum

class AttendanceType(enum.Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class TestType(PyEnum):
    VERIFICATION = 'verification'
    CURRENT = 'current'
    FINAL = 'final'

class CommentType(enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


# === ЭКЗАМЕНЫ И ОЦЕНКИ ===

class DtmExam(Base):
    __tablename__ = 'dtm_exams'
    exam_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    common_subject_score = Column(Float, nullable = False )
    second_subject_score = Column(Float, nullable = False)
    first_subject_score = Column(Float, nullable = False)
    total_score = Column(Float , nullable = False)
    exam_date = Column(DateTime, nullable = True)
    category_correct = Column(JSON, nullable=True)
    category_mistake = Column(JSON, nullable=True)
    # Связи
    student = relationship("Student", back_populates="dtm_exams")
    subject = relationship("Subject", back_populates="dtm_exams")

class SectionExam(Base):
    __tablename__ = 'section_exams'
    section_exam_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    score = Column(Float)
    exam_date = Column(DateTime)
    category_correct = Column(JSON, nullable=True)
    category_mistake = Column(JSON, nullable=True)
    # Связи
    student = relationship("Student", back_populates="section_exams")
    section = relationship("Section", back_populates="section_exams")

class BlockExam(Base):
    __tablename__ = 'block_exams'
    block_exam_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.block_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    score = Column(Float)
    exam_date = Column(DateTime)
    category_correct = Column(JSON, nullable=True)
    category_mistake = Column(JSON, nullable=True)
    # Связи
    student = relationship("Student", back_populates="block_exams")
    block = relationship("Block", back_populates="block_exams")
    subject = relationship("Subject", back_populates="block_exams")

class ModulExam(Base):
    __tablename__ = 'modul_exams'
    modul_exam_id = Column(Integer, primary_key=True, autoincrement=True)
    modul_id = Column(Integer, ForeignKey('moduls.modul_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    chem_score = Column(Float, nullable=False)
    bio_score = Column(Float, nullable=False)
    exam_date = Column(DateTime)
    category_correct = Column(JSON, nullable=True)
    category_mistake = Column(JSON, nullable=True)

    # Связи
    moduls = relationship("Moduls", back_populates="exams")
    student = relationship("Student", back_populates="modul_exams")
#Оценка за тест относящийся к определённой теме
class TopicTest(Base):
    __tablename__ = 'topic_tests'
    topic_test_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    score = Column(Float)
    attempt_date = Column(DateTime)
    # Связи
    student = relationship("Student", back_populates="topic_tests")
    topic = relationship("Topic", back_populates="topic_tests")

# Оценка за опрос
class CurrentRating(Base):
    __tablename__ = 'current_ratings'
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    current_score = Column(Float, nullable=False)
    second_current_score = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.now())
    # Связи
    student = relationship("Student", back_populates="current_ratings")
    subject = relationship("Subject", back_populates="current_ratings")
    topic = relationship("Topic", back_populates="current_ratings")

# === СИСТЕМА ТЕСТИРОВАНИЯ ===

class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    text = Column(Text, nullable=False)
    answer_1 = Column(String(500))
    answer_2 = Column(String(500))
    answer_3 = Column(String(500))
    answer_4 = Column(String(500))
    correct_answer = Column(Integer, nullable=False)
    explanation = Column(Text, nullable = True)
    category = Column(JSON, nullable=False, default=list)
    # Связи
    topic = relationship("Topic", back_populates="questions")

# === ПОСЕЩАЕМОСТЬ И КОММЕНТАРИИ ===

class Attendance(Base):
    __tablename__ = 'attendances'
    attendance_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    lesson_date_time = Column(DateTime, nullable=False)
    att_status = Column(Enum(AttendanceType), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    # Связи
    student = relationship("Student", back_populates="attendances")
    subject = relationship("Subject", back_populates="attendances")
    topic = relationship('Topic', back_populates="attendances")

class Comments(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    comment_text = Column(Text, nullable=False)
    comment_date = Column(DateTime(timezone=True), server_default=func.now())
    comment_type = Column(Enum(CommentType), nullable=False)
    # Связи
    teacher = relationship("Teacher", back_populates="comments")
    student = relationship("Student", back_populates="comments")

