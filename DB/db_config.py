from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os


load_dotenv()

DB_URL = os.getenv("DB_URL")

engine_options = {
    "pool_pre_ping": True,
    "pool_recycle": 1800,
    "pool_size": 5,
    "max_overflow": 10
}

engine = create_engine(DB_URL, echo=True, **engine_options)

def get_db():
    yield Session(engine)

def create_tables():
    SQLModel.metadata.create_all(engine)
