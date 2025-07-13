from sqlalchemy import Column, Integer, ForeignKey, String, Text, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum

class AdminStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Admin(Base):
    __tablename__ = 'admins'
    admin_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    schedule = Column(Text)
    admin_status = Column(Enum(AdminStatus), default=AdminStatus.ACTIVE)
    # Связи
    user = relationship("User", back_populates="admin", ondelete='CASCADE')
    admin_info = relationship("AdminInfo", back_populates="admin")

class AdminInfo(Base):
    __tablename__ = 'admin_info'
    admin_id = Column(Integer, ForeignKey('admins.admin_id'), primary_key =True)
    admin_number = Column(String(14))
    employment = Column(String, nullable=True)
    admin_hobby = Column(String(100), nullable = True)
    admin = relationship("Admin", back_populates="admin_info")
