from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.academic import Moduls

def add_modul_db(start_topic_chem: int, start_topic_bio: int,end_topic_chem: int,
                 end_topic_bio: int) -> Moduls:
    with next(get_db()) as db:
        new_modul = Moduls(start_topic_chem=start_topic_chem,start_topic_bio=start_topic_bio,
                           end_topic_chem=end_topic_chem,end_topic_bio=end_topic_bio)
        db.add(new_modul)
        db.commit()
        db.refresh(new_modul)
        return new_modul

def delete_modul_db(modul_id: int) -> dict:
    with next(get_db()) as db:
        modul = db.query(Moduls).filter_by(modul_id=modul_id).first()
        if not modul:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Модуль не найден"
            )
        db.delete(modul)
        db.commit()
        return {"status": "Удалён"}

def find_modul_db(modul_id: int) -> Moduls:
    with next(get_db()) as db:
        modul = db.query(Moduls).filter_by(modul_id=modul_id).first()
        if not modul:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Модуль не найден")
        return modul

def edit_modul_db(modul_id: int, start_topic_chem: int = None,start_topic_bio: int = None,
                  end_topic_chem: int = None,end_topic_bio: int = None) -> Moduls:
    with next(get_db()) as db:
        modul = db.query(Moduls).filter_by(modul_id=modul_id).first()
        if not modul:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Модуль не найден")

        if start_topic_chem is not None:
            modul.start_topic_chem = start_topic_chem
        if start_topic_bio is not None:
            modul.start_topic_bio = start_topic_bio
        if end_topic_chem is not None:
            modul.end_topic_chem = end_topic_chem
        if end_topic_bio is not None:
            modul.end_topic_bio = end_topic_bio

        db.commit()
        db.refresh(modul)
        return modul

