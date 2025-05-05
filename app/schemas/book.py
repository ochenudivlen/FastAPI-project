"""
Модуль с Pydantic-схемами для работы с книгами.

Содержит схемы для валидации данных при операциях CRUD с книгами.
"""

from datetime import datetime
from pydantic import BaseModel, field_validator, constr


class BookBase(BaseModel):        # pylint: disable=too-few-public-methods
    """
    Базовая схема книги. Используется для создания и обновления записей.

    Attributes:
        title: Название книги
        publication_year: Год публикации
        isbn: Уникальный номер ISBN в формате 000-0000000000
        author_id: Идентификатор автора книги

    Raises:
        ValueError: Если год публикации превышает текущий год
    """
    title: str
    publication_year: int
    isbn: constr(pattern=r'^\d{3}-\d{10}$')  # Формат ISBN 000-0000000000
    author_id: int

    @field_validator('publication_year')
    def validate_year(cls, value: int) -> int:
        """
        Проверяет корректность года публикации.

        Args:
            value: Проверяемый год публикации

        Returns:
            int: Валидный год публикации

        Raises:
            ValueError: Если год публикации в будущем
        """
        current_year = datetime.now().year
        if value > current_year:
            raise ValueError('Год публикации не может быть в будущем')
        return value


class BookCreate(BookBase):       # pylint: disable=too-few-public-methods
    """Схема для создания новой книги (наследует все поля базовой схемы)."""


class Book(BookBase):         # pylint: disable=too-few-public-methods
    """
    Схема для возвращения данных о книге. 
    Добавляет идентификатор и настройки ORM.

    Attributes:
        id: Уникальный идентификатор книги в БД
    """
    id: int

    class Config:         # pylint: disable=too-few-public-methods
        """Настройки для работы с ORM."""
        from_attributes = True
