from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.moduls import Moduls
from app.database.models.topic import Topic


def add_topic_db(module_id: int, title: str) -> Topic:
    with next(get_db()) as db:
        if not db.query(Moduls).get(module_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Module id={module_id} not found")
        topic = Topic(module_id=module_id, title=title)
        db.add(topic)
        db.commit()
        db.refresh(topic)
        return topic


def get_topic_db(topic_id: int) -> Topic:
    with next(get_db()) as db:
        topic = db.query(Topic).get(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Topic id={topic_id} not found")
        return topic


def delete_topic_db(topic_id: int) -> dict:
    with next(get_db()) as db:
        topic = db.query(Topic).get(topic_id)
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Topic id={topic_id} not found")
        db.delete(topic)
        db.commit()
        return {"message": "Topic deleted"}
