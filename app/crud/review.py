from sqlalchemy.orm import Session
from app.models import Review
from app.schemas import ReviewCreate

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_reviews_by_book(db: Session, book_id: int):
    return db.query(Review).filter(Review.book_id == book_id).all()