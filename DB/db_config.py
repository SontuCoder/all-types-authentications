from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os
import time


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
    with Session(engine) as session:
        yield session

def create_tables():
    start = time.perf_counter()

    print("Checking database connection...")

    with engine.connect() as connection:
        print("Database connection successful!")

    print("Creating database tables...")

    SQLModel.metadata.create_all(engine)

    print(
        f"Table creation completed in "
        f"{time.perf_counter() - start:.2f} seconds"
    )
