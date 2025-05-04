from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/genres", tags=["genres"])

@router.post("/", response_model=schemas.Genre, status_code=status.HTTP_201_CREATED)
def create_genre(
    genre: schemas.GenreCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_genre = crud.get_genre_by_name(db, name=genre.name)
    if db_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre already exists"
        )
    return crud.create_genre(db=db, genre=genre)

@router.get("/", response_model=list[schemas.Genre])
def read_genres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_genres(db, skip=skip, limit=limit)

@router.get("/{genre_id}", response_model=schemas.Genre)
def read_genre(
    genre_id: int,
    db: Session = Depends(get_db)  # Публичный доступ
):
    db_genre = crud.get_genre(db, genre_id=genre_id)
    if not db_genre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Genre not found"
        )
    return db_genre

@router.delete("/{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)  # Проверка аутентификации
):
    db_genre = crud.delete_genre(db, genre_id=genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return {"ok": True}