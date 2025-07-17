from sqlalchemy import (Float, DateTime, Column, Integer, ForeignKey, Text,
                        Enum, Table, JSON, CheckConstraint, String, Boolean)
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

# Ассоциативные таблицы для тестирования
question_category = Table(
    'question_category', Base.metadata,
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id'), primary_key=True))

test_question = Table(
    'test_question', Base.metadata,
    Column('test_id', Integer, ForeignKey('tests.test_id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('order', Integer, nullable=False))

# === ЭКЗАМЕНЫ И ОЦЕНКИ ===

class DtmExam(Base):
    __tablename__ = 'dtm_exams'
    exam_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    common_score = Column(Float, nullable = False )
    second_subject_score = Column(Float, nullable = False)
    first_subject_score = Column(Float, nullable = False)
    total_score = Column(Float , nullable = False)
    exam_date = Column(DateTime)
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

    # Связи
    moduls = relationship("Moduls", back_populates="exams")
    student = relationship("Student", back_populates="modul_exams")

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

class CurrentRating(Base):
    __tablename__ = 'current_ratings'
    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    current_score = Column(Float, nullable=False)
    second_current_score = Column(Float, nullable=False)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Связи
    student = relationship("Student", back_populates="current_ratings")
    subject = relationship("Subject", back_populates="current_ratings")
    topic = relationship("Topic", back_populates="current_ratings")

# === СИСТЕМА ТЕСТИРОВАНИЯ ===

class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    # Связи
    questions = relationship("Question", secondary=question_category, back_populates="categories")

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
    explanation = Column(Text)
    # Связи
    topic = relationship("Topic", back_populates="questions")
    categories = relationship("Category", secondary=question_category, back_populates="questions")
    tests = relationship("Test", secondary=test_question, back_populates="questions")

class Test(Base):
    __tablename__ = 'tests'
    test_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    test_type = Column(Enum(TestType, name='test_type'), nullable=False, default=TestType.CURRENT)
    time_limit = Column(Integer, nullable=True)
    categories_distribution = Column(JSON, nullable=False, default=dict)

    __table_args__ = (CheckConstraint("test_type != 'verification' OR time_limit IS NOT NULL",
            name='verification_time_limit_ck'),)

    # Связи

    questions = relationship("Question", secondary=test_question, back_populates="tests")
    results = relationship("TestResult", back_populates="test")

class TestResult(Base):
    __tablename__ = 'test_results'
    result_id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tests.test_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_scores = Column(JSON, nullable=False)
    question_results = Column(JSON, nullable=False)
    total_correct = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    taken_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связи
    test = relationship("Test", back_populates="results")
    user = relationship("User", back_populates="test_results")

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

