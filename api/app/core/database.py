"""
Database Configuration and Session Management

This module handles the connection to PostgreSQL and provides
the SQLAlchemy session for database operations.

KEY CONCEPTS:
-------------
1. Engine: The connection pool to the database
2. SessionLocal: A factory for creating database sessions
3. get_db: A dependency injection function for FastAPI

WHY USE DEPENDENCY INJECTION?
-----------------------------
FastAPI's dependency injection system ensures that:
- Each request gets its own database session
- Sessions are properly closed after the request completes
- Transactions are rolled back if an error occurs

This prevents connection leaks and ensures data integrity.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database URL from environment variable
# Format: postgresql://user:password@host:port/database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/clinical_genomics"
)

# Create the SQLAlchemy engine
# pool_pre_ping: Checks if connection is alive before using it
# This prevents errors from stale connections
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,  # Maximum connections in the pool
    max_overflow=20,  # Additional connections if pool is exhausted
    echo=False  # Set to True to see SQL queries in logs
)

# SessionLocal is a factory that creates new Session objects
# autocommit=False: We control when to commit transactions
# autoflush=False: We control when to flush changes to the database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    Dependency injection function for FastAPI.
    
    Usage in a route:
        @app.get("/samples")
        def get_samples(db: Session = Depends(get_db)):
            return db.query(Sample).all()
    
    The `yield` keyword makes this a generator, which allows FastAPI
    to execute cleanup code (db.close()) after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
