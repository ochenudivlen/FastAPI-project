from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app.database import Base

book_genre = Table(
    "book_genre",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id")),
    Column("genre_id", Integer, ForeignKey("genres.id"))
)

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    books = relationship("Book", secondary=book_genre, back_populates="genres")