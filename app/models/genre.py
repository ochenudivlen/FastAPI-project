"""
Модуль с моделью данных для жанров книг.

Содержит определение таблицы genres и ассоциативной таблицы book_genre
для связи многие-ко-многим с книгами.
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from app.database import Base


book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True)
)


class Genre(Base):      # pylint: disable=too-few-public-methods
    """
    Модель представления жанра в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор жанра (первичный ключ)
        name (str): Название жанра (уникальное)
        books (Relationship): Связь многие-ко-многим с книгами через book_genre
    """

    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship(
        "Book",
        secondary=book_genre,
        back_populates="genres"
    )
