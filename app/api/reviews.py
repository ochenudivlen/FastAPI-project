"""
Модуль для работы с отзывами о книгах в REST API.

Содержит операции создания и получения отзывов с проверкой аутентификации пользователя.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app import crud, schemas, models

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> schemas.Review:
    """
    Создает новый отзыв о книге.

    Args:
        review: Данные для создания отзыва.
        db: Сессия базы данных.
        current_user: Текущий аутентифицированный пользователь.

    Returns:
        schemas.Review: Созданный отзыв.
    """
    return crud.create_review(db=db, review=review)


@router.get("/book/{book_id}", response_model=list[schemas.Review])
def get_book_reviews(
    book_id: int,
    db: Session = Depends(get_db)
) -> list[schemas.Review]:
    """
    Получает список отзывов для указанной книги.

    Args:
        book_id: Идентификатор книги.
        db: Сессия базы данных.

    Returns:
        list[schemas.Review]: Список отзывов для книги.
    """
    reviews = crud.get_reviews_by_book(db, book_id=book_id)
    if not reviews:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзывы для данной книги не найдены"
        )
    return reviews