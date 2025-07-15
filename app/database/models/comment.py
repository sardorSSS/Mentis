from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import func

class Comments(Base):
    __tablename__ = 'comments'
    comment_id = Column(Integer, primary_key = True , autoincrement = True)
    teacher_id = Column(Integer, ForeignKey('teachers.teacher_id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    comment_text = Column(Text, nullable=False)
    comment_date = Column(DateTime(timezone=True),server_default=func.now())
    # Связи
    teacher = relationship("Teacher", back_populates="comments")
    student = relationship("Student", back_populates="comments")

