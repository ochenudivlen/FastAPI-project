"""
Набор интеграционных тестов для проверки работоспособности API.
"""

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal

client = TestClient(app)
session = SessionLocal()


def test_create_book_unauthorized():
    """
    Тест на создание книги без авторизации.
    """
    response = client.post("/api/books/", json={
        "title": "Unauthorized Book",
        "author_id": 1
    })
    assert response.status_code == 401


def test_get_nonexistent_book():
    """
    Тест на получение несуществующей книги.
    """
    response = client.get("/api/books/9999")
    assert response.status_code == 404


def test_full_flow():
    """
    Интеграционный тест полного цикла действий: регистрация → авторизация → создание → отзыв.
    """
    # Регистрация пользователя
    user_data = {
        "username": "testuser",
        "password": "Str0ngP@ss",
        "email": "test@example.com"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200

    # Авторизация
    login_data = {
        "username": "testuser",
        "password": "Str0ngP@ss"
    }
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]

    # Создание автора
    author_data = {"name": "Test Author", "bio": "Test Bio"}
    response = client.post("/authors/",
                           headers={"Authorization": f"Bearer {token}"},
                           json=author_data
                           )
    author_id = response.json()["id"]

    # Создание книги
    book_data = {
        "title": "Test Book",
        "publication_year": 2023,
        "isbn": "123-4567890123",
        "author_id": author_id
    }
    response = client.post("/books/",
                           headers={"Authorization": f"Bearer {token}"},
                           json=book_data
                           )
    book_id = response.json()["id"]

    # Добавление отзыва
    review_data = {
        "rating": 5,
        "comment": "Excellent book",
        "book_id": book_id
    }
    response = client.post("/reviews/",
                           headers={"Authorization": f"Bearer {token}"},
                           json=review_data
                           )
    assert response.status_code == 200

    # Проверка рейтинга
    response = client.get(f"/books/top-rated/")
    assert response.status_code == 200
    assert any(book["id"] == book_id for book in response.json())