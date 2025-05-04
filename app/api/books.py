from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from app.dependencies import get_db, get_current_user
from app import crud, schemas
from app.models.book import Book
from app.models.review import Review

router = APIRouter()

@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book

@router.get("/books/top-rated/")
def get_top_rated_books(limit: int = 10, db: Session = Depends(get_db)):
    top_books = db.query(Book).join(Review).group_by(Book.id).order_by(func.avg(Review.rating).desc()).limit(limit).all()
    return top_books

@router.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user)
):
    try:
        # Проверка существования автора
        db_author = crud.get_author(db, book.author_id)
        if not db_author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Author not found"
            )

        return crud.create_book(db=db, book=book)
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with this ISBN already exists"
        )

@router.put("/{book_id}")
def update_book(
    book_id: int,
    book_data: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.update_book(db, book_id, book_data)

@router.delete("/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)  # Требуем аутентификацию
):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return crud.delete_book(db, book_id)