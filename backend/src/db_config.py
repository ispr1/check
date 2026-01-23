from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get database URL from environment
DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/check360")

# Create engine with connection pooling
db_engine = create_engine(DB_URL, pool_pre_ping=True, echo=False)

# Session factory
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

# Base class for models
BaseModel = declarative_base()


def get_database_session():
    """Generator function for database sessions"""
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
