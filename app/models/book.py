"""
Модуль с моделью данных для книг.

Содержит определение таблицы books в базе данных и связи с другими таблицами.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Book(Base):       # pylint: disable=too-few-public-methods
    """
    Модель представления книги в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор книги (первичный ключ)
        title (str): Название книги
        publication_year (int): Год публикации
        isbn (str): Уникальный номер ISBN
        author_id (int): Внешний ключ для связи с автором
        author (Relationship): Связь многие-к-одному с автором
        reviews (Relationship): Связь один-ко-многим с отзывами
        genres (Relationship): Связь многие-ко-многим с жанрами
    """

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_year = Column(Integer)
    isbn = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book")
    genres = relationship(
        "Genre",
        secondary="book_genre",
        back_populates="books"
    )
