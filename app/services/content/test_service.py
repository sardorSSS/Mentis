from sqlalchemy import func
from typing import List, Dict
from app.database.models.assesment import Question
from app.database.models.academic import Topic, Block, Section, Subject
from app.database.models.academic import Moduls
from app.database import get_db


# === ФУНКЦИИ ДЛЯ РАБОТЫ С ВОПРОСАМИ ===

def get_random_questions_by_topic(topic_id: int, limit: int = 30) -> List[Question]:
    """
    Получить случайные вопросы по определенной теме

    Args:
        topic_id: ID темы
        limit: количество вопросов (по умолчанию 30)

    Returns:
        List[Question]: список случайных вопросов
    """
    with next(get_db()) as db:
        questions = (
            db.query(Question)
            .filter(Question.topic_id == topic_id)
            .order_by(func.rand())
            .limit(limit)
            .all()
        )
        return questions


def get_random_questions_by_block(block_id: int, limit: int = 30) -> List[Question]:
    """
    Получить случайные вопросы по определенному блоку

    Args:
        block_id: ID блока
        limit: количество вопросов (по умолчанию 30)

    Returns:
        List[Question]: список случайных вопросов
    """
    with next(get_db()) as db:
        questions = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .filter(Topic.block_id == block_id)
            .order_by(func.rand())
            .limit(limit)
            .all()
        )
        return questions


def get_random_questions_by_modul(modul_id: int, limit_per_subject: int = 30) -> Dict[str, List[Question]]:
    """
    Получить случайные вопросы по модулю (по 30 на химию и биологию)

    Args:
        modul_id: ID модуля
        limit_per_subject: количество вопросов на каждый предмет (по умолчанию 30)

    Returns:
        Dict[str, List[Question]]: словарь с вопросами по химии и биологии
    """
    with next(get_db()) as db:
        # Получаем информацию о модуле
        modul = db.query(Moduls).filter(Moduls.modul_id == modul_id).first()
        if not modul:
            return {"chemistry": [], "biology": []}

        # Получаем вопросы по химии
        chemistry_questions = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .join(Block, Topic.block_id == Block.block_id)
            .join(Section, Block.section_id == Section.section_id)
            .join(Subject, Section.subject_id == Subject.subject_id)
            .filter(
                Subject.name.ilike('%химия%'),  # или используйте конкретный subject_id
                Topic.topic_id >= modul.start_topic_chem,
                Topic.topic_id <= modul.end_topic_chem
            )
            .order_by(func.rand())
            .limit(limit_per_subject)
            .all()
        )

        # Получаем вопросы по биологии
        biology_questions = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .join(Block, Topic.block_id == Block.block_id)
            .join(Section, Block.section_id == Section.section_id)
            .join(Subject, Section.subject_id == Subject.subject_id)
            .filter(
                Subject.name.ilike('%биология%'),  # или используйте конкретный subject_id
                Topic.topic_id >= modul.start_topic_bio,
                Topic.topic_id <= modul.end_topic_bio
            )
            .order_by(func.rand())
            .limit(limit_per_subject)
            .all()
        )

        return {
            "chemistry": chemistry_questions,
            "biology": biology_questions
        }


def get_random_questions_by_section(section_id: int, limit: int = 30) -> List[Question]:
    """
    Получить случайные вопросы по определенному разделу

    Args:
        section_id: ID раздела
        limit: количество вопросов (по умолчанию 30)

    Returns:
        List[Question]: список случайных вопросов
    """
    with next(get_db()) as db:
        questions = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .join(Block, Topic.block_id == Block.block_id)
            .filter(Block.section_id == section_id)
            .order_by(func.rand())
            .limit(limit)
            .all()
        )
        return questions


def get_random_questions_by_subject(subject_id: int, limit: int = 30) -> List[Question]:
    """
    Получить случайные вопросы по определенному предмету

    Args:
        subject_id: ID предмета
        limit: количество вопросов (по умолчанию 30)

    Returns:
        List[Question]: список случайных вопросов
    """
    with next(get_db()) as db:
        questions = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .join(Block, Topic.block_id == Block.block_id)
            .join(Section, Block.section_id == Section.section_id)
            .filter(Section.subject_id == subject_id)
            .order_by(func.rand())
            .limit(limit)
            .all()
        )
        return questions


def get_questions_count_by_topic(topic_id: int) -> int:
    """
    Получить количество вопросов по теме

    Args:
        topic_id: ID темы

    Returns:
        int: количество вопросов
    """
    with next(get_db()) as db:
        count = db.query(Question).filter(Question.topic_id == topic_id).count()
        return count


def get_questions_count_by_block(block_id: int) -> int:
    """
    Получить количество вопросов по блоку

    Args:
        block_id: ID блока

    Returns:
        int: количество вопросов
    """
    with next(get_db()) as db:
        count = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .filter(Topic.block_id == block_id)
            .count()
        )
        return count


def get_questions_count_by_section(section_id: int) -> int:
    """
    Получить количество вопросов по разделу

    Args:
        section_id: ID раздела

    Returns:
        int: количество вопросов
    """
    with next(get_db()) as db:
        count = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .join(Block, Topic.block_id == Block.block_id)
            .filter(Block.section_id == section_id)
            .count()
        )
        return count


def get_questions_count_by_subject(subject_id: int) -> int:
    """
    Получить количество вопросов по предмету

    Args:
        subject_id: ID предмета

    Returns:
        int: количество вопросов
    """
    with next(get_db()) as db:
        count = (
            db.query(Question)
            .join(Topic, Question.topic_id == Topic.topic_id)
            .join(Block, Topic.block_id == Block.block_id)
            .join(Section, Block.section_id == Section.section_id)
            .filter(Section.subject_id == subject_id)
            .count()
        )
        return count

# === ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ STUDENT SKILL ===
