"""
Модуль с моделью данных для отзывов о книгах.

Содержит определение таблицы reviews и связей с пользователями и книгами.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Review(Base):     # pylint: disable=too-few-public-methods
    """
    Модель представления отзыва в базе данных.

    Атрибуты:
        id (int): Уникальный идентификатор отзыва (первичный ключ)
        book_id (int): Внешний ключ для связи с книгой
        user_id (int): Внешний ключ для связи с пользователем
        rating (int): Оценка книги (от 1 до 5)
        comment (str): Текстовый комментарий к отзыву
        book (Relationship): Связь многие-к-одному с книгой
        user (Relationship): Связь многие-к-одному с пользователем
    """

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(String)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
