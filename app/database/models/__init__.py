# models/__init__.py

from .base import Base, TimestampMixin, StatusMixin

# Пользователи и роли
from .users import (
    User, UserRole,
    Student, StudentInfo, StudentSkill, StudentStatus,
    Teacher, TeacherInfo, TeacherStatus,
    Admin, AdminInfo, AdminStatus,
    ParentInfo,
    teacher_subject_table,
    student_university_table
)

# Учебная структура
from .academic import (
    Subject, Section, SectionMaterial, Block, Topic,
    Group, GroupProgress,
    University, Faculty, UniversityType,
    Moduls
)

# Оценки, экзамены и тесты
from .assessments import (
    # Экзамены
    DtmExam, SectionExam, BlockExam, ModulExam,
    TopicTest, CurrentRating,
    
    # Тестирование
    Test, TestType, TestResult,
    Question, Category,
    question_category, test_question,
    
    # Посещаемость и комментарии
    Attendance, AttendanceType,
    Comments, CommentType
)

# Все модели для удобства
__all__ = [
    # Base
    'Base', 'TimestampMixin', 'StatusMixin',
    
    # Users
    'User', 'UserRole',
    'Student', 'StudentInfo', 'StudentSkill', 'StudentStatus',
    'Teacher', 'TeacherInfo', 'TeacherStatus', 
    'Admin', 'AdminInfo', 'AdminStatus',
    'ParentInfo',
    'teacher_subject_table', 'student_university_table',
    
    # Academic
    'Subject', 'Section', 'SectionMaterial', 'Block', 'Topic',
    'Group', 'GroupProgress',
    'University', 'Faculty', 'UniversityType',
    'Moduls',
    
    # Assessments
    'DtmExam', 'SectionExam', 'BlockExam', 'ModulExam',
    'TopicTest', 'CurrentRating',
    'Test', 'TestType', 'TestResult',
    'Question', 'Category',
    'question_category', 'test_question',
    'Attendance', 'AttendanceType',
    'Comments', 'CommentType'
]