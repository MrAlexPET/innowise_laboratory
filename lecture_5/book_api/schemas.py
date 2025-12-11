"""
Pydantic models (schemas) used for request validation and response models.


Using separate schemas for Create / Update / Response helps clearly define
which fields are required for each operation and keeps API contracts explicit.
"""


from pydantic import BaseModel
from typing import Optional


class BookBase(BaseModel):
    """Base fields shared by create/update schemas."""
    title: str
    author: str
    year: Optional[int] = None


class BookCreate(BookBase):
    """Schema used when creating a new book (all required fields inherited)."""
    pass


class BookUpdate(BaseModel):
    """Schema for partial updates. All fields optional so callers can update any subset."""
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None


class BookOut(BookBase):
    """Schema used for responses. Includes the auto-generated `id` field."""
    id: int


class Config:
    orm_mode = True  # allow returning ORM objects directly
