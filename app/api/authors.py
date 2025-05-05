"""
Модуль для работы с авторами книг
Содержит CRUD-операции для управления авторами в системе
"""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import crud, schemas

router = APIRouter(tags=["Авторы"])


@router.post(
    "/",
    response_model=schemas.Author,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового автора"
)
def create_author(
        author: schemas.AuthorCreate,
        db: Annotated[Session, Depends(get_db)]
) -> schemas.Author:
    """Создание нового автора в системе

    Args:
        author: Данные для создания автора
        db: Сессия базы данных

    Returns:
        schemas.Author: Созданный автор

    Raises:
        HTTPException: 400 Если автор с таким именем уже существует
    """
    return crud.create_author(db=db, author=author)


@router.get(
    "/{author_id}",
    response_model=schemas.Author,
    summary="Получить автора по ID"
)
def read_author(
        author_id: int,
        db: Annotated[Session, Depends(get_db)]
) -> schemas.Author:
    """Получение информации об авторе по его идентификатору

    Args:
        author_id: Идентификатор автора
        db: Сессия базы данных

    Returns:
        schemas.Author: Данные автора

    Raises:
        HTTPException: 404 Если автор не найден
    """
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор не найден"
        )
    return author


@router.put(
    "/{author_id}",
    response_model=schemas.Author,
    summary="Обновить данные автора"
)
def update_author(
        author_id: int,
        author: schemas.AuthorCreate,
        db: Annotated[Session, Depends(get_db)]
) -> schemas.Author:
    """Обновление информации об авторе

    Args:
        author_id: Идентификатор автора
        author: Новые данные автора
        db: Сессия базы данных

    Returns:
        schemas.Author: Обновленные данные автора

    Raises:
        HTTPException: 404 Если автор не найден
    """
    db_author = crud.get_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор не найден"
        )
    return crud.update_author(db=db, author_id=author_id, author=author)


@router.delete(
    "/{author_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить автора"
)
def delete_author(
        author_id: int,
        db: Annotated[Session, Depends(get_db)]
) -> None:
    """Удаление автора из системы

    Args:
        author_id: Идентификатор автора
        db: Сессия базы данных

    Raises:
        HTTPException: 404 Если автор не найден
    """
    db_author = crud.delete_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Автор не найден"
        )
    return