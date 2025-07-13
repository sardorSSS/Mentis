from typing import Any
from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.exam import DtmExam, SectionExam, BlockExam

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


def add_pk_grade_db(student_id: int, pk_exam_id: int, score: float) -> PKExam:
    """
    Добавление оценки за PK.
    """
    with next(get_db()) as db:
        pk = PKExam(student_id=student_id, exam_id=pk_exam_id, score=score)
        db.add(pk)
        db.commit()
        db.refresh(pk)
        return pk


def add_ik_grade_db(student_id: int, ik_exam_id: int, score: float) -> IKExam:
    """
    Добавление оценки за IK.
    """
    with next(get_db()) as db:
        ik = IKExam(student_id=student_id, exam_id=ik_exam_id, score=score)
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

