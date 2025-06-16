from sqlalchemy.orm import Session
from sqlalchemy import exc

import models
from schemas import BookCreate


def get_all_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DBBook).offset(skip).limit(limit).all()


def get_books_by_author_id(db: Session, author_id: int):
    return db.query(
        models.DBBook).filter(
        models.DBBook.author_id == author_id).all()


def create_book_for_author(db: Session, book_data: BookCreate):

    author_existing = db.query(models.DBAuthor).filter(
        models.DBAuthor.id == book_data.author_id
    ).first()

    if not author_existing:
        raise ValueError(f"Author with id '{book_data.author_id}' does not exist.")

    new_book = models.DBBook(
        title=book_data.title,
        summary=book_data.summary,
        publication_date=book_data.publication_date,
        author_id=book_data.author_id,
    )
    try:
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
    except exc.IntegrityError:
        db.rollback()
        raise ValueError("Some error occurred while creating the book.")
    except Exception as e:
        db.rollback()
        raise Exception(f"An unexpected error occurred: {e}")

    return new_book
