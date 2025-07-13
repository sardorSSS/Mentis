from typing import Optional, List, Any
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.database.models.subject import Subject
from app.database.models.section import Section
from app.database.models.moduls import Moduls
from app.database.models.topic import Topic
from app.database.models.topic import Question



def add_comment_db(parent_type: str, parent_id: int, text: str) -> Comment:
    """
    Добавление комментария к объекту parent_type (например, 'DTMExam', 'Question').
    """
    with next(get_db()) as db:
        comment = Comment(parent_type=parent_type, parent_id=parent_id, text=text)
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment


def update_comment_db(comment_id: int, text: str) -> Comment:
    """
    Редактирование текста комментария.
    """
    with next(get_db()) as db:
        comm = db.query(Comment).get(comment_id)
        if not comm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Comment id={comment_id} not found")
        comm.text = text
        db.commit()
        db.refresh(comm)
        return comm


def delete_comment_db(comment_id: int) -> dict:
    """
    Удаление комментария.
    """
    with next(get_db()) as db:
        comm = db.query(Comment).get(comment_id)
        if not comm:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Comment id={comment_id} not found")
        db.delete(comm)
        db.commit()
        return {"message": "Comment deleted"}
