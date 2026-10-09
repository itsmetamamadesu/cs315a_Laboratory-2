from fastapi import FastAPI, Depends, HTTPException, Query, status
from typing import Optional


from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import Base, engine, get_db
import models
import schemas
import crud


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management API")


# 1. CREATE CATEGORY
@app.post(
    "/categories/",
    response_model=schemas.CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(models.Category)
        .filter(models.Category.name == category.name)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category name already exists"
        )

    try:
        return crud.create_category(db, category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to create category"
        )


# 2. GET ALL CATEGORIES
@app.get(
    "/categories/",
    response_model=list[schemas.CategoryResponse]
)
def read_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


# 3. CREATE BOOK
@app.post(
    "/books/",
    response_model=schemas.BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    category = (
        db.query(models.Category)
        .filter(models.Category.id == book.category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category does not exist"
        )

    existing = (
        db.query(models.Book)
        .filter(models.Book.isbn == book.isbn)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="ISBN already exists"
        )

    new_book = models.Book(**book.model_dump())

    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to create book"
        )


# 4. GET ALL BOOKS / FILTER BY CATEGORY
@app.get(
    "/books/",
    response_model=list[schemas.BookResponse]
)
def read_books(
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    if category_id is not None:
        category = (
            db.query(models.Category)
            .filter(models.Category.id == category_id)
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    return crud.get_books(db, category_id)


# 5. GET ONE BOOK
@app.get(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
def read_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return book


# 6. UPDATE BOOK
@app.put(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
def update_book(
    book_id: int,
    book_data: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    changes = book_data.model_dump(exclude_unset=True)

    if "category_id" in changes and changes["category_id"] is not None:
        category = (
            db.query(models.Category)
            .filter(models.Category.id == changes["category_id"])
            .first()
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

    if "isbn" in changes and changes["isbn"] is not None:
        existing = (
            db.query(models.Book)
            .filter(
                models.Book.isbn == changes["isbn"],
                models.Book.id != book_id
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="ISBN already exists"
            )

    for key, value in changes.items():
        setattr(book, key, value)

    try:
        db.commit()
        db.refresh(book)
        return book
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to update book"
        )


# 7. DELETE BOOK
@app.delete(
    "/books/{book_id}",
    response_model=schemas.BookResponse
)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()
    return book
