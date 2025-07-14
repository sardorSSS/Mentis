from typing import Optional, List, Any
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from app.database import get_db
from app.database.models.subject import Subject
from app.database.models.section import Section
from app.database.models.moduls import Moduls
from app.database.models.topic import Topic
from app.database.models.topic import Question

def add_module_db(section_id: int, name: str) -> Moduls:
    with next(get_db()) as db:
        if not db.query(Section).get(section_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Section id={section_id} not found")
        mod = Moduls(section_id=section_id, name=name)
        db.add(mod)
        db.commit()
        db.refresh(mod)
        return mod


def update_module_db(module_id: int, name: Optional[str] = None) -> Moduls:
    with next(get_db()) as db:
        mod = db.query(Moduls).get(module_id)
        if not mod:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Module id={module_id} not found")
        if name is not None:
            mod.name = name
        db.commit()
        db.refresh(mod)
        return mod


def delete_module_db(module_id: int) -> dict:
    with next(get_db()) as db:
        mod = db.query(Moduls).get(module_id)
        if not mod:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Module id={module_id} not found")
        db.delete(mod)
        db.commit()
        return {"message": "Module deleted"}
