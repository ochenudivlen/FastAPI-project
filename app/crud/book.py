"""
Модуль для операций CRUD с книгами.

Содержит функции для создания и чтения книг в базе данных.
"""

from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookCreate


def get_book(db: Session, book_id: int) -> Book | None:
    """
    Получает книгу по её идентификатору.

    Args:
        db: Сессия базы данных.
        book_id: Идентификатор книги.

    Returns:
        Book | None: Объект книги или None, если не найдена.
    """
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: BookCreate) -> Book:
    """
    Создает новую книгу в базе данных.

    Args:
        db: Сессия базы данных.
        book: Данные для создания книги.

    Returns:
        Book: Созданный объект книги.
    """
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
