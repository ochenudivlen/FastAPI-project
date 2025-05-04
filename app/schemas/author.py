from pydantic import BaseModel

class AuthorBase(BaseModel):
    name: str
    bio: str | None = None

class Author(AuthorBase):
    id: int
    class Config:
        from_attributes = True