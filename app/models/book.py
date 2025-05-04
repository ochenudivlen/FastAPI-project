from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publication_year = Column(Integer)
    isbn = Column(String, unique=True, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book")
    genres = relationship("Genre", secondary="book_genre", back_populates="books")