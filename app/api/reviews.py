from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app import crud, schemas, models

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=schemas.Review)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # Требуется авторизация
):
    return crud.create_review(db=db, review=review)

@router.get("/book/{book_id}", response_model=list[schemas.Review])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    return crud.get_reviews_by_book(db, book_id=book_id)