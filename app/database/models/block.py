from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from .base import Base


class Block(Base):
    __tablename__ = 'blocks'
    block_id = Column(Integer, primary_key = True , autoincrement = True)
    section_id = Column(Integer, ForeignKey('sections.section_id'), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    # Связи
    section = relationship("Section", back_populates="blocks")
    topics = relationship("Topic", back_populates="block")
    block_exams = relationship("Block_exam", back_populates="block")

