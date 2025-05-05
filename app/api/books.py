"""
Модуль для работы с книгами
Содержит CRUD-операции и дополнительные функции для работы с книгами
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.dependencies import get_db, get_current_user
from app import crud, schemas
from app.models.book import Book
from app.models.review import Review

router = APIRouter(tags=["Книги"])


@router.get(
    "/{book_id}",
    response_model=schemas.Book,
    summary="Получить книгу по ID"
)
def read_book(
        book_id: int,
        db: Annotated[Session, Depends(get_db)]
) -> schemas.Book:
    """Получение информации о книге по её идентификатору

    Args:
        book_id: Идентификатор книги
        db: Сессия базы данных

    Returns:
        schemas.Book: Данные книги

    Raises:
        HTTPException: 404 Если книга не найдена
    """
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )
    return db_book


@router.get(
    "/books/top-rated/",
    response_model=list[schemas.Book],
    summary="Топ книг по рейтингу"
)
def get_top_rated_books(
        limit: int = 10,
        db: Session = Depends(get_db)
) -> list[schemas.Book]:
    """Получение списка книг с наивысшим рейтингом

    Args:
        limit: Количество возвращаемых книг (по умолчанию 10)
        db: Сессия базы данных

    Returns:
        list[schemas.Book]: Список книг с рейтингом
    """
    top_books = (
        db.query(Book)
        .join(Review)
        .group_by(Book.id)
        .order_by(func.avg(Review.rating).desc())
        .limit(limit)
        .all()
    )
    return top_books


@router.post(
    "/books/",
    response_model=schemas.Book,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую книгу"
)
def create_book(
        book: schemas.BookCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Depends(get_current_user)]
) -> schemas.Book:
    """Создание новой книги в каталоге

    Args:
        book: Данные для создания книги
        db: Сессия базы данных
        current_user: Текущий аутентифицированный пользователь

    Returns:
        schemas.Book: Созданная книга

    Raises:
        HTTPException: 404 Если автор не найден
        HTTPException: 400 Если ISBN уже существует
    """
    try:
        db_author = crud.get_author(db, book.author_id)
        if not db_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Автор не найден"
            )

        return crud.create_book(db=db, book=book)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Книга с таким ISBN уже существует"
        ) from e


@router.put(
    "/{book_id}",
    response_model=schemas.Book,
    summary="Обновить информацию о книге"
)
def update_book(
        book_id: int,
        book_data: schemas.BookCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Depends(get_current_user)]
) -> schemas.Book:
    """Обновление информации о существующей книге

    Args:
        book_id: Идентификатор книги
        book_data: Новые данные книги
        db: Сессия базы данных
        current_user: Текущий аутентифицированный пользователь

    Returns:
        schemas.Book: Обновленные данные книги

    Raises:
        HTTPException: 404 Если книга не найдена
    """
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )
    return crud.update_book(db, book_id, book_data)


@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить книгу"
)
def delete_book(
        book_id: int,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[schemas.User, Depends(get_current_user)]
) -> None:
    """Удаление книги из каталога

    Args:
        book_id: Идентификатор книги
        db: Сессия базы данных
        current_user: Текущий аутентифицированный пользователь

    Raises:
        HTTPException: 404 Если книга не найдена
    """
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )
    crud.delete_book(db, book_id)