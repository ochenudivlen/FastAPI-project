"""
Маркер, который сообщает интерпретатору, что каталог содержит код для модуля Python.
"""

from .user import get_user_by_username, get_user_by_email, create_user
from .author import get_author, create_author, update_author, delete_author
from .book import get_book, create_book
from .genre import get_genre_by_name, create_genre, get_genres, delete_genre, get_genre
from .review import create_review, get_reviews_by_book

__all__ = [
    "get_user_by_username", "get_user_by_email", "create_user",
    "get_author", "create_author", "update_author", "delete_author",
    "get_book", "create_book",
    "get_genre_by_name", "create_genre", "get_genres", "delete_genre", "get_genre",
    "create_review", "get_reviews_by_book"
]
