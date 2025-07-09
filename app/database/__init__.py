from sqlalchemy.engine import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#Формат базы данных и прописываем путь к базе данных

SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"

#Вариант с postgres
#SQLALCHEMY_DATABASE_URI = "postgresql://postgres:admin@localhost/quiz61"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

#создаём генератор сессий
Sessionlocal = sessionmaker(bind = engine)

Base = declarative_base()

#создаём функцию генератор сессий

def get_db():
    db = Sessionlocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()








