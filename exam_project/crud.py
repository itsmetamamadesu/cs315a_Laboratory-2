
from sqlalchemy.orm import Session
from models import Category, Book


def create_category(db: Session, category_data):
    category = Category(**category_data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session):
    return db.query(Category).all()


def get_book(db: Session, book_id: int):
    return (
        db.query(Book)
        .filter(Book.id == book_id)
        .first()
    )


def get_books(db: Session, category_id=None):
    query = db.query(Book)

    if category_id is not None:
        query = query.filter(Book.category_id == category_id)

    return query.all()
