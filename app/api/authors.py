from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@router.get("/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db, author_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.put("/{author_id}", response_model=schemas.Author)
def update_author(
    author_id: int,
    author: schemas.AuthorCreate,
    db: Session = Depends(get_db)
):
    db_author = crud.get_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return crud.update_author(db=db, author_id=author_id, author=author)

@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.delete_author(db, author_id=author_id)
    if not db_author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Author not found"
        )
    return