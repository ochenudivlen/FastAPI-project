from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Genre, Book, book_genre
from app.schemas import GenreCreate

def get_genre(db: Session, genre_id: int):
    return db.query(Genre).filter(Genre.id == genre_id).first()

def get_genre_by_name(db: Session, name: str):
    return db.query(Genre).filter(func.lower(Genre.name) == func.lower(name)).first()

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Genre).offset(skip).limit(limit).all()

def create_genre(db: Session, genre: GenreCreate):
    db_genre = Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

def update_genre(db: Session, genre_id: int, genre: GenreCreate):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        db_genre.name = genre.name
        db.commit()
        db.refresh(db_genre)
    return db_genre

def delete_genre(db: Session, genre_id: int):
    db_genre = get_genre(db, genre_id)
    if db_genre:
        db.delete(db_genre)
        db.commit()
    return db_genre