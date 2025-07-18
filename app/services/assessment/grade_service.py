from app.database import get_db
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import func
from app.database.models.assesment import



def add_dtm_exam_db(student_id: int, subject_id: int, common_score: float,
    second_subject_score: float, first_subject_score: float,
                    total_score: float ,exam_date: Optional[datetime] = None) -> DtmExam:
    with next(get_db()) as db:
        new_exam = DtmExam(student_id=student_id,subject_id=subject_id,common_score=common_score,
                           second_subject_score=second_subject_score,first_subject_score=first_subject_score,
                           exam_date=exam_date, total_score= total_score)
        db.add(new_exam)
        db.commit()
        db.refresh(new_exam)
        return new_exam

# -----------------------
# DELETE DTM EXAM
# -----------------------
def delete_dtm_exam_db(exam_id: int, student_id: int,subject_id: int) -> dict:
    with next(get_db()) as db:
        exam = (db.query(DtmExam).filter_by(exam_id=exam_id,student_id=student_id,
                  subject_id=subject_id).first())
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Экзамен id={exam_id} для студента {student_id} по предмету {subject_id} не найден")
        db.delete(exam)
        db.commit()
        return {"status": "Удалён"}

# -----------------------
# EDIT DTM EXAM SCORES & DATE
# -----------------------
def edit_dtm_exam_db(exam_id: int,student_id: int,subject_id: int, common_score: Optional[float] = None,
    second_subject_score: Optional[float] = None, total_score :Optional[float] = None,
                     first_subject_score: Optional[float] = None, exam_date: Optional[datetime] = None) -> DtmExam:
    with next(get_db()) as db:
        exam = (db.query(DtmExam).filter_by(exam_id=exam_id,student_id=student_id,
                  subject_id=subject_id).first())
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Экзамен id={exam_id} для студента {student_id} по предмету {subject_id} не найден")
        if common_score is not None:
            exam.common_score = common_score
        if second_subject_score is not None:
            exam.second_subject_score = second_subject_score
        if first_subject_score is not None:
            exam.first_subject_score = first_subject_score
        if exam_date is not None:
            exam.exam_date = exam_date
        if total_score is not None:
            exam.total_score = total_score

        db.commit()
        db.refresh(exam)
        return exam



def get_common_score_by_student_and_date(student_id: int, exam_date: datetime) -> float:
    """
    Возвращает common_score для заданного студента на конкретную дату.
    """
    with next(get_db()) as db:
        exam: Optional[DtmExam] = (db.query(DtmExam).filter(DtmExam.student_id == student_id,
                                                            DtmExam.exam_date == exam_date).first())
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail=f"DtmExam not found for student_id={student_id} on {exam_date}")
        return exam.common_score

def get_second_subject_score_by_student_and_date(student_id: int, exam_date: datetime) -> float:
    """
    Возвращает second_subject_score для заданного студента на конкретную дату.
    """
    with next(get_db()) as db:
        exam = (db.query(DtmExam).filter(DtmExam.student_id == student_id,
                DtmExam.exam_date == exam_date).first())
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"DtmExam not found for student_id={student_id} on {exam_date}"
            )
        return exam.second_subject_score

def get_first_subject_score_by_student_and_date(student_id: int, exam_date: datetime) -> float:
    """
    Возвращает first_subject_score для заданного студента на конкретную дату.
    """
    with next(get_db()) as db:
        exam = (db.query(DtmExam).filter(DtmExam.student_id == student_id,
                                         DtmExam.exam_date == exam_date).first())
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"DtmExam not found for student_id={student_id} on {exam_date}")
        return exam.first_subject_score

def get_total_score_by_student_and_date(student_id: int, exam_date: datetime) -> float:
    """
    Возвращает total_score для заданного студента на конкретную дату.
    """
    with next(get_db()) as db:
        exam = (db.query(DtmExam).filter(DtmExam.student_id == student_id,DtmExam.exam_date == exam_date)
            .first())
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"DtmExam not found for student_id={student_id} on {exam_date}")
        return exam.total_score

def get_all_total_scores_by_student(student_id: int) -> List[float]:
    """
    Возвращает список всех total_score для заданного студента,
    упорядоченный по дате экзамена.
    """
    with next(get_db()) as db:
        rows = (db.query(DtmExam.total_score).filter(DtmExam.student_id == student_id)
            .order_by(DtmExam.exam_date).all())
        return [r[0] for r in rows]

def get_average_total_score_for_student(student_id: int) -> float:
    """
    Возвращает средний total_score для заданного студента за всё время.
    """
    with next(get_db()) as db:
        avg_score = (db.query(func.avg(DtmExam.total_score)).filter(DtmExam.student_id == student_id).scalar())
        if avg_score is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No DtmExam records found for student_id={student_id}")
        return float(avg_score)

def find_section_exam_db(section_exam_id: int) -> SectionExam:
    """
    Находит SectionExam по его ID.
    """
    with next(get_db()) as db:
        exam = db.query(SectionExam).get(section_exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SectionExam id={section_exam_id} not found"
            )
        return exam


def add_section_exam_db(
    student_id: int,
    section_id: int,
    score: float,
    exam_date: datetime
) -> SectionExam:
    """
    Создаёт новую запись SectionExam.
    """
    with next(get_db()) as db:
        if not db.query(Student).get(student_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Student id={student_id} not found"
            )
        if not db.query(Section).get(section_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Section id={section_id} not found"
            )

        exam = SectionExam(
            student_id=student_id,
            section_id=section_id,
            score=score,
            exam_date=exam_date
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam


def delete_section_exam_db(section_exam_id: int) -> None:
    """
    Удаляет SectionExam по его ID.
    """
    with next(get_db()) as db:
        exam = db.query(SectionExam).get(section_exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SectionExam id={section_exam_id} not found"
            )
        db.delete(exam)
        db.commit()


def update_section_exam_db(
    section_exam_id: int,
    score: float | None = None,
    section_id: int | None = None,
    student_id: int | None = None,
    exam_date: datetime | None = None
) -> SectionExam:
    """
    Обновляет поля SectionExam по его ID.
    """
    with next(get_db()) as db:
        exam = db.query(SectionExam).get(section_exam_id)
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"SectionExam id={section_exam_id} not found"
            )

        if student_id is not None:
            if not db.query(Student).get(student_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Student id={student_id} not found"
                )
            exam.student_id = student_id

        if section_id is not None:
            if not db.query(Section).get(section_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Section id={section_id} not found"
                )
            exam.section_id = section_id

        if score is not None:
            exam.score = score

        if exam_date is not None:
            exam.exam_date = exam_date

        db.commit()
        db.refresh(exam)
        return exam


def get_section_exam_score_db(student_id: int, exam_date: datetime) -> float:
    """
    Возвращает score для заданного студента на конкретную дату.
    """
    with next(get_db()) as db:
        exam = (
            db.query(SectionExam)
            .filter(
                SectionExam.student_id == student_id,
                SectionExam.exam_date == exam_date
            )
            .first()
        )
        if not exam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No SectionExam for student_id={student_id} on {exam_date}"
            )
        return exam.score


def get_avg_score_by_student_subject_db(student_id: int, subject_id: int) -> float:
    """
    Средний score одного студента по предмету (через связь Section → Subject).
    """
    with next(get_db()) as db:
        avg_score = (
            db.query(func.avg(SectionExam.score))
            .join(SectionExam.section)      # relationship SectionExam.section
            .filter(
                SectionExam.student_id == student_id,
                Section.subject_id == subject_id
            )
            .scalar()
        )
        if avg_score is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No SectionExams for student_id={student_id}, subject_id={subject_id}"
            )
        return float(avg_score)


def get_avg_score_for_subject_db(subject_id: int) -> float:
    """
    Средний score по всем студентам для заданного предмета.
    """
    with next(get_db()) as db:
        avg_score = (
            db.query(func.avg(SectionExam.score))
            .join(SectionExam.section)
            .filter(Section.subject_id == subject_id)
            .scalar()
        )
        if avg_score is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No SectionExams for subject_id={subject_id}"
            )
        return float(avg_score)

from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from your_app.db import get_db
from your_app.models import BlockExam, Student, Block, Subject

def add_block_exam_db(
    student_id: int,
    block_id: int,
    subject_id: int,
    score: float,
    exam_date: datetime
) -> BlockExam:
    """
    Создаёт новую запись BlockExam для студента.
    """
    with next(get_db()) as db:
        if not db.query(Student).get(student_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Student id={student_id} not found")
        if not db.query(Block).get(block_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Block id={block_id} not found")
        if not db.query(Subject).get(subject_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Subject id={subject_id} not found")

        exam = BlockExam(
            student_id=student_id,
            block_id=block_id,
            subject_id=subject_id,
            score=score,
            exam_date=exam_date
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam

def delete_block_exam_db(block_exam_id: int) -> None:
    """
    Удаляет запись BlockExam по её ID.
    """
    with next(get_db()) as db:
        exam = db.query(BlockExam).get(block_exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"BlockExam id={block_exam_id} not found")
        db.delete(exam)
        db.commit()

def update_block_exam_db(
    block_exam_id: int,
    student_id: Optional[int] = None,
    block_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    score: Optional[float] = None,
    exam_date: Optional[datetime] = None
) -> BlockExam:
    """
    Обновляет поля BlockExam. Передавайте только нужные параметры.
    """
    with next(get_db()) as db:
        exam = db.query(BlockExam).get(block_exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"BlockExam id={block_exam_id} not found")

        if student_id is not None:
            if not db.query(Student).get(student_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Student id={student_id} not found")
            exam.student_id = student_id

        if block_id is not None:
            if not db.query(Block).get(block_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Block id={block_id} not found")
            exam.block_id = block_id

        if subject_id is not None:
            if not db.query(Subject).get(subject_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Subject id={subject_id} not found")
            exam.subject_id = subject_id

        if score is not None:
            exam.score = score

        if exam_date is not None:
            exam.exam_date = exam_date

        db.commit()
        db.refresh(exam)
        return exam

def get_all_block_scores_by_student_subject_db(
    student_id: int,
    subject_id: int
) -> List[float]:
    """
    Возвращает список всех score из BlockExam для данного студента и предмета.
    """
    with next(get_db()) as db:
        rows = (
            db.query(BlockExam.score)
            .filter(
                BlockExam.student_id == student_id,
                BlockExam.subject_id == subject_id
            )
            .order_by(BlockExam.exam_date)
            .all()
        )
        return [r[0] for r in rows]

def get_block_score_by_student_date_subject_db(
    student_id: int,
    subject_id: int,
    exam_date: datetime
) -> float:
    """
    Возвращает score из BlockExam для студента на конкретную дату и предмет.
    """
    with next(get_db()) as db:
        exam = (
            db.query(BlockExam)
            .filter_by(
                student_id=student_id,
                subject_id=subject_id,
                exam_date=exam_date
            )
            .first()
        )
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=(
                                    f"No BlockExam for "
                                    f"student_id={student_id}, "
                                    f"subject_id={subject_id} on {exam_date}"
                                ))
        return exam.score

def get_avg_block_score_by_student_subject_db(
    student_id: int,
    subject_id: int
) -> float:
    """
    Средний score BlockExam для данного студента и предмета.
    """
    with next(get_db()) as db:
        avg_score = (
            db.query(func.avg(BlockExam.score))
            .filter(
                BlockExam.student_id == student_id,
                BlockExam.subject_id == subject_id
            )
            .scalar()
        )
        if avg_score is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=(
                                    f"No BlockExams for "
                                    f"student_id={student_id}, "
                                    f"subject_id={subject_id}"
                                ))
        return float(avg_score)

def get_avg_block_score_for_subject_db(subject_id: int) -> Dict[int, float]:
    """
    Возвращает средний балл по BlockExam для каждого студента по заданному предмету.
    Результат — словарь {student_id: average_score, ...}.
    """
    with next(get_db()) as db:  # type: Session
        rows = (
            db.query(
                BlockExam.student_id,
                func.avg(BlockExam.score).label("avg_score")
            )
            .filter(BlockExam.subject_id == subject_id)
            .group_by(BlockExam.student_id)
            .all()
        )

        if not rows:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No BlockExam records found for subject_id={subject_id}"
            )

        # Преобразуем список кортежей в словарь
        return {student_id: float(avg_score) for student_id, avg_score in rows}

from datetime import datetime
from typing import Dict
from sqlalchemy import func
from fastapi import HTTPException, status

from .database import get_db
from .models import ModulExam, Moduls, Student

def add_modul_exam_db(
    modul_id: int,
    student_id: int,
    chem_score: float,
    bio_score: float,
    exam_date: datetime
) -> ModulExam:
    """Добавление новой записи ModulExam."""
    with next(get_db()) as db:
        # Проверяем существование связанных записей
        if not db.query(Moduls).get(modul_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Modul id={modul_id} not found")
        if not db.query(Student).get(student_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Student id={student_id} not found")

        exam = ModulExam(
            modul_id=modul_id,
            student_id=student_id,
            chem_score=chem_score,
            bio_score=bio_score,
            exam_date=exam_date
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam

def delete_modul_exam_db(modul_exam_id: int) -> None:
    """Удаление записи ModulExam по его ID."""
    with next(get_db()) as db:
        exam = db.query(ModulExam).get(modul_exam_id)
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"ModulExam id={modul_exam_id} not found")
        db.delete(exam)
        db.commit()

def update_chem_score_db(
    student_id: int,
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime,
    new_chem_score: float
) -> ModulExam:
    """Изменение chem_score по заданным критериям."""
    with next(get_db()) as db:
        exam = (
            db.query(ModulExam)
            .filter_by(
                modul_exam_id=modul_exam_id,
                student_id=student_id,
                modul_id=modul_id,
                exam_date=exam_date
            )
            .first()
        )
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ModulExam not found for update chem_score")
        exam.chem_score = new_chem_score
        db.commit()
        db.refresh(exam)
        return exam

def update_bio_score_db(
    student_id: int,
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime,
    new_bio_score: float
) -> ModulExam:
    """Изменение bio_score по заданным критериям."""
    with next(get_db()) as db:
        exam = (
            db.query(ModulExam)
            .filter_by(
                modul_exam_id=modul_exam_id,
                student_id=student_id,
                modul_id=modul_id,
                exam_date=exam_date
            )
            .first()
        )
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="ModulExam not found for update bio_score")
        exam.bio_score = new_bio_score
        db.commit()
        db.refresh(exam)
        return exam

def get_chem_score_db(
    student_id: int,
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime
) -> float:
    """Получение chem_score по заданным критериям."""
    with next(get_db()) as db:
        exam = (
            db.query(ModulExam.chem_score)
            .filter_by(
                modul_exam_id=modul_exam_id,
                student_id=student_id,
                modul_id=modul_id,
                exam_date=exam_date
            )
            .scalar()
        )
        if exam is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="chem_score not found")
        return exam

def get_bio_score_db(
    student_id: int,
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime
) -> float:
    """Получение bio_score по заданным критериям."""
    with next(get_db()) as db:
        score = (
            db.query(ModulExam.bio_score)
            .filter_by(
                modul_exam_id=modul_exam_id,
                student_id=student_id,
                modul_id=modul_id,
                exam_date=exam_date
            )
            .scalar()
        )
        if score is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="bio_score not found")
        return score

def get_scores_db(
    student_id: int,
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime
) -> Dict[str, float]:
    """Получение сразу chem_score и bio_score по заданным критериям."""
    with next(get_db()) as db:
        exam = (
            db.query(ModulExam.chem_score, ModulExam.bio_score)
            .filter_by(
                modul_exam_id=modul_exam_id,
                student_id=student_id,
                modul_id=modul_id,
                exam_date=exam_date
            )
            .first()
        )
        if not exam:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Scores not found")
        chem, bio = exam
        return {"chem_score": chem, "bio_score": bio}

def get_avg_bio_score_for_student_db(student_id: int) -> float:
    """Средний bio_score по всем экзаменам одного студента."""
    with next(get_db()) as db:
        avg_bio = (
            db.query(func.avg(ModulExam.bio_score))
            .filter(ModulExam.student_id == student_id)
            .scalar()
        )
        return avg_bio or 0.0

def get_avg_chem_score_for_student_db(student_id: int) -> float:
    """Средний chem_score по всем экзаменам одного студента."""
    with next(get_db()) as db:
        avg_chem = (
            db.query(func.avg(ModulExam.chem_score))
            .filter(ModulExam.student_id == student_id)
            .scalar()
        )
        return avg_chem or 0.0

def get_all_chem_scores_db(
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime
) -> Dict[int, float]:
    """
    Словарь {student_id: chem_score} для всех студентов
    по заданному modul_id, modul_exam_id и exam_date.
    """
    with next(get_db()) as db:
        rows = (
            db.query(ModulExam.student_id, ModulExam.chem_score)
            .filter_by(
                modul_id=modul_id,
                modul_exam_id=modul_exam_id,
                exam_date=exam_date
            )
            .all()
        )
        return {sid: score for sid, score in rows}

def get_all_bio_scores_db(
    modul_id: int,
    modul_exam_id: int,
    exam_date: datetime
) -> Dict[int, float]:
    """
    Словарь {student_id: bio_score} для всех студентов
    по заданному modul_id, modul_exam_id и exam_date.
    """
    with next(get_db()) as db:
        rows = (
            db.query(ModulExam.student_id, ModulExam.bio_score)
            .filter_by(
                modul_id=modul_id,
                modul_exam_id=modul_exam_id,
                exam_date=exam_date
            )
            .all()
        )
        return {sid: score for sid, score in rows}
from datetime import datetime
from typing import Dict, List
from sqlalchemy import func
from fastapi import HTTPException, status

from .database import get_db
from .models import TopicTest, Student, Topic

def add_topic_test_db(
    student_id: int,
    topic_id: int,
    score: float,
    attempt_date: datetime
) -> TopicTest:
    """Добавление новой записи TopicTest."""
    with next(get_db()) as db:
        if not db.query(Student).get(student_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Student id={student_id} not found")
        if not db.query(Topic).get(topic_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Topic id={topic_id} not found")
        tt = TopicTest(
            student_id=student_id,
            topic_id=topic_id,
            score=score,
            attempt_date=attempt_date
        )
        db.add(tt)
        db.commit()
        db.refresh(tt)
        return tt

def update_topic_test_score_db(
    student_id: int,
    topic_id: int,
    topic_test_id: int,
    new_score: float
) -> TopicTest:
    """Изменение score в TopicTest."""
    with next(get_db()) as db:
        tt = (
            db.query(TopicTest)
            .filter_by(
                topic_test_id=topic_test_id,
                student_id=student_id,
                topic_id=topic_id
            )
            .first()
        )
        if not tt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="TopicTest not found for update")
        tt.score = new_score
        db.commit()
        db.refresh(tt)
        return tt

def delete_topic_test_db(topic_test_id: int) -> None:
    """Удаление TopicTest по его ID."""
    with next(get_db()) as db:
        tt = db.query(TopicTest).get(topic_test_id)
        if not tt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"TopicTest id={topic_test_id} not found")
        db.delete(tt)
        db.commit()

def get_topic_test_score_db(
    student_id: int,
    topic_id: int,
    topic_test_id: int
) -> float:
    """Получение score одной записи TopicTest."""
    with next(get_db()) as db:
        score = (
            db.query(TopicTest.score)
            .filter_by(
                topic_test_id=topic_test_id,
                student_id=student_id,
                topic_id=topic_id
            )
            .scalar()
        )
        if score is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Score not found")
        return score

def get_all_topic_scores_by_topic_db(topic_id: int) -> Dict[int, float]:
    """Все score всех студентов по заданному topic_id."""
    with next(get_db()) as db:
        rows = (
            db.query(TopicTest.student_id, TopicTest.score)
            .filter(TopicTest.topic_id == topic_id)
            .all()
        )
        return {sid: sc for sid, sc in rows}

def get_avg_topic_score_for_student_db(
    student_id: int,
    topic_id: int
) -> float:
    """Средний score TopicTest одного студента по заданному topic_id."""
    with next(get_db()) as db:
        avg = (
            db.query(func.avg(TopicTest.score))
            .filter(
                TopicTest.student_id == student_id,
                TopicTest.topic_id == topic_id
            )
            .scalar()
        )
        return avg or 0.0
from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .database import get_db
from .models import CurrentRating, Topic


def add_current_rating_db(
    student_id: int,
    subject_id: int,
    topic_id: int,
    current_score: float,
    second_current_score: float
) -> CurrentRating:
    """
    Добавление новой записи CurrentRating.
    """
    with next(get_db()) as db:
        # Проверка на существование topic (необязательно, но рекомендуется)
        if not db.query(Topic).get(topic_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic id={topic_id} not found"
            )
        rating = CurrentRating(
            student_id=student_id,
            subject_id=subject_id,
            topic_id=topic_id,
            current_score=current_score,
            second_current_score=second_current_score,
            last_updated=datetime.utcnow()
        )
        db.add(rating)
        db.commit()
        db.refresh(rating)
        return rating


def delete_current_rating_db(rating_id: int) -> None:
    """
    Удаление записи CurrentRating по её ID.
    """
    with next(get_db()) as db:
        rating = db.query(CurrentRating).filter_by(rating_id=rating_id).first()
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CurrentRating id={rating_id} not found"
            )
        db.delete(rating)
        db.commit()


def update_current_rating_db(
    rating_id: int,
    current_score: float | None = None,
    second_current_score: float | None = None
) -> CurrentRating:
    """
    Обновление полей current_score и/или second_current_score.
    """
    with next(get_db()) as db:
        rating = db.query(CurrentRating).filter_by(rating_id=rating_id).first()
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"CurrentRating id={rating_id} not found"
            )
        if current_score is not None:
            rating.current_score = current_score
        if second_current_score is not None:
            rating.second_current_score = second_current_score
        rating.last_updated = datetime.utcnow()
        db.commit()
        db.refresh(rating)
        return rating


def get_current_score_db(
    student_id: int,
    subject_id: int,
    topic_id: int
) -> float:
    """
    Получение current_score по трём ключам.
    """
    with next(get_db()) as db:
        rating = db.query(CurrentRating).filter_by(
            student_id=student_id,
            subject_id=subject_id,
            topic_id=topic_id
        ).first()
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CurrentRating not found"
            )
        return rating.current_score


def get_second_current_score_db(
    student_id: int,
    subject_id: int,
    topic_id: int
) -> float:
    """
    Получение second_current_score по трём ключам.
    """
    with next(get_db()) as db:
        rating = db.query(CurrentRating).filter_by(
            student_id=student_id,
            subject_id=subject_id,
            topic_id=topic_id
        ).first()
        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CurrentRating not found"
            )
        return rating.second_current_score


def get_avg_sum_scores_by_block_for_student_db(
        student_id: int,
        block_id: int
) -> float:
    """
    Среднее значение суммы (current_score + second_current_score)
    для всех тем одного блока у заданного студента.
    """
    with next(get_db()) as db:
        avg_sum = db.query(
            func.avg(
                func.coalesce(CurrentRating.current_score, 0) +
                func.coalesce(CurrentRating.second_current_score, 0)
            )
        ).join(
            Topic, CurrentRating.topic_id == Topic.topic_id
        ).filter(
            CurrentRating.student_id == student_id,
            Topic.block_id == block_id
        ).scalar()

        return float(avg_sum) if avg_sum is not None else 0.0


def get_avg_current_rating_for_block_db(block_id: int) -> dict[int, float]:
    with next(get_db()) as db:
        # 1. Убедимся, что блок существует и найдём subject_id через Section → Subject
        block = db.query(Block).filter_by(block_id=block_id).first()
        if not block:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Block with id={block_id} not found"
            )
        subject_id = block.section.subject_id

        # 2. Построим запрос: соединяем с Topic, фильтруем по block_id и subject_id,
        #    группируем по student_id и берём среднее суммы двух полей.
        rows = (
            db.query(
                CurrentRating.student_id,
                func.avg(
                    CurrentRating.current_score +
                    CurrentRating.second_current_score
                ).label("avg_score")
            )
            .join(CurrentRating.topic)  # связываем с Topic
            .filter(
                Topic.block_id == block_id,
                CurrentRating.subject_id == subject_id
            )
            .group_by(CurrentRating.student_id)
            .all()
        )

        # 3. Собираем результат в словарь
        return {student_id: avg_score for student_id, avg_score in rows}

