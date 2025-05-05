"""
Модуль схем отзыва (review) приложения.
"""

from typing import Optional
from pydantic import BaseModel, Field


class ReviewBase(BaseModel):        # pylint: disable=too-few-public-methods
    """
    Базовая схема отзыва.
    """
    rating: int = Field(..., description="Рейтинг отзыва", ge=1, le=5)
    comment: Optional[str] = None
    book_id: int


class ReviewCreate(ReviewBase):     # pylint: disable=too-few-public-methods
    """
    Схема для создания отзыва.
    """


class Review(ReviewBase):       # pylint: disable=too-few-public-methods
    """
    Полная схема отзыва.
    """
    id: int
    user_id: int

    class Config:       # pylint: disable=too-few-public-methods
        """
        Конфигурация модели Pydantic.
        """
        from_attributes = True
