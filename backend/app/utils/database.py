import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session as SQLAlchemySession
from datetime import datetime
from typing import Generator
import uuid

from app.models.database import Base, Session, Message, FileAttachment

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./report_agent.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db() -> Generator[SQLAlchemySession, None, None]:
    """
    Get a database session.
    
    Yields:
        SQLAlchemy Session: A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """
    Initialize the database by creating all tables and a default session if none exists.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a default session if none exists
    db = SessionLocal()
    try:
        # Check if any sessions exist
        session_count = db.query(Session).count()
        if session_count == 0:
            # Create a default session
            default_session = Session.create_new(title="New Analysis")
            db.add(default_session)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error initializing database: {e}")
    finally:
        db.close()
