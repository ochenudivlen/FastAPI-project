"""
Маркер, который сообщает интерпретатору, что каталог содержит код для модуля Python.
"""

from .book import Book, BookCreate
from .user import User, UserCreate, Token
from .author import Author, AuthorCreate
from .genre import Genre, GenreCreate
from .review import Review, ReviewCreate

__all__ = [
    "Book", "BookCreate",
    "User", "UserCreate", "Token",
    "Author", "AuthorCreate",
    "Genre", "GenreCreate",
    "Review", "ReviewCreate"
]
