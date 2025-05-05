"""
Маркер, который сообщает интерпретатору, что каталог содержит код для модуля Python.
"""

from .book import Book
from .author import Author
from .genre import Genre
from .user import User
from .review import Review

__all__ = ["Book", "Author", "Genre", "User", "Review"]
