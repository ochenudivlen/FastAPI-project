from pydantic import BaseModel, Field

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str | None = None
    book_id: int

class Review(ReviewBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True