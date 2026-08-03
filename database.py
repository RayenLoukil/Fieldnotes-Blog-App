from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase , sessionmaker

DB_URL = "sqlite:///./fieldnotes.db"

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},)

SessionLocal  = sessionmaker(autocommit=False , bind=engine , autoflush=False )

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as db :
        yield db