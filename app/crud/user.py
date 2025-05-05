"""
Модуль для операций CRUD с пользователями.

Содержит функции для работы с учетными записями пользователей:
создание, получение и обновление данных.
"""

from typing import Optional
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate
from app.security import get_password_hash


def get_user(db: Session, user_id: int) -> Optional[User]:
    """
    Получает пользователя по идентификатору.

    Args:
        db: Сессия базы данных.
        user_id: Идентификатор пользователя.

    Returns:
        Optional[User]: Объект пользователя или None, если не найден.
    """
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Находит пользователя по email.

    Args:
        db: Сессия базы данных.
        email: Email пользователя для поиска.

    Returns:
        Optional[User]: Объект пользователя или None, если не найден.
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Находит пользователя по имени пользователя.

    Args:
        db: Сессия базы данных.
        username: Логин пользователя для поиска.

    Returns:
        Optional[User]: Объект пользователя или None, если не найден.
    """
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Создает нового пользователя в базе данных.

    Args:
        db: Сессия базы данных.
        user: Данные для создания пользователя.

    Returns:
        User: Созданный объект пользователя.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(
    db: Session,
    user_id: int,
    new_password: str
) -> Optional[User]:
    """
    Обновляет пароль пользователя.

    Args:
        db: Сессия базы данных.
        user_id: Идентификатор пользователя.
        new_password: Новый пароль для установки.

    Returns:
        Optional[User]: Обновленный объект пользователя или None, если не найден.
    """
    user = get_user(db, user_id)
    if user:
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
    return user
