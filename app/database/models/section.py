from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Section(Base):
    __tablename__ = 'sections'
    section_id = Column(Integer, primary_key = True , autoincrement = True)
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'), nullable=False)
    name = Column(String(200), nullable=True)
    # Связи
    subject = relationship("Subject", back_populates="sections")
    blocks = relationship("Block", back_populates="section")
    section_exams = relationship("Section_exam", back_populates="section")
    section_material = relationship('SectionMaterial', back_populates="section")

class SectionMaterial(Base):
    __tablename__ = 'section_material'
    section_id = Column(Integer,ForeignKey('sections.section_id'), primary_key =True)
    material_links = Column(String)
    section = relationship("Section", back_populates="section_material")



