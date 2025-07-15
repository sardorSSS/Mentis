from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.subject import Subject
from app.database.models.section import Section

def add_section_db(subject_id: int) -> Section:
    with next(get_db()) as db:
        if not db.query(Subject).get(subject_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Subject id={subject_id} not found")
        new_section = Section(subject_id=subject_id)
        db.add(new_section)
        db.commit()
        db.refrash()
        return new_section


def get_section_db(section_id: int) -> Section:
    with next(get_db()) as db:
        sec = db.query(Section).get(section_id)
        if not sec:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Section id={section_id} not found")
        return sec


def delete_section_db(section_id: int) -> dict:
    with next(get_db()) as db:
        sec = db.query(Section).get(section_id)
        if not sec:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Section id={section_id} not found")
        db.delete(sec)
        db.commit()
        return {"message": "Section deleted"}
