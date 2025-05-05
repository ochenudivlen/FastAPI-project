"""
Модуль с Pydantic-схемами для работы с жанрами.

Содержит схемы для валидации данных при операциях CRUD с жанрами.
"""

from pydantic import BaseModel


class GenreBase(BaseModel):     # pylint: disable=too-few-public-methods
    """
    Базовая схема жанра. Используется для наследования другими схемами.

    Attributes:
        name: Название жанра
    """
    name: str


class GenreCreate(GenreBase):       # pylint: disable=too-few-public-methods
    """Схема для создания нового жанра (наследует все поля базовой схемы)."""

class Genre(GenreBase):     # pylint: disable=too-few-public-methods
    """
    Схема для возвращения данных о жанре. 
    Добавляет идентификатор и количество книг.

    Attributes:
        id: Уникальный идентификатор жанра в БД
        book_count: Количество книг в данном жанре (опционально)
    """
    id: int
    book_count: int | None = None

    class Config:       # pylint: disable=too-few-public-methods
        """Настройки для работы с ORM."""
        from_attributes = True
