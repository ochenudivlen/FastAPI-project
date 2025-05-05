"""
Модуль для операций CRUD с авторами книг.

Содержит функции для создания, чтения, обновления и удаления авторов в базе данных.
"""

from sqlalchemy.orm import Session
from app.models import Author
from app.schemas import AuthorCreate


def get_author(db: Session, author_id: int) -> Author | None:
    """
    Получает автора по его идентификатору.

    Args:
        db: Сессия базы данных.
        author_id: Идентификатор автора.

    Returns:
        Author | None: Объект автора или None, если не найден.
    """
    return db.query(Author).filter(Author.id == author_id).first()


def create_author(db: Session, author: AuthorCreate) -> Author:
    """
    Создает нового автора в базе данных.

    Args:
        db: Сессия базы данных.
        author: Данные для создания автора.

    Returns:
        Author: Созданный объект автора.
    """
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author: AuthorCreate) -> Author | None:
    """
    Обновляет данные автора.

    Args:
        db: Сессия базы данных.
        author_id: Идентификатор автора для обновления.
        author: Новые данные автора.

    Returns:
        Author | None: Обновленный объект автора или None, если не найден.
    """
    db_author = get_author(db, author_id)
    if db_author:
        for key, value in author.dict().items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> Author | None:
    """
    Удаляет автора из базы данных.

    Args:
        db: Сессия базы данных.
        author_id: Идентификатор автора для удаления.

    Returns:
        Author | None: Удаленный объект автора или None, если не найден.
    """
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author
