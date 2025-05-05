"""
Модуль схем пользователей (User) приложения.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):      # pylint: disable=too-few-public-methods
    """
    Базовая схема пользователя.
    """
    username: str
    email: EmailStr


class UserCreate(UserBase):     # pylint: disable=too-few-public-methods
    """
    Схема для создания нового пользователя.
    """
    password: str

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        """
        Валидатор пароля.

        Проверяет длину пароля, наличие прописных букв и цифр.
        """
        if len(value) < 8:
            raise ValueError("Пароль должен быть минимум 8 символов.")
        if not any(char.isupper() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну прописную букву.")
        if not any(char.isdigit() for char in value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру.")
        return value


class UserUpdate(BaseModel):        # pylint: disable=too-few-public-methods
    """
    Схема для обновления профиля пользователя.
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):       # pylint: disable=too-few-public-methods
    """
    Полная схема пользователя.
    """
    id: int
    is_active: Optional[bool] = None

    class Config:       # pylint: disable=too-few-public-methods
        """
        Конфигурация модели Pydantic.
        """
        from_attributes = True


class UserInDB(User):       # pylint: disable=too-few-public-methods
    """
    Внутренняя схема пользователя с хешированным паролем.
    """
    hashed_password: str


class Token(BaseModel):     # pylint: disable=too-few-public-methods
    """
    Схема токена аутентификации.
    """
    access_token: str
    token_type: str
