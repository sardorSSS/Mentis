from fastapi import HTTPException, status
from app.database import get_db
from app.database.models.assesment import Question

def add_question_db(topic_id: int, text: str,correct_answer: int,answer_1: str = None, answer_2: str = None,
    answer_3: str = None, answer_4: str = None, explanation: str = None) -> Question:
    with next(get_db()) as db:
        new_q = Question(topic_id=topic_id, text=text, answer_1=answer_1, answer_2=answer_2, answer_3=answer_3,
            answer_4=answer_4, correct_answer=correct_answer, explanation=explanation)
        db.add(new_q)
        db.commit()
        db.refresh(new_q)
        return new_q

def delete_question_db(question_id: int) -> dict:
    with next(get_db()) as db:
        q = db.query(Question).filter_by(question_id=question_id).first()
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Вопрос не найден")
        db.delete(q)
        db.commit()
        return {"status": "Удалён"}

def find_question_db(question_id: int) -> Question:
    with next(get_db()) as db:
        q = db.query(Question).filter_by(question_id=question_id).first()
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Вопрос не найден")
        return q

def edit_question_db( question_id: int, topic_id: int = None, text: str = None, correct_answer: int = None,
    answer_1: str = None, answer_2: str = None, answer_3: str = None, answer_4: str = None,
    explanation: str = None) -> Question:
    with next(get_db()) as db:
        q = db.query(Question).filter_by(question_id=question_id).first()
        if not q:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Вопрос не найден")
        if topic_id is not None:
            q.topic_id = topic_id
        if text is not None:
            q.text = text
        if correct_answer is not None:
            q.correct_answer = correct_answer
        if answer_1 is not None:
            q.answer_1 = answer_1
        if answer_2 is not None:
            q.answer_2 = answer_2
        if answer_3 is not None:
            q.answer_3 = answer_3
        if answer_4 is not None:
            q.answer_4 = answer_4
        if explanation is not None:
            q.explanation = explanation
        db.commit()
        db.refresh(q)
        return q

