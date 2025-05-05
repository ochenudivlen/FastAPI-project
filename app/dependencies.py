"""
Модуль зависимостей приложения.

Содержит функции для работы с аутентификацией и получения текущего пользователя.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app import security, crud
from app.schemas.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[Session, Depends(get_db)]
) -> User:
    """
    Получает текущего аутентифицированного пользователя по JWT-токену.

    Args:
        token: JWT-токен из заголовка Authorization
        db: Сессия базы данных

    Returns:
        User: Объект аутентифицированного пользователя

    Raises:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = security.decode_token(token)
        username: str | None = payload.get("sub")

        if not username:
            raise credentials_exception

    except JWTError as exc:
        raise credentials_exception from exc

    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user
