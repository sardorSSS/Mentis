from datetime import datetime
from typing import List
from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.assesment import Attendance, AttendanceType
from app.database.models.user import Student
# -----------------------
# ADD ATTENDANCE
# -----------------------
def add_attendance_db(student_id: int,lesson_date_time: datetime, att_status: AttendanceType,
    subject_id: int,topic_id: int) -> Attendance:
    with next(get_db()) as db:
        new_att = Attendance(student_id=student_id, lesson_date_time=lesson_date_time,
                             att_status=att_status,subject_id=subject_id, topic_id=topic_id)
        db.add(new_att)
        db.commit()
        db.refresh(new_att)
        return new_att

# -----------------------
# DELETE ATTENDANCE
# -----------------------
def delete_attendance_db(attendance_id: int) -> dict:
    with next(get_db()) as db:
        att = db.query(Attendance).filter_by(attendance_id=attendance_id).first()
        if not att:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись о посещаемости не найдена")
        db.delete(att)
        db.commit()
        return {"status": "Удалена"}

# -----------------------
# GET ATTENDANCE BY GROUP & SUBJECT
# -----------------------
def get_attendance_by_group_and_subject_db(group_id: int, subject_id: int) -> List[Attendance]:
    with next(get_db()) as db:
        records = (db.query(Attendance).join(Attendance.student).filter(Student.group_id == group_id,Attendance.subject_id == subject_id)
                   .all())
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Посещаемость группы {group_id} по предмету {subject_id} не найдена")
        return records

# -----------------------
# GET ATTENDANCE BY STUDENT & SUBJECT
# -----------------------
def get_attendance_by_student_and_subject_db(student_id: int,subject_id: int) -> List[Attendance]:
    with next(get_db()) as db:
        records = (db.query(Attendance).filter_by(student_id=student_id, subject_id=subject_id).all())
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Посещаемость студента {student_id} по предмету {subject_id} не найдена")
        return records

# -----------------------
# CHANGE STATUS BY LESSON
# -----------------------
def change_attendance_status_by_lesson_db(student_id: int, topic_id:int,
                                          new_status: AttendanceType) -> Attendance:
    with next(get_db()) as db:
        att = (db.query(Attendance).filter_by(student_id=student_id,topic_id = topic_id).first())
        if not att:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,detail="Запись о посещаемости для данного урока не найдена")
        att.status = new_status
        db.commit()
        db.refresh(att)
        return att

# -----------------------
# COUNT MISSED LESSONS
# -----------------------
def count_missed_lessons_db(student_id: int) -> int:
    with next(get_db()) as db:
        return db.query(Attendance).filter_by(student_id=student_id,att_status=AttendanceType.ABSENT).count()
