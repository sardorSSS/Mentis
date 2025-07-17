from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.academic import Topic

def add_topic_db(block_id: int,name: str,homework: str = None,number: int = None,
    additional_material: str = None) -> Topic:
    with next(get_db()) as db:
        new_topic = Topic(block_id=block_id,name=name,homework=homework,number=number,
            additional_material=additional_material)
        db.add(new_topic)
        db.commit()
        db.refresh(new_topic)
        return new_topic

def delete_topic_db(topic_id: int) -> dict:
    with next(get_db()) as db:
        top = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not top:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Тема не найдена")
        db.delete(top)
        db.commit()
        return {"status": "Удалена"}

def find_topic_db(topic_id: int) -> Topic:
    with next(get_db()) as db:
        top = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not top:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Тема не найдена")
        return top

def edit_topic_db(topic_id: int,block_id: int = None,name: str = None,
    homework: str = None,number: int = None, additional_material: str = None) -> Topic:
    with next(get_db()) as db:
        top = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not top:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Тема не найдена")
        if block_id is not None:
            top.block_id = block_id
        if name is not None:
            top.name = name
        if homework is not None:
            top.homework = homework
        if number is not None:
            top.number = number
        if additional_material is not None:
            top.additional_material = additional_material
        db.commit()
        db.refresh(top)
        return top

def add_homework_db(topic_id: int, homework: str) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.homework = homework
        db.commit()
        db.refresh(topic)
        return topic

def delete_homework_db(topic_id: int) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.homework = None
        db.commit()
        db.refresh(topic)
        return topic

def edit_homework_db(topic_id: int, homework: str) -> Topic:
    # по сути то же, что и add_homework_db, но вынесено отдельно
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.homework = homework
        db.commit()
        db.refresh(topic)
        return topic

# -----------------------
# NUMBER
# -----------------------

def add_topic_number_db(topic_id: int, number: int) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.number = number
        db.commit()
        db.refresh(topic)
        return topic

def delete_topic_number_db(topic_id: int) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.number = None
        db.commit()
        db.refresh(topic)
        return topic

def edit_topic_number_db(topic_id: int, number: int) -> Topic:
    # аналогично add_number_db
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.number = number
        db.commit()
        db.refresh(topic)
        return topic

# -----------------------
# ADDITIONAL MATERIAL
# -----------------------

def add_additional_material_db(topic_id: int, additional_material: str) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена")
        topic.additional_material = additional_material
        db.commit()
        db.refresh(topic)
        return topic

def delete_additional_material_db(topic_id: int) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.additional_material = None
        db.commit()
        db.refresh(topic)
        return topic

def edit_additional_material_db(topic_id: int, additional_material: str) -> Topic:
    # аналогично add_additional_material_db
    with next(get_db()) as db:
        topic = db.query(Topic).filter_by(topic_id=topic_id).first()
        if not topic:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Тема не найдена"
            )
        topic.additional_material = additional_material
        db.commit()
        db.refresh(topic)
        return topic
