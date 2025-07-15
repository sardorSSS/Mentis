from sqlalchemy import Float, Column, Integer, ForeignKey, String, Table, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum

class UniversityType(enum.Enum):
    STATE = "state"
    PRIVATE = "private"

student_university_table = Table(
    'student_university',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id'), primary_key=True),
    Column('university_id', Integer, ForeignKey('universities.university_id'), primary_key=True),
    Column('priority_order', Integer, nullable=False))


class University(Base):
    __tablename__ = 'universities'
    university_id = Column(Integer, primary_key = True , autoincrement = True)
    name = Column(String(300), nullable=False)
    entrance_score = Column(Float)
    type = Column(Enum(UniversityType))
    location = Column(String(200), nullable = False)
    website = Column(String(300), nullable = False)
    # Связи
    students = relationship("Student", secondary=student_university_table, back_populates="universities")
