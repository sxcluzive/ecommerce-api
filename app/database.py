from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL
import logging

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    try:
        # Test the connection before creating tables
        with engine.connect() as connection:
            logging.info("Successfully connected to the database.")
        
        # Create tables if they do not exist
        Base.metadata.create_all(bind=engine)
        logging.info("Database tables created successfully.")
    except Exception as e:
        logging.error(f"Error connecting to the database: {e}")
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()