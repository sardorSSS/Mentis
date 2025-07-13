from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.database.models.subject import Subject


def add_subject_db(name: str, description: Optional[str] = None) -> Subject:
    try:
        with next(get_db()) as db:
            exists = db.query(Subject).filter(Subject.name == name).first()
            if exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Subject с именем '{name}' уже существует"
                )

            subject = Subject(name=name, description=description)
            db.add(subject)
            db.commit()
            db.refresh(subject)
            return subject

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}"
        )


def delete_subject_db(subject_id: int) -> dict:
    try:
        with next(get_db()) as db:
            subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()
            if not subject:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Subject с ID={subject_id} не найден"
                )

            db.delete(subject)
            db.commit()
            return {"message": "Subject успешно удалён"}

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}"
        )

def update_subject_db(subject_id: int,
            name: Optional[str] = None,
            description: Optional[str] = None ) -> Subject:
    try:
        with next(get_db()) as db:
            subject = db.query(Subject).filter(Subject.subject_id == subject_id).first()
            if not subject:
                raise HTTPException( status_code=status.HTTP_404_NOT_FOUND,
                                     detail=f"Subject с ID={subject_id} не найден")

            if name is not None:
                subject.name = name
            if description is not None:
                subject.description = description

            db.commit()
            db.refresh(subject)
            return subject

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {e}")

def get_subject_db(subject_id: int) -> Subject:
    with next(get_db()) as db:
        subject = db.query(Subject).get(subject_id)
        if not subject:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Subject with id={subject_id} not found")
        return subject
