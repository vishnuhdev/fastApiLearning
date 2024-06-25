from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, session
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

BASE_URL = 'postgresql://postgres:1234@192.168.5.57:5432/user-data'


def db_init() -> None:
    global BASE_URL
    global Base

    engine = create_engine(BASE_URL, pool_size=5, max_overflow=0)
    Base.metadata.create_all(engine)


def get_db() -> session:
    global BASE_URL

    local_session = sessionmaker(bind=create_engine(BASE_URL))
    db = local_session()
    try:
        yield db
    finally:
        db.close()
