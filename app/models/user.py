"""
Модуль с моделью данных для пользователей.

Содержит определение таблицы users и связи с отзывами.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):       # pylint: disable=too-few-public-methods
    """
    Модель представления пользователя в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор пользователя (первичный ключ)
        username (str): Уникальное имя пользователя
        hashed_password (str): Хеш пароля пользователя
        email (str): Уникальный email пользователя
        reviews (Relationship): Связь один-ко-многим с отзывами
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True)

    reviews = relationship("Review", back_populates="user")
