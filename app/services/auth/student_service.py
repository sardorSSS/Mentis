from app.database import get_db
from app.database.models.parent import ParentInfo
from app.database.models.user import UserRole, User
from app.database.models.student import Student, StudentInfo
from app.database.models.admin import Admin,AdminInfo
from app.database.models.teacher import Teacher, TeacherInfo
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.hash_argon import *


