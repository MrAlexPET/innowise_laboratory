"""
ORM model definitions.


We define a single `Book` model mapped to the `books` table.
Fields:
- id: primary key integer
- title: required string
- author: required string
- year: optional integer


All fields have basic indexing where helpful.
"""


from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    """SQLAlchemy ORM model representing a book record."""

    __tablename__ = "books"

    # Primary key column. `index=True` helps with certain lookups.
    id = Column(Integer, primary_key=True, index=True)

    # Required title and author columns
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)

    # Optional publication year
    year = Column(Integer, nullable=True, index=True)
