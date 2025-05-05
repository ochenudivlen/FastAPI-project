"""
Модуль с моделью данных для авторов книг.

Содержит определение таблицы authors в базе данных и отношения с другими таблицами.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Author(Base):     # pylint: disable=too-few-public-methods
    """
    Модель представления автора в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор автора (первичный ключ)
        name (str): Полное имя автора (уникальное)
        bio (str): Биографическая информация об авторе
        books (Relationship): Связь один-ко-многим с книгами автора
    """

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    bio = Column(String)

    books = relationship("Book", back_populates="author")
