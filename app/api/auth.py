"""
Точки API аутентификации
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import crud, schemas, security

router = APIRouter(tags=["Authentication"])


@router.post(
    "/token",
    summary="Аутентификация и получение токена",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK
)
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
) -> dict:
    """Аутентификация пользователя и возврат токена JWT

    Аргументы:
    form_data: данные формы OAuth2 с именем пользователя/паролем
    db: сеанс базы данных

    Возвращает:
    dict: токен доступа и тип токена

    Вызывает:
    HTTPException: 401, если недействительные учетные данные
    """
    user = crud.get_user_by_username(db, form_data.username)

    if not user or not security.verify_password(
            form_data.password,
            user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )

    access_token = security.create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
    "/register",
    response_model=schemas.User,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя"
)
def register_user(
        user_data: schemas.UserCreate,
        db: Session = Depends(get_db)
) -> schemas.User:
    """Регистрация нового пользователя в системе

    Аргументы:
    user_data: Данные регистрации пользователя
    db: Сеанс базы данных

    Возвращает:
    schemas.User: Созданные данные пользователя

    Вызывает:
    HTTPException: 400, если имя пользователя/адрес электронной почты уже существуют
    """
    if crud.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    if crud.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    hashed_password = security.get_password_hash(user_data.password)

    db_user = crud.create_user(
        db,
        schemas.UserCreate(
            username=user_data.username,
            email=user_data.email,
            password=hashed_password
        )
    )

    return db_user
