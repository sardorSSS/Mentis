from enum import Enum as PyEnum
from sqlalchemy import (Table, Column, Integer, String, Text,
                        ForeignKey, DateTime, CheckConstraint, Enum, JSON)
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import func


# Перечисление типов тестов
class TestType(PyEnum):
    VERIFICATION = 'verification'
    CURRENT = 'current'

# Ассоциативная таблица вопрос↔категория
question_category = Table(
    'question_category', Base.metadata,
    Column('question_id',  Integer, ForeignKey('questions.question_id'),  primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.category_id'), primary_key=True))

# Ассоциативная таблица тест↔вопрос (с полем порядка)
test_question = Table(
    'test_question', Base.metadata,
    Column('test_id',     Integer, ForeignKey('tests.test_id'),     primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.question_id'), primary_key=True),
    Column('order',       Integer, nullable=False))


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    name        = Column(String(100), unique=True, nullable=False)
    questions   = relationship("Question",secondary=question_category,back_populates="categories")

class Question(Base):
    __tablename__ = 'questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    topic_id=Column(Integer, ForeignKey('topics.topic_id'), nullable=False)
    text=Column(Text, nullable=False)
    answer_1=Column(String(500))
    answer_2=Column(String(500))
    answer_3=Column(String(500))
    answer_4=Column(String(500))
    correct_answer=Column(Integer, nullable=False)
    explanation=Column(Text)
    topic=relationship("Topic", back_populates="questions")
    categories=relationship("Category",secondary=question_category,back_populates="questions")
    tests= relationship("Test",secondary=test_question,back_populates="questions")

class Test(Base):
    __tablename__ = 'tests'
    test_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    test_type  = Column(Enum(TestType, name='test_type'), nullable=False, default=TestType.CURRENT)
    time_limit = Column(Integer, nullable=True)
    categories_distribution = Column(JSON, nullable=False, default=dict)

    __table_args__ = (CheckConstraint("test_type != 'verification' OR time_limit IS NOT NULL",
            name='verification_time_limit_ck'),)

    questions   = relationship("Question",secondary=test_question,back_populates="tests")
    results     = relationship("TestResult", back_populates="test")

class TestResult(Base):
    __tablename__ = 'test_results'
    result_id         = Column(Integer, primary_key=True)
    test_id           = Column(Integer, ForeignKey('tests.test_id'), nullable=False)
    user_id           = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    category_scores   = Column(JSON, nullable=False)
    question_results  = Column(JSON, nullable=False)
    total_correct     = Column(Integer, nullable=False)
    total_questions   = Column(Integer, nullable=False)
    taken_at          = Column(DateTime(timezone=True),server_default=func.now())
    test = relationship("Test", back_populates="results")
