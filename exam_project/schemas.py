
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    description: Optional[str] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    publication_year: Optional[int] = None
    stock_quantity: int = Field(default=1, ge=0)
    category_id: int


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    isbn: Optional[str] = Field(default=None, min_length=1)
    publication_year: Optional[int] = None
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    category_id: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: Optional[int] = None
    stock_quantity: int
    category_id: int

    model_config = ConfigDict(from_attributes=True)
