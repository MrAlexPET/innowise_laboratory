"""
Async database setup using SQLAlchemy and SQLite (aiosqlite).


This module creates an async engine and an async session factory that
other modules import to obtain AsyncSession instances. We use
`sqlite+aiosqlite:///./books.db` connection URL for a local file DB.


All functions and endpoints that interact with the DB should use
`AsyncSession` from this module via dependency injection.
"""


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base


# Async connection URL for SQLite using aiosqlite driver.
DATABASE_URL = "sqlite+aiosqlite:///./books.db"


# Create the async engine. echo=True can be enabled for SQL logging during development.
engine = create_async_engine(DATABASE_URL, echo=False, future=True)


# Async session factory. expire_on_commit=False prevents attributes from being expired
# after commit which makes it easier to work with returned ORM objects in async code.
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


# Declarative base for ORM models (shared across modules)
Base = declarative_base()
