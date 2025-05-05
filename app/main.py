"""
Основной файл приложения REST API для каталога книг.
"""

from fastapi import FastAPI
from app.database import engine, Base

from app.api.books import router as books_router
from app.api.authors import router as authors_router
from app.api.genres import router as genres_router
from app.api.auth import router as auth_router
from app.api.reviews import router as reviews_router


# Создаёт таблицы в базе данных
Base.metadata.create_all(bind=engine)


# Настройка основного экземпляра приложения FastAPI
app = FastAPI(
    title="Book Catalog API",
    description="REST API для управления каталогом книг.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)


# Регистрация маршрутов
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(books_router, prefix="/api/books", tags=["Books"])
app.include_router(authors_router, prefix="/api/authors", tags=["Authors"])
app.include_router(genres_router, prefix="/api/genres", tags=["Genres"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])
