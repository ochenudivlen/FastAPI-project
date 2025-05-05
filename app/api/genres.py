"""
Модуль для работы с эндпоинтами жанров в REST API.

Содержит операции CRUD для жанров книг с проверкой аутентификации пользователя.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/genres", tags=["genres"])


@router.post("/", response_model=schemas.Genre, status_code=status.HTTP_201_CREATED)
def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    Создает новый жанр в базе данных.

    Args:
        genre: Данные для создания жанра.
        db: Сессия базы данных.
        current_user: Текущий аутентифицированный пользователь.

    Returns:
        schemas.Genre: Созданный жанр.

    Raises:
        HTTPException: Если жанр с таким именем уже существует.
    """
    db_genre = crud.get_genre_by_name(db, name=genre.name)
    if db_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Жанр с таким названием уже существует",
        )
    return crud.create_genre(db=db, genre=genre)


@router.get("/", response_model=list[schemas.Genre])
def read_genres(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schemas.Genre]:
    """
    Получает список жанров из базы данных.

    Args:
        skip: Количество записей для пропуска.
        limit: Максимальное количество записей.
        db: Сессия базы данных.

    Returns:
        list[schemas.Genre]: Список жанров.
    """
    return crud.get_genres(db, skip=skip, limit=limit)


@router.get("/{genre_id}", response_model=schemas.Genre)
def read_genre(
    genre_id: int,
    db: Session = Depends(get_db),
) -> schemas.Genre:
    """
    Получает информацию о жанре по его ID.

    Args:
        genre_id: Идентификатор жанра.
        db: Сессия базы данных.

    Returns:
        schemas.Genre: Запрошенный жанр.

    Raises:
        HTTPException: Если жанр не найден.
    """
    db_genre = crud.get_genre(db, genre_id=genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жанр не найден",
        )
    return db_genre


@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
) -> None:
    """
    Удаляет жанр из базы данных.

    Args:
        genre_id: Идентификатор жанра.
        db: Сессия базы данных.
        current_user: Текущий аутентифицированный пользователь.

    Raises:
        HTTPException: Если жанр не найден.
    """
    db_genre = crud.delete_genre(db, genre_id=genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Жанр не найден",
        )
    return {"ok": True}