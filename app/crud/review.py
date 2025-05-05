"""
Модуль для операций CRUD с отзывами о книгах.

Содержит функции для создания и получения отзывов из базы данных.
"""

from sqlalchemy.orm import Session
from app.models import Review
from app.schemas import ReviewCreate


def create_review(db: Session, review: ReviewCreate) -> Review:
    """
    Создает новый отзыв о книге в базе данных.

    Args:
        db: Сессия базы данных.
        review: Данные для создания отзыва.

    Returns:
        Review: Созданный объект отзыва.
    """
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews_by_book(db: Session, book_id: int) -> list[Review]:
    """
    Получает все отзывы для указанной книги.

    Args:
        db: Сессия базы данных.
        book_id: Идентификатор книги.

    Returns:
        list[Review]: Список отзывов для указанной книги.
    """
    return db.query(Review).filter(Review.book_id == book_id).all()