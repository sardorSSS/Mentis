from app.database import get_db
from app.database.models.parent import ParentInfo
from app.database.models.user import UserRole, User
from app.database.models.student import Student, StudentInfo
from app.database.models.admin import Admin,AdminInfo
from app.database.models.teacher import Teacher, TeacherInfo
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from app.hash_argon import *

def add_user_db(name, surname, phone, email, password, role, is_active, direction,
                student_status, photo, hobby,sex, address , birthday,
                employment, admin_number,admin_hobby, schedule, admin_status, teacher_schedule,
                teacher_status,teacher_employment,teacher_number,dop_info, profession, parent_phone):
    with next(get_db()) as db:
        user = db.query(User).filter(User.phone == phone).first()
        if user:
            return { "message": "Такой номер уже существует"}
        user = User( name = name, surname = surname, email =email,
                     password = password, role = role, is_active =is_active, photo = photo)
        if user.role == UserRole.STUDENT:
            student = Student(direction = direction, student_status =student_status,)
            student_info = StudentInfo(hobby = hobby, sex =sex ,
                                      address = address, birthday = birthday)
            db.add(student)
            db.add(student_info)
        if user.role == UserRole.ADMIN:
            admin = Admin(schedule = schedule, admin_status = admin_status)
            admin_info = AdminInfo(admin_number = admin_number,
                                   employment =employment, admin_hobby = admin_hobby)

            db.add(admin)
            db.add(admin_info)
        if user.role == UserRole.TEACHER:
            teacher = Teacher(teacher_schedule = teacher_schedule, teacher_status = teacher_status )
            teacher_info = TeacherInfo(teacher_employment= teacher_employment, teacher_number = teacher_number,
                                       dop_info = dop_info)
            db.add(teacher)
            db.add(teacher_info)
        if user.role == UserRole.PARENT:
            parent_info = ParentInfo(profession = profession, parent_phone =parent_phone)
            db.add(parent_info)
        db.add(user)
        db.commit()
        return user.user_id
def delete_user_db(user_id):
    with next(get_db()) as db:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="пользователь с таким айди не найден")
        if user:
            db.delete(user)
            db.commit()
        return {"status": "Удалён"}

def change_user_data(user_id : int,
                     name = None, surname = None, phone= None, email = None,
                     password = None, is_active = None):
    try:

       with next(get_db()) as db:
            user = db.query(User).filter_by(id = user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="пользователь  не найден")
            if  name  :
                user.name = name
            if   surname :
                user.surname = surname
            if  phone :
                user.phone = phone
            if  password :
                user.password = password
            if  is_active   :
                user.is_active = is_active
            if  email   :
                user.email = email
            db.commit()
            db.refresh(user)
            return True, 'Данные пользователя изменены'
    except SQLAlchemyError as e:
        db.rollback()
        return False , 'Ошибка в работе базы данных'


def user_block_db(user_id):
    try:
        with next(get_db()) as db:
            user = (db.query(User)
                .filter(User.user_id == user_id, User.is_active == True)
                .first())
            if not user:
                return False, f"Активный пользователь с ID {user_id} не найден или уже заблокирован."

            user.is_active = False
            db.commit()
            return True, f"Пользователь с ID {user_id} успешно заблокирован."

    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Ошибка базы данных: {e}"


def user_unblock_db(user_id):
    try:
        with next(get_db()) as db:
            user = (db.query(User).filter(User.user_id == user_id, User.is_active == False).first())
            if not user:
                return False, f"Заблокированный пользователь с ID {user_id} не найден или уже активен."
            user.is_active = True
            db.commit()
            return True, f"Пользователь с ID {user_id} успешно активирован."

    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Ошибка базы данных: {e}"

def add_only_user_db(name, surname, phone, email, password, role, photo):
    try:
        with next(get_db()) as db:
            user = db.query(User).filter(User.phone == phone).first()
            if user:
                return {"message": "Пользователь с таким номером уже существует"}
            user = User(name=name, surname=surname, email=email,
                        password=password, role=role, is_active=is_active, photo=photo)
            db.add(user)
            db.commit()
            return True, user.user_id
    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Ошибка базы данных: {e}"

def login_db(phone, password):
    with next(get_db()) as db:
        user = db.query(User).filter_by(phone = phone).first()
        if user:
            if not check_pw(password, user.password):
                return False
        return user.user_id

def get_user_info_db(user_id):
    try:
        with next(get_db()) as db:
            user = db.query(User).filter_by(user_id = user_id).first()
            if user:
                return {"message": "Пользователь с таким ID не найден"}

            return True, user.user_id
    except SQLAlchemyError as e:
        db.rollback()
        return False, f"Ошибка базы данных: {e}"














