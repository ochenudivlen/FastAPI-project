from pydantic import BaseModel, field_validator, constr
from datetime import datetime

class BookBase(BaseModel):
    title: str
    publication_year: int
    isbn: constr(pattern=r'^\d{3}-\d{10}$')  # Формат ISBN 000-0000000000
    author_id: int

    @field_validator('publication_year')
    def validate_year(cls, v):
        if v > datetime.now().year:
            raise ValueError('Publication year cannot be in the future')
        return v

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True