"""
Модуль для работы с базой данных.

Содержит настройки подключения к PostgreSQL, фабрику сессий и обработку ошибок.
"""

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/book_catalog"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def get_db():
    """
    Контекстный менеджер для получения сессии базы данных.

    Yields:
        Session: Сессия базы данных

    Пример использования:
        with get_db() as db:
            # работа с базой данных
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка базы данных: {str(exc)}"
        ) from exc
    finally:
        db.close()


def handle_db_errors(func):
    """
    Декоратор для обработки ошибок базы данных.

    Args:
        func: Декорируемая функция

    Returns:
        function: Обернутая функция с обработкой исключений

    Raises:
        HTTPException: При возникновении ошибок SQLAlchemy
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except SQLAlchemyError as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Ошибка базы данных: {str(exc)}"
            ) from exc
    return wrapper
