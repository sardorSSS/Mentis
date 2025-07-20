from typing import List, Optional, Union, Dict
import json
from app.database.models.assesment import  DtmExam, SectionExam, BlockExam, ModulExam
from app.database.models.user import StudentSkill
from app.database import get_db

def _add_arrays(existing_array: List[int], new_array: List[int]) -> List[int]:
    """
    Складывает два массива поэлементно

    Args:
        existing_array: существующий массив (например, [12, 60, 29, 12, 43, 23, 34, 53])
        new_array: новый массив (например, [1, 0, 0, 1, 0, 0, 1, 1])

    Returns:
        List[int]: результирующий массив
    """
    # Определяем максимальную длину массива
    max_length = max(len(existing_array), len(new_array))

    # Дополняем массивы нулями до одинаковой длины
    existing_padded = existing_array + [0] * (max_length - len(existing_array))
    new_padded = new_array + [0] * (max_length - len(new_array))

    # Складываем поэлементно
    result = [existing_padded[i] + new_padded[i] for i in range(max_length)]

    return result


def _parse_json_array(json_data: Optional[Union[str, list]]) -> List[int]:
    """
    Парсит JSON данные в массив целых чисел

    Args:
        json_data: JSON строка, список или None

    Returns:
        List[int]: массив целых чисел
    """
    if not json_data:
        return []

    try:
        if isinstance(json_data, str):
            parsed_data = json.loads(json_data)
        else:
            parsed_data = json_data

        # Проверяем, что это список
        if isinstance(parsed_data, list):
            # Конвертируем все элементы в int
            return [int(x) for x in parsed_data]
        else:
            return []
    except (json.JSONDecodeError, ValueError, TypeError):
        return []


def _get_or_create_student_skill(student_id: int, db) -> StudentSkill:
    """
    Получает существующий StudentSkill или создает новый

    Args:
        student_id: ID студента
        db: сессия базы данных

    Returns:
        StudentSkill: объект навыков студента
    """
    student_skill = db.query(StudentSkill).filter(
        StudentSkill.student_id == student_id
    ).first()

    if not student_skill:
        student_skill = StudentSkill(
            student_id=student_id,
            correct=[],
            mistakes=[]
        )
        db.add(student_skill)
        db.flush()  # Получаем ID без коммита

    return student_skill


# === ОСНОВНЫЕ ФУНКЦИИ ДЛЯ STUDENT SKILL ===

def update_student_skill_from_dtm_exam(dtm_exam: DtmExam) -> StudentSkill:
    """
    Обновляет навыки студента на основе DTM экзамена

    Args:
        dtm_exam: объект DTM экзамена

    Returns:
        StudentSkill: обновленный объект навыков студента
    """
    with next(get_db()) as db:
        # Получаем или создаем StudentSkill
        student_skill = _get_or_create_student_skill(dtm_exam.student_id, db)

        # Получаем текущие значения correct и mistakes
        current_correct = _parse_json_array(student_skill.correct) if student_skill.correct else []
        current_mistakes = _parse_json_array(student_skill.mistakes) if student_skill.mistakes else []

        # Получаем данные из экзамена
        exam_correct = _parse_json_array(dtm_exam.category_correct) if dtm_exam.category_correct else []
        exam_mistakes = _parse_json_array(dtm_exam.category_mistake) if dtm_exam.category_mistake else []

        # Складываем массивы
        new_correct = _add_arrays(current_correct, exam_correct)
        new_mistakes = _add_arrays(current_mistakes, exam_mistakes)

        # Обновляем StudentSkill
        student_skill.correct = new_correct
        student_skill.mistakes = new_mistakes

        # Сохраняем изменения
        db.commit()
        db.refresh(student_skill)

        return student_skill


def update_student_skill_from_section_exam(section_exam: SectionExam) -> StudentSkill:
    """
    Обновляет навыки студента на основе экзамена по разделу

    Args:
        section_exam: объект экзамена по разделу

    Returns:
        StudentSkill: обновленный объект навыков студента
    """
    with next(get_db()) as db:
        # Получаем или создаем StudentSkill
        student_skill = _get_or_create_student_skill(section_exam.student_id, db)

        # Получаем текущие значения correct и mistakes
        current_correct = _parse_json_array(student_skill.correct) if student_skill.correct else []
        current_mistakes = _parse_json_array(student_skill.mistakes) if student_skill.mistakes else []

        # Получаем данные из экзамена
        exam_correct = _parse_json_array(section_exam.category_correct) if section_exam.category_correct else []
        exam_mistakes = _parse_json_array(section_exam.category_mistake) if section_exam.category_mistake else []

        # Складываем массивы
        new_correct = _add_arrays(current_correct, exam_correct)
        new_mistakes = _add_arrays(current_mistakes, exam_mistakes)

        # Обновляем StudentSkill
        student_skill.correct = new_correct
        student_skill.mistakes = new_mistakes

        # Сохраняем изменения
        db.commit()
        db.refresh(student_skill)

        return student_skill


def update_student_skill_from_block_exam(block_exam: BlockExam) -> StudentSkill:
    """
    Обновляет навыки студента на основе экзамена по блоку

    Args:
        block_exam: объект экзамена по блоку

    Returns:
        StudentSkill: обновленный объект навыков студента
    """
    with next(get_db()) as db:
        # Получаем или создаем StudentSkill
        student_skill = _get_or_create_student_skill(block_exam.student_id, db)

        # Получаем текущие значения correct и mistakes
        current_correct = _parse_json_array(student_skill.correct) if student_skill.correct else []
        current_mistakes = _parse_json_array(student_skill.mistakes) if student_skill.mistakes else []

        # Получаем данные из экзамена
        exam_correct = _parse_json_array(block_exam.category_correct) if block_exam.category_correct else []
        exam_mistakes = _parse_json_array(block_exam.category_mistake) if block_exam.category_mistake else []

        # Складываем массивы
        new_correct = _add_arrays(current_correct, exam_correct)
        new_mistakes = _add_arrays(current_mistakes, exam_mistakes)

        # Обновляем StudentSkill
        student_skill.correct = new_correct
        student_skill.mistakes = new_mistakes

        # Сохраняем изменения
        db.commit()
        db.refresh(student_skill)

        return student_skill


def update_student_skill_from_modul_exam(modul_exam: ModulExam) -> StudentSkill:
    """
    Обновляет навыки студента на основе модульного экзамена

    Args:
        modul_exam: объект модульного экзамена

    Returns:
        StudentSkill: обновленный объект навыков студента
    """
    with next(get_db()) as db:
        # Получаем или создаем StudentSkill
        student_skill = _get_or_create_student_skill(modul_exam.student_id, db)

        # Получаем текущие значения correct и mistakes
        current_correct = _parse_json_array(student_skill.correct) if student_skill.correct else []
        current_mistakes = _parse_json_array(student_skill.mistakes) if student_skill.mistakes else []

        # Получаем данные из экзамена
        exam_correct = _parse_json_array(modul_exam.category_correct) if modul_exam.category_correct else []
        exam_mistakes = _parse_json_array(modul_exam.category_mistake) if modul_exam.category_mistake else []

        # Складываем массивы
        new_correct = _add_arrays(current_correct, exam_correct)
        new_mistakes = _add_arrays(current_mistakes, exam_mistakes)

        # Обновляем StudentSkill
        student_skill.correct = new_correct
        student_skill.mistakes = new_mistakes

        # Сохраняем изменения
        db.commit()
        db.refresh(student_skill)

        return student_skill


def get_student_skill(student_id: int) -> Optional[StudentSkill]:
    """
    Получает навыки студента по ID

    Args:
        student_id: ID студента

    Returns:
        Optional[StudentSkill]: объект навыков студента или None
    """
    with next(get_db()) as db:
        student_skill = db.query(StudentSkill).filter(
            StudentSkill.student_id == student_id
        ).first()
        return student_skill


def get_student_skill_stats(student_id: int) -> Dict[str, Union[int, float, List[int]]]:
    """
    Получает статистику навыков студента

    Args:
        student_id: ID студента

    Returns:
        Dict[str, Union[int, float, List[int]]]: статистика навыков
    """
    student_skill = get_student_skill(student_id)

    if not student_skill:
        return {
            "total_correct": 0,
            "total_mistakes": 0,
            "total_attempts": 0,
            "accuracy_percentage": 0,
            "categories_count": 0,
            "correct_by_category": [],
            "mistakes_by_category": []
        }

    correct_array = _parse_json_array(student_skill.correct)
    mistakes_array = _parse_json_array(student_skill.mistakes)

    total_correct = sum(correct_array)
    total_mistakes = sum(mistakes_array)
    total_attempts = total_correct + total_mistakes
    accuracy_percentage = (total_correct / total_attempts * 100) if total_attempts > 0 else 0

    return {
        "total_correct": total_correct,
        "total_mistakes": total_mistakes,
        "total_attempts": total_attempts,
        "accuracy_percentage": round(accuracy_percentage, 2),
        "categories_count": len(correct_array),
        "correct_by_category": correct_array,
        "mistakes_by_category": mistakes_array
    }

# === УНИВЕРСАЛЬНАЯ ФУНКЦИЯ ===


def update_student_skill_from_exam(student_id: int,
                                   exam: Union[DtmExam, SectionExam, BlockExam, ModulExam]) -> StudentSkill:
    with next(get_db()) as db:
        # Получаем или создаём запись StudentSkill
        skill = db.query(StudentSkill).filter_by(student_id=student_id).first()
        if not skill:
            skill = StudentSkill(
                student_id=student_id,
                # можно задать начальные значения при создании
            )
            db.add(skill)
            db.commit()
            db.refresh(skill)

    if isinstance(exam, DtmExam):
        return update_student_skill_from_dtm_exam(exam)
    elif isinstance(exam, SectionExam):
        return update_student_skill_from_section_exam(exam)
    elif isinstance(exam, BlockExam):
        return update_student_skill_from_block_exam(exam)
    elif isinstance(exam, ModulExam):
        return update_student_skill_from_modul_exam(exam)
    else:
        raise ValueError(f"Неподдерживаемый тип экзамена: {type(exam)}")


