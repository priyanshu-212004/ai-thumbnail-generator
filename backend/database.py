from sqlmodel import SQLModel, create_engine, Session
from config import DATABASE_URL


# -----------------------
# ENGINE
# -----------------------
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}  # SQLite only
)


# -----------------------
# CREATE TABLES
# -----------------------
def create_tables():
    SQLModel.metadata.create_all(engine)


# -----------------------
# SESSION DEPENDENCY (FASTAPI SAFE)
# -----------------------
def get_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()