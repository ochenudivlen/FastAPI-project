"""
Модуль для работы с эндпоинтами пользователей.

Содержит операции для получения информации о текущем аутентифицированном пользователе.
"""

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app import schemas

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/me",
    response_model=schemas.User,
    summary="Получить данные текущего пользователя",
    description="Возвращает информацию о текущем аутентифицированном пользователе"
)
def read_current_user(
    current_user: schemas.User = Depends(get_current_user)
) -> schemas.User:
    """
    Получает информацию о текущем аутентифицированном пользователе.

    Args:
        current_user: Объект текущего пользователя из зависимости.

    Returns:
        schemas.User: Данные аутентифицированного пользователя.
    """
    return current_user