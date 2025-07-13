from typing import Optional, List
from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.attendance import Attendance


def add_attendance_db(student_id: int, lesson_id: int, status: str, comment: Optional[str] = None) -> Attendance:
    """
    Добавление записи посещаемости.
    status: 'present', 'late', 'absent'
    """
    with next(get_db()) as db:
        att = Attendance(student_id=student_id, lesson_id=lesson_id, status=status, comment=comment)
        db.add(att)
        db.commit()
        db.refresh(att)
        return att


def get_attendance_db(attendance_id: int) -> Attendance:
    with next(get_db()) as db:
        att = db.query(Attendance).get(attendance_id)
        if not att:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attendance id={attendance_id} not found")
        return att


def update_attendance_db(attendance_id: int, status: Optional[str] = None, comment: Optional[str] = None) -> Attendance:
    with next(get_db()) as db:
        att = db.query(Attendance).get(attendance_id)
        if not att:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attendance id={attendance_id} not found")
        if status is not None:
            att.status = status
        if comment is not None:
            att.comment = comment
        db.commit()
        db.refresh(att)
        return att


def delete_attendance_db(attendance_id: int) -> dict:
    with next(get_db()) as db:
        att = db.query(Attendance).get(attendance_id)
        if not att:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attendance id={attendance_id} not found")
        db.delete(att)
        db.commit()
        return {"message": "Attendance deleted"}


def get_attendance_by_student_db(student_id: int) -> List[Attendance]:
    with next(get_db()) as db:
        return db.query(Attendance).filter(Attendance.student_id == student_id).all()