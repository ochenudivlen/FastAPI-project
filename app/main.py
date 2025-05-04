from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import book, author, genre, user, review  # noqa: F401
from app.api import (
    books_router,
    authors_router,
    genres_router,
    auth_router,
    reviews_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Catalog API",
    description="REST API для управления каталогом книг",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(books_router, prefix="/api/books", tags=["Books"])
app.include_router(authors_router, prefix="/api/authors", tags=["Authors"])
app.include_router(genres_router, prefix="/api/genres", tags=["Genres"])
app.include_router(reviews_router, prefix="/api/reviews", tags=["Reviews"])