from app.database import get_db
from app.database.models.assesment import CommentType, Comments
from typing import List
from fastapi import HTTPException, status
from sqlalchemy import or_

def add_comment_db(teacher_id: int, student_id: int, comment_text: str,
                   comment_type: CommentType) -> Comments:
    with next(get_db()) as db:
        new_comment = Comments(teacher_id=teacher_id, student_id=student_id,comment_text=comment_text,
            comment_type=comment_type)
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment

def delete_comment_db(comment_id: int) -> dict:
    with next(get_db()) as db:
        comment = db.query(Comments).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Комментарий не найден"
            )
        db.delete(comment)
        db.commit()
        return {"status": "Удалён"}

def edit_comment_text_db(comment_id: int,new_text: str) -> Comments:
    with next(get_db()) as db:
        comment = db.query(Comments).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Комментарий не найден"
            )
        comment.comment_text = new_text
        db.commit()
        db.refresh(comment)
        return comment

def edit_comment_type_db(comment_id: int,new_type: CommentType) -> Comments:
    with next(get_db()) as db:
        comment = db.query(Comments).filter_by(comment_id=comment_id).first()
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Комментарий не найден"
            )
        comment.comment_type = new_type
        db.commit()
        db.refresh(comment)
        return comment

# -----------------------
# GET COMMENTS BY STUDENT & TYPE
# -----------------------

def get_negative_comments_by_student_db(student_id: int) -> List[Comments]:
    with next(get_db()) as db:
        records = db.query(Comments).filter_by(student_id=student_id,
                                               comment_type=CommentType.NEGATIVE).all()
        if not records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Негативные комментарии для студента {student_id} не найдены"
            )
        return records

def get_positive_comments_by_student_db(student_id: int) -> List[Comments]:
    with next(get_db()) as db:
        records = db.query(Comments).filter_by(student_id=student_id, comment_type=CommentType.POSITIVE).all()
        if not records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Позитивные комментарии для студента {student_id} не найдены")
        return records

def get_neutral_comments_by_student_db(student_id: int) -> List[Comments]:
    with next(get_db()) as db:
        records = db.query(Comments) .filter_by(student_id=student_id, comment_type=CommentType.NEUTRAL).all()
        if not records:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Нейтральные комментарии для студента {student_id} не найдены")
        return records

def get_all_comments_by_student_db(student_id: int) -> List[Comments]:
    with next(get_db()) as db:
        records = db.query(Comments).filter_by(student_id=student_id).all()
        if not records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Комментарии для студента {student_id} не найдены")
        return records

def search_comments_by_text_db(search_text: str) -> List[Comments]:
    with next(get_db()) as db:
        records = db.query(Comments) .filter(Comments.comment_text.ilike(f"%{search_text}%")).all()
        if not records:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Комментариев, содержащих «{search_text}», не найдено")
        return records
