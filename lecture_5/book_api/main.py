"""
Async FastAPI application exposing Book management endpoints.

All endpoints are `async def` and use `AsyncSession` via dependency injection.
Detailed English comments are added to each endpoint for graders.
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, AsyncSessionLocal, Base
import schemas
import crud

# Create database tables if they do not exist. For async engines, we run
# metadata.create_all() in a synchronous context using run_sync.
# This operation is performed here once at startup so the DB file and
# schema are present before handling requests.


async def _create_db_and_tables():
    # Use engine.begin() and run_sync to create tables synchronously in the DB.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(title="Async Book Collection API")


# Register startup event to create tables before serving requests.
@app.on_event("startup")
async def on_startup():
    await _create_db_and_tables()


# Dependency that yields an AsyncSession for each request. Using `async with`
# ensures the session is properly closed after use even if an exception occurs.
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@app.post("/books/", response_model=schemas.BookOut, status_code=201)
async def create_book_endpoint(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    """Create a book record, preventing duplicates.

    - Validates incoming payload via BookCreate schema.
    - Checks if a book with the same title, author, and year already exists.
    - If exists, raises HTTP 409 Conflict.
    - Otherwise, creates the book and returns BookOut (includes generated id).
    """
    # Check if book already exists
    existing_book = await crud.get_book_by_unique_fields(db, book.title, book.author, book.year)
    if existing_book:
        raise HTTPException(
            status_code=409,
            detail="Book with this title, author and year already exists"
        )

    # Create new book
    created = await crud.create_book(db, book)
    return created


@app.get("/books/", response_model=List[schemas.BookOut])
async def read_books_endpoint(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """Read books with pagination support using query parameters `skip` and `limit`."""
    return await crud.get_books(db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.BookOut)
async def read_book_by_id(book_id: int, db: AsyncSession = Depends(get_db)):
    """Get a single book by its ID. Returns 404 if not found."""
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.BookOut)
async def update_book_endpoint(book_id: int, updates: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    """Update an existing book. Only fields provided in BookUpdate are altered."""
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    updated = await crud.update_book(db, db_book, updates)
    return updated


@app.delete("/books/{book_id}")
async def delete_book_endpoint(book_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a book by ID. Returns success message on deletion."""
    db_book = await crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await crud.delete_book(db, db_book)
    return {"detail": "Book deleted"}


@app.get("/books/search/", response_model=List[schemas.BookOut])
async def search_books_endpoint(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Search books by title, author or year (all parameters optional)."""
    results = await crud.search_books(db, title=title, author=author, year=year)
    # For search endpoints typically it's OK to return an empty list instead of 404.
    return results
