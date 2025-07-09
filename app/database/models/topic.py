from sqlalchemy import Float, Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key = True , autoincrement = True)
    block_id = Column(Integer, ForeignKey('blocks.block_id'), nullable=False)
    name = Column(String(200), nullable=False)
    content = Column(Text)
    additional_material = Column(Text)
    data = Column(String)
    # Связи
    block = relationship("Block", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
    topic_tests = relationship("Topic_test", back_populates="topic")

class TopicTest(Base):
    __tablename__ = 'topic_tests'
    topic_test_id = Column(Integer, primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    score = Column(Float)
    attempt_date = Column(DateTime)
    # Связи
    student = relationship("Student", back_populates="topic_tests")
    topic = relationship("Topic", back_populates="topic_tests")

class CurrentRating(Base):
    __tablename__ = 'current_ratings'
    rating_id = Column(Integer, primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    current_score = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

    # Связи
    student = relationship("Student", back_populates="current_ratings")
    subject = relationship("Subject", back_populates="current_ratings")


class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key = True , autoincrement = True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    text = Column(Text, nullable=False)
    answer_1 = Column(String(500))
    answer_2 = Column(String(500))
    answer_3 = Column(String(500))
    answer_4 = Column(String(500))
    correct_answer = Column(Integer, nullable=False)  # номер правильного ответа (1-4)
    difficulty_level = Column(Integer, default=1)  # 1-5
    explanation = Column(Text)
    # Связи
    topic = relationship("Topic", back_populates="questions")
