"""
Модуль для операций CRUD с жанрами книг.

Содержит функции для создания, чтения, обновления и удаления жанров,
а также работы с ассоциативными таблицами.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Genre
from app.schemas import GenreCreate


def get_genre(db: Session, genre_id: int) -> Genre | None:
    """
    Получает жанр по его идентификатору.

    Args:
        db: Сессия базы данных.
        genre_id: Идентификатор жанра.

    Returns:
        Genre | None: Объект жанра или None, если не найден.
    """
    return db.query(Genre).filter(Genre.id == genre_id).first()


def get_genre_by_name(db: Session, name: str) -> Genre | None:
    """
    Находит жанр по названию (без учета регистра).

    Args:
        db: Сессия базы данных.
        name: Название жанра для поиска.

    Returns:
        Genre | None: Объект жанра или None, если не найден.
    """
    return db.query(Genre).filter(func.lower(Genre.name) == func.lower(name)).first()


def get_genres(db: Session, skip: int = 0, limit: int = 100) -> list[Genre]:
    """
    Получает список жанров с пагинацией.

    Args:
        db: Сессия базы данных.
        skip: Количество пропускаемых записей.
        limit: Максимальное количество возвращаемых записей.

    Returns:
        list[Genre]: Список объектов жанров.
    """
    return db.query(Genre).offset(skip).limit(limit).all()


def create_genre(db: Session, genre: GenreCreate) -> Genre:
    """
    Создает новый жанр в базе данных.

    Args:
        db: Сессия базы данных.
        genre: Данные для создания жанра.

    Returns:
        Genre: Созданный объект жанра.
    """
    db_genre = Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def update_genre(db: Session, genre_id: int, genre: GenreCreate) -> Genre | None:
    """
    Обновляет данные жанра.

    Args:
        db: Сессия базы данных.
        genre_id: Идентификатор обновляемого жанра.
        genre: Новые данные для обновления.

    Returns:
        Genre | None: Обновленный объект жанра или None, если не найден.
    """
    db_genre = get_genre(db, genre_id)
    if db_genre:
        db_genre.name = genre.name
        db.commit()
        db.refresh(db_genre)
    return db_genre


def delete_genre(db: Session, genre_id: int) -> Genre | None:
    """
    Удаляет жанр из базы данных.

    Args:
        db: Сессия базы данных.
        genre_id: Идентификатор удаляемого жанра.

    Returns:
        Genre | None: Удаленный объект жанра или None, если не найден.
    """
    db_genre = get_genre(db, genre_id)
    if db_genre:
        db.delete(db_genre)
        db.commit()
    return db_genre
