from fastapi import APIRouter, Depends
from app.dependencies import get_db, get_current_user
from app import schemas

router = APIRouter(tags=["Users"])

@router.get(
    "/me",
    response_model=schemas.User,
    summary="Получить данные текущего пользователя"
)
def read_current_user(
    current_user: schemas.User = Depends(get_current_user)
):
    return current_user