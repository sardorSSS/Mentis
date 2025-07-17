from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.academic import Section

def add_section_db(subject_id: int, name: str) -> Section:
    with next(get_db()) as db:
        new_section = Section(subject_id=subject_id, name=name)
        db.add(new_section)
        db.commit()
        db.refresh(new_section)
        return new_section

def delete_section_db(section_id: int) -> dict:
    with next(get_db()) as db:
        sec = db.query(Section).filter_by(section_id=section_id).first()
        if not sec:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Раздел не найден")
        db.delete(sec)
        db.commit()
        return {"status": "Удалён"}

def find_section_db(section_id: int) -> Section:
    with next(get_db()) as db:
        section = db.query(Section).filter_by(section_id=section_id).first()
        if not section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Раздел не найден")
        return section

def edit_section_db(section_id: int, subject_id: int = None, name: str = None) -> Section:
    with next(get_db()) as db:
        sec = db.query(Section).filter_by(section_id=section_id).first()
        if not sec:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Раздел не найден")
        if subject_id is not None:
            sec.subject_id = subject_id
        if name is not None:
            sec.name = name
        db.commit()
        db.refresh(sec)
        return sec

def get_section_name_db(section_id: int) -> Section:
    with next(get_db()) as db:
        section = db.query(Section).filter_by(section_id=section_id).first()
        if not section:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Раздел не найден")
        return section.name

def count_sections_by_subject_db(subject_id: int) -> int:
    with next(get_db()) as db:
        return db.query(Section).filter_by(subject_id=subject_id).count()
