from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config

engine = create_engine(config.DB_URL, connect_args={"check_same_thread": False} if "sqlite" in config.DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
