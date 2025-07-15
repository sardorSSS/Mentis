from sqlalchemy import Float, Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class Topic(Base):
    __tablename__ = 'topics'
    topic_id = Column(Integer, primary_key = True , autoincrement = True)
    block_id = Column(Integer, ForeignKey('blocks.block_id'), nullable=False)
    name = Column(String(200), nullable=False)
    Homework = Column(Text)
    number = Column(Integer)
    # ссылки на видео
    additional_material = Column(Text)
    # Связи
    block = relationship("Block", back_populates="topics")
    questions = relationship("Question", back_populates="topic")
    topic_tests = relationship("Topic_test", back_populates="topic")
    attendance = relationship("Attendance", back_populates="topic" )

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
    current_rating = relationship("CurrentRating", back_populates = "topic")
# текущая оценка
class CurrentRating(Base):
    __tablename__ = 'current_ratings'
    rating_id = Column(Integer, primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    current_score = Column(Float, nullable = False)
    second_current_score = Column(Float, nullable = False)
    last_updated = Column(DateTime, default=datetime.utcnow)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'), primary_key = True)
    # Связи
    student = relationship("Student", back_populates="current_ratings")
    subject = relationship("Subject", back_populates="current_ratings")
    topic = relationship("Topic", back_populates="current_rating")



