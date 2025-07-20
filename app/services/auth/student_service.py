from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import and_, or_
from app.database import get_db
from app.database.models.academic import GroupProgress, University, Faculty, UniversityType
from app.database.models.assesment import TopicTest, ModulExam, BlockExam, SectionExam


def add_group_progress_db(group_id: int, topic_id: int, data: str) -> GroupProgress:
    """Добавление прогресса группы по конкретному уроку"""
    with next(get_db()) as db:
        # Проверяем, существует ли уже запись для данной группы и урока
        existing_progress = db.query(GroupProgress).filter_by(
            group_id=group_id, topic_id=topic_id
        ).first()

        if existing_progress:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Прогресс для группы {group_id} по уроку {topic_id} уже существует"
            )

        new_progress = GroupProgress(
            group_id=group_id,
            topic_id=topic_id,
            data=data
        )
        db.add(new_progress)
        db.commit()
        db.refresh(new_progress)
        return new_progress


def update_group_progress_db(group_progress_id: int, data: str) -> GroupProgress:
    """Изменение прогресса группы по конкретному уроку"""
    with next(get_db()) as db:
        progress = db.query(GroupProgress).filter_by(
            group_progress_id=group_progress_id
        ).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Прогресс группы не найден"
            )

        progress.data = data
        db.commit()
        db.refresh(progress)
        return progress


def delete_group_progress_db(group_progress_id: int) -> dict:
    """Удаление прогресса группы по конкретному уроку"""
    with next(get_db()) as db:
        progress = db.query(GroupProgress).filter_by(
            group_progress_id=group_progress_id
        ).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Прогресс группы не найден"
            )

        db.delete(progress)
        db.commit()
        return {"status": "Удален"}


def get_group_progress_by_lesson_db(group_id: int, topic_id: int) -> GroupProgress:
    """Получение прогресса группы по конкретному уроку"""
    with next(get_db()) as db:
        progress = db.query(GroupProgress).filter_by(
            group_id=group_id, topic_id=topic_id
        ).first()

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Прогресс группы {group_id} по уроку {topic_id} не найден"
            )

        return progress


# ===========================================
# STUDENT EXAM STATUS OPERATIONS
# ===========================================

def get_overdue_exams_db(student_id: int) -> dict:
    """Получение всех просроченных тестов конкретного ученика"""
    with next(get_db()) as db:
        today = datetime.now().date()

        # Получаем все экзамены студента, где дата экзамена меньше сегодняшней
        overdue_topic_tests = db.query(TopicTest).filter(
            and_(
                TopicTest.student_id == student_id,
                TopicTest.attempt_date < today
            )
        ).all()

        overdue_module_exams = db.query(ModulExam).filter(
            and_(
                ModulExam.student_id == student_id,
                ModulExam.exam_date < today
            )
        ).all()

        overdue_block_exams = db.query(BlockExam).filter(
            and_(
                BlockExam.student_id == student_id,
                BlockExam.exam_date < today
            )
        ).all()

        overdue_section_exams = db.query(SectionExam).filter(
            and_(
                SectionExam.student_id == student_id,
                SectionExam.exam_date < today
            )
        ).all()

        return {
            "student_id": student_id,
            "overdue_topic_tests": overdue_topic_tests,
            "overdue_module_exams": overdue_module_exams,
            "overdue_block_exams": overdue_block_exams,
            "overdue_section_exams": overdue_section_exams,
            "total_overdue": (len(overdue_topic_tests) + len(overdue_module_exams) +
                              len(overdue_block_exams) + len(overdue_section_exams))
        }


def get_upcoming_exams_db(student_id: int) -> dict:
    """Получение актуальных тестов (в ближайшие 2 дня) конкретного ученика"""
    with next(get_db()) as db:
        today = datetime.now().date()
        two_days_later = today + timedelta(days=2)

        # Получаем все экзамены студента на ближайшие 2 дня
        upcoming_topic_tests = db.query(TopicTest).filter(
            and_(
                TopicTest.student_id == student_id,
                TopicTest.attempt_date >= today,
                TopicTest.attempt_date <= two_days_later
            )
        ).all()

        upcoming_module_exams = db.query(ModulExam).filter(
            and_(
                ModulExam.student_id == student_id,
                ModulExam.exam_date >= today,
                ModulExam.exam_date <= two_days_later
            )
        ).all()

        upcoming_block_exams = db.query(BlockExam).filter(
            and_(
                BlockExam.student_id == student_id,
                BlockExam.exam_date >= today,
                BlockExam.exam_date <= two_days_later
            )
        ).all()

        upcoming_section_exams = db.query(SectionExam).filter(
            and_(
                SectionExam.student_id == student_id,
                SectionExam.exam_date >= today,
                SectionExam.exam_date <= two_days_later
            )
        ).all()

        return {
            "student_id": student_id,
            "upcoming_topic_tests": upcoming_topic_tests,
            "upcoming_module_exams": upcoming_module_exams,
            "upcoming_block_exams": upcoming_block_exams,
            "upcoming_section_exams": upcoming_section_exams,
            "total_upcoming": (len(upcoming_topic_tests) + len(upcoming_module_exams) +
                               len(upcoming_block_exams) + len(upcoming_section_exams))
        }


# ===========================================
# UNIVERSITY OPERATIONS
# ===========================================

def add_university_db(name: str, entrance_score: Optional[float],
                      university_type: UniversityType, location: str, website: str) -> University:
    """Добавление нового университета"""
    with next(get_db()) as db:
        # Проверяем, существует ли уже университет с таким именем
        existing_university = db.query(University).filter_by(name=name).first()
        if existing_university:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Университет с именем '{name}' уже существует"
            )

        new_university = University(
            name=name,
            entrance_score=entrance_score,
            type=university_type,
            location=location,
            website=website
        )
        db.add(new_university)
        db.commit()
        db.refresh(new_university)
        return new_university


def update_university_db(university_id: int, name: Optional[str] = None,
                         entrance_score: Optional[float] = None,
                         university_type: Optional[UniversityType] = None,
                         location: Optional[str] = None,
                         website: Optional[str] = None) -> University:
    """Изменение информации о университете"""
    with next(get_db()) as db:
        university = db.query(University).filter_by(university_id=university_id).first()

        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Университет не найден"
            )

        if name is not None:
            university.name = name
        if entrance_score is not None:
            university.entrance_score = entrance_score
        if university_type is not None:
            university.type = university_type
        if location is not None:
            university.location = location
        if website is not None:
            university.website = website

        db.commit()
        db.refresh(university)
        return university


def delete_university_db(university_id: int) -> dict:
    """Удаление университета"""
    with next(get_db()) as db:
        university = db.query(University).filter_by(university_id=university_id).first()

        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Университет не найден"
            )

        db.delete(university)
        db.commit()
        return {"status": "Удален"}


def get_university_by_id_db(university_id: int) -> University:
    """Получение университета по ID"""
    with next(get_db()) as db:
        university = db.query(University).filter_by(university_id=university_id).first()

        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Университет не найден"
            )

        return university


def get_all_universities_db() -> List[University]:
    """Получение всех университетов"""
    with next(get_db()) as db:
        universities = db.query(University).all()
        return universities


# ===========================================
# FACULTY OPERATIONS
# ===========================================

def add_faculty_db(university_id: int, name: str, description: Optional[str] = None,
                   entrance_score: Optional[float] = None) -> Faculty:
    """Добавление нового факультета"""
    with next(get_db()) as db:
        # Проверяем, существует ли университет
        university = db.query(University).filter_by(university_id=university_id).first()
        if not university:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Университет не найден"
            )

        # Проверяем, существует ли уже факультет с таким именем в данном университете
        existing_faculty = db.query(Faculty).filter_by(
            university_id=university_id, name=name
        ).first()
        if existing_faculty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Факультет '{name}' уже существует в данном университете"
            )

        new_faculty = Faculty(
            university_id=university_id,
            name=name,
            description=description,
            entrance_score=entrance_score
        )
        db.add(new_faculty)
        db.commit()
        db.refresh(new_faculty)
        return new_faculty


def update_faculty_db(faculty_id: int, name: Optional[str] = None,
                      description: Optional[str] = None,
                      entrance_score: Optional[float] = None) -> Faculty:
    """Изменение информации о факультете"""
    with next(get_db()) as db:
        faculty = db.query(Faculty).filter_by(faculty_id=faculty_id).first()

        if not faculty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Факультет не найден"
            )

        if name is not None:
            faculty.name = name
        if description is not None:
            faculty.description = description
        if entrance_score is not None:
            faculty.entrance_score = entrance_score

        db.commit()
        db.refresh(faculty)
        return faculty


def delete_faculty_db(faculty_id: int) -> dict:
    """Удаление факультета"""
    with next(get_db()) as db:
        faculty = db.query(Faculty).filter_by(faculty_id=faculty_id).first()

        if not faculty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Факультет не найден"
            )

        db.delete(faculty)
        db.commit()
        return {"status": "Удален"}


def get_faculty_by_id_db(faculty_id: int) -> Faculty:
    """Получение факультета по ID"""
    with next(get_db()) as db:
        faculty = db.query(Faculty).filter_by(faculty_id=faculty_id).first()

        if not faculty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Факультет не найден"
            )

        return faculty


def get_faculties_by_university_db(university_id: int) -> List[Faculty]:
    """Получение всех факультетов конкретного университета"""
    with next(get_db()) as db:
        faculties = db.query(Faculty).filter_by(university_id=university_id).all()

        if not faculties:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Факультеты для университета {university_id} не найдены"
            )

        return faculties


def get_all_faculties_db() -> List[Faculty]:
    """Получение всех факультетов"""
    with next(get_db()) as db:
        faculties = db.query(Faculty).all()
        return faculties


