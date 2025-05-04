from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.dependencies import get_db
from app import crud, schemas

router = APIRouter()

@router.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@router.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/books/top-rated/")
def get_top_rated_books(limit: int = 10, db: Session = Depends(get_db)):
    top_books = db.query(Book).join(Review).group_by(Book.id).order_by(func.avg(Review.rating).desc()).limit(limit).all()
    return top_books

@router.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(
        book: schemas.BookCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(deps.get_current_user)
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