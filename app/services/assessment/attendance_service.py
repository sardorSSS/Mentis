from datetime import date, datetime
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import cast, Date
from app.database import get_db
from app.database.models.attendance import Attendance, AttendanceType
from app.database.models.student import Student


def add_attendance_db(student_id: int, lesson_date_time: datetime, attendance_type: str,
                      teacher_id: int,subject_id: int,) -> Attendance:

    try:
        att_type = AttendanceType(attendance_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid attendance_type: {attendance_type}",
        )

    with next(get_db()) as db:
        att = Attendance(
            student_id=student_id,
            lesson_date_time=lesson_date_time,
            type=att_type,
            teacher_id=teacher_id,
            subject_id=subject_id,
        )
        db.add(att)
        db.commit()
        db.refresh(att)
        return att


def delete_attendance_db(attendance_id: int) -> dict:

    with next(get_db()) as db:
        att = db.query(Attendance).get(attendance_id)
        if not att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance id={attendance_id} not found",
            )
        db.delete(att)
        db.commit()
        return {"message": "Attendance deleted"}


def update_attendance_type_db(attendance_id: int, attendance_type: str,) -> Attendance:
    try:
        new_type = AttendanceType(attendance_type)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid attendance_type: {attendance_type}",
        )

    with next(get_db()) as db:
        att = db.query(Attendance).get(attendance_id)
        if not att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance id={attendance_id} not found",
            )
        att.type = new_type
        db.commit()
        db.refresh(att)
        return att


def get_attendance_by_id(attendance_id: int) -> Attendance:
    with next(get_db()) as db:
        att = db.query(Attendance).get(attendance_id)
        if not att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance id={attendance_id} not found",
            )
        return att


def get_attendance_by_date(target_date: date) -> List[Attendance]:
    with next(get_db()) as db:
        return db.query(Attendance).filter(cast(Attendance.lesson_date_time, Date) == target_date).all()


def get_attendance_by_group(group_id: int) -> List[Attendance]:
    with next(get_db()) as db:
        return (
            db.query(Attendance)
            .join(Attendance.student)
            .filter(Student.group_id == group_id)
            .all()
        )