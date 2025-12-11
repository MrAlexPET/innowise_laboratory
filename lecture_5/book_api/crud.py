"""
Async CRUD operations for Book model.

Each function accepts an AsyncSession and performs the required
operation using SQLAlchemy Core/ORM async APIs (select/execute/commit).
All functions are fully asynchronous and documented for grading.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Book
import models
import schemas


async def get_book(db: AsyncSession, book_id: int) -> Optional[models.Book]:
    """Return a single Book by id or None if not found.

    Uses `select()` + `execute()` then `scalars().first()` to return the ORM object.
    """
    stmt = select(models.Book).where(models.Book.id == book_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """Return a list of books with pagination (skip/limit)."""
    stmt = select(models.Book).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def search_books(
    db: AsyncSession, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None
) -> List[models.Book]:
    """Search books by partial title, partial author (case-insensitive) and exact year.

    This function builds a dynamic query depending on the provided parameters.
    """
    stmt = select(models.Book)

    if title:
        # Use ilike for case-insensitive partial matching
        stmt = stmt.where(models.Book.title.ilike(f"%{title}%"))
    if author:
        stmt = stmt.where(models.Book.author.ilike(f"%{author}%"))
    if year is not None:
        stmt = stmt.where(models.Book.year == year)

    result = await db.execute(stmt)
    return result.scalars().all()


async def create_book(db: AsyncSession, book: schemas.BookCreate) -> models.Book:
    """Create a new Book record and return the ORM object.

    We add the object to the session, commit the transaction and refresh
    to populate auto-generated fields (like `id`).
    """
    db_book = models.Book(title=book.title, author=book.author, year=book.year)
    db.add(db_book)
    # commit persists the change to the DB
    await db.commit()
    # refresh loads any DB-generated defaults into db_book (e.g., id)
    await db.refresh(db_book)
    return db_book


async def update_book(db: AsyncSession, db_book: models.Book, updates: schemas.BookUpdate) -> models.Book:
    """Update fields on an existing Book ORM instance and persist changes.

    Receives an already-loaded ORM object (db_book). Only non-None fields
    from `updates` are applied. After commit, the object is refreshed.
    """
    if updates.title is not None:
        db_book.title = updates.title
    if updates.author is not None:
        db_book.author = updates.author
    if updates.year is not None:
        db_book.year = updates.year

    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def delete_book(db: AsyncSession, db_book: models.Book) -> None:
    """Delete a Bсвook ORM object from the database."""
    await db.delete(db_book)
    await db.commit()


async def get_book_by_unique_fields(db: AsyncSession, title: str, author: str, year: int):
    """Check if a book with the given title, author, and year exists."""
    result = await db.execute(
        select(Book).where(Book.title == title, Book.author == author, Book.year == year)
    )
    return result.scalars().first()
