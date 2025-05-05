"""
Модуль с Pydantic-схемами для работы с авторами.

Содержит схемы для валидации данных при операциях CRUD с авторами.
"""

from pydantic import BaseModel


class AuthorBase(BaseModel):        # pylint: disable=too-few-public-methods
    """
    Базовая схема автора. Используется для наследования другими схемами.

    Attributes:
        name: Полное имя автора
        bio: Биографическая информация (опционально)
    """
    name: str
    bio: str | None = None


class AuthorCreate(AuthorBase):     # pylint: disable=too-few-public-methods
    """Схема для создания нового автора (наследует все поля базовой)."""


class Author(AuthorBase):       # pylint: disable=too-few-public-methods
    """
    Схема для возвращения данных об авторе. 
    Добавляет идентификатор и настройки ORM.

    Attributes:
        id: Уникальный идентификатор автора в БД
    """
    id: int

    class Config:       # pylint: disable=too-few-public-methods
        """Настройки для работы с ORM."""
        from_attributes = True
