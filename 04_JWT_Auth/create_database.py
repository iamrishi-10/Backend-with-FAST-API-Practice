import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ProgrammingError

load_dotenv()

NEW_DB_NAME = "fastapi_jwt_auth"

# Connect to the 'postgres' maintenance database to issue CREATE DATABASE -
# you cannot create a database while connected to it.
admin_url = make_url(os.environ["DATABASE_URL"]).set(database="postgres")
engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

with engine.connect() as conn:
    try:
        conn.execute(text(f'CREATE DATABASE "{NEW_DB_NAME}"'))
        print(f"Database '{NEW_DB_NAME}' created.")
    except ProgrammingError:
        print(f"Database '{NEW_DB_NAME}' already exists.")

engine.dispose()
