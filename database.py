from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine("mysql+mysqldb://syed:syedfurqan@localhost:3306/mobile_accessories")
engine = create_engine("sqlite:///database.sqlite")

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextmanager
def get_db_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
