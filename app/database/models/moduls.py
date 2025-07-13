from sqlalchemy import Column, Integer,Float, String
from sqlalchemy.orm import relationship
from .base import Base
from app.database.models.exam import ModulExam

class Moduls(Base):
    __tablename__ = 'moduls'
    modul_id = Column(Integer, primary_key = True , autoincrement = True)
    start_topic_chem = Column(Integer)
    start_topic_bio = Column(Integer)
    end_topic_chem = Column(Integer)
    end_topic_bio = Column(Integer)
    exam = relationship("ModulsExam", back_populates="moduls")





