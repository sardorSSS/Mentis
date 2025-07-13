from typing import Optional, List, Any
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.database.models.subject import Subject
from app.database.models.section import Section
from app.database.models.moduls import Moduls
from app.database.models.topic import Topic
from app.database.models.topic import Question

def add_question_db(topic_id: int, text: str, classification: Optional[str] = None) -> Question:
    with next(get_db()) as db:
        if not db.query(Topic).get(topic_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Topic id={topic_id} not found")
        q = Question(topic_id=topic_id, text=text, classification=classification)
        db.add(q)
        db.commit()
        db.refresh(q)
        return q


def get_question_db(question_id: int) -> Question:
    with next(get_db()) as db:
        q = db.query(Question).get(question_id)
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Question id={question_id} not found")
        return q


def update_question_db(question_id: int, text: Optional[str] = None,
                       classification: Optional[str] = None) -> Question:
    with next(get_db()) as db:
        q = db.query(Question).get(question_id)
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Question id={question_id} not found")
        if text is not None:
            q.text = text
        if classification is not None:
            q.classification = classification
        db.commit()
        db.refresh(q)
        return q


def delete_question_db(question_id: int) -> dict:
    with next(get_db()) as db:
        q = db.query(Question).get(question_id)
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Question id={question_id} not found")
        db.delete(q)
        db.commit()
        return {"message": "Question deleted"}

# Grade services



# Comment services



# Attendance services

