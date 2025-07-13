from typing import Any, Optional
from datetime import datetime
from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.moduls import Moduls
from app.database.models.exam import DtmExam, SectionExam, BlockExam, ModulExam
from app.database.models.student import Student

def add_dtm_grade_db(student_id: int, dtm_exam_id: int, score: float) -> DtmExam:
    """
    Добавление оценки за DTM.
    """
    with next(get_db()) as db:
        dtm = DtmExam(student_id=student_id, exam_id=dtm_exam_id, score=score)
        db.add(dtm)
        db.commit()
        db.refresh(dtm)
        return dtm


def add_pk_grade_db(student_id: int, pk_exam_id: int, score: float) -> BlockExam:
    """
    Добавление оценки за PK.
    """
    with next(get_db()) as db:
        pk = BlockExam(student_id=student_id, exam_id=pk_exam_id, score=score)
        db.add(pk)
        db.commit()
        db.refresh(pk)
        return pk


def add_ik_grade_db(student_id: int, ik_exam_id: int, score: float) -> SectionExam:
    with next(get_db()) as db:
        ik = SectionExam(student_id=student_id, exam_id=ik_exam_id, score=score)
        db.add(ik)
        db.commit()
        db.refresh(ik)
        return ik


def update_grade_db(exam_model: Any, grade_id: int, score: float) -> Any:
    """
    Редактирование любой оценки (DTM, PK, IK).
    exam_model — модель SQLAlchemy (DTMExam, PKExam или IKExam)
    """
    with next(get_db()) as db:
        grade = db.query(exam_model).get(grade_id)
        if not grade:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Grade id={grade_id} not found in {exam_model.__name__}")
        grade.score = score
        db.commit()
        db.refresh(grade)
        return grade
def add_modul_exam_db(modul_id: int, student_id: int, chem_score: float, bio_score: float,
                      exam_date: Optional[datetime] = None,) -> ModulExam:
    """
    Добавляет оценку по указанному модулю для заданного студента.
    Проверяет существование модуля и студента.
    """
    with next(get_db()) as db:
        # Проверка существования модуля
        modul = db.query(Moduls).get(modul_id)
        if not modul:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Modul id={modul_id} not found",
            )
        # Проверка существования студента
        student = db.query(Student).get(student_id)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student id={student_id} not found",
            )
        # Создание записи оценки
        modul_exam = ModulExam(
            modul_id=modul_id,
            student_id=student_id,
            chem_score=chem_score,
            bio_score=bio_score,
            exam_date=exam_date,
        )
        db.add(modul_exam)
        db.commit()
        db.refresh(modul_exam)
        return modul_exam