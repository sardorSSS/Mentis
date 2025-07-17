from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.academic import Subject

def add_subject_db(name: str, description: str = None) -> Subject:
    with next(get_db()) as db:
        new_subject = Subject(name=name, description=description)
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
        return new_subject

def delete_subject_db(subject_id: int) -> dict:
    with next(get_db()) as db:
        subj = db.query(Subject).filter_by(subject_id=subject_id).first()
        if not subj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Предмет не найден")
        db.delete(subj)
        db.commit()
        return {"status": "Удалён"}

def find_subject_db(subject_id: int) -> Subject:
    with next(get_db()) as db:
        subj = db.query(Subject).filter_by(subject_id=subject_id).first()
        if not subj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Предмет не найден")
        return subj

