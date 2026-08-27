import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DB_URL = os.environ['DATABASE_URL_1']

engine  = create_engine(DB_URL)

SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush=False)

class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


if __name__ == "__main__":
    # Test the database connection
    try:
        with engine.connect():
            print("Engine: okay")
    except Exception as e:
        print("Engine: no")
        print(e)

    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))
        session.close()
        print("Session: okay")
    except Exception as e:
        print("Session: no")
        print(e)
