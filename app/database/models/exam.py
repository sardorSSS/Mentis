from sqlalchemy import Float, DateTime, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class DtmExam(Base):
    __tablename__ = 'dtm_exams'
    exam_id = Column(Integer, primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    common_score = Column(Float)
    second_subject_score = Column(Float)
    first_subject_score = Column(Float)
    exam_date = Column(DateTime)
    # Связи
    student = relationship("Student", back_populates="dtm_exams")
    subject = relationship("Subject", back_populates="dtm_exams")

#Промежуточный экзамен
class SectionExam(Base):
    __tablename__ = 'section_exams'
    section_exam_id = Column(Integer,primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    score = Column(Float)
    exam_date = Column(DateTime)
    # Связи
    student = relationship("Student", back_populates="section_exams")
    section = relationship("Section", back_populates="section_exams")

#Итоговый экзамен
class BlockExam(Base):
    __tablename__ = 'block_exams'
    block_exam_id = Column(Integer, primary_key = True , autoincrement = True)
    student_id = Column(Integer, ForeignKey('students.student_id'), nullable=False)
    block_id = Column(Integer, ForeignKey('blocks.block_id'), nullable=False)
    score = Column(Float)
    exam_date = Column(DateTime)
    subject_id = Column(Integer,ForeignKey('subjects.subject_is'), primary_key = True)
    # Связи
    student = relationship("Student", back_populates="block_exams")
    block = relationship("Block", back_populates="block_exams")
    subject = relationship("Subject", back_populates = "block_exam")


class ModulExam(Base):
    __tablename__ = 'modul_exam'
    modul_id = Column(Integer, ForeignKey('moduls.modul_id'), primary_key=True)
    student_id = Column(Column(Integer, ForeignKey('students.student_id'), nullable=False))
    chem_score = Column(Float, nullable = False)
    bio_score = Column(Float, nullable = False)
    exam_date = Column(DateTime)
    moduls = relationship("Moduls", back_populates = "exam")
    student = relationship("Student", back_populates="moduls_exams")


