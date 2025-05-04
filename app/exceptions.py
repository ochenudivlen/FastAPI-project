from fastapi import HTTPException

class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str, headers: dict = None):
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers or {}

class BookNotFoundError(CustomHTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Book not found",
            headers={"X-Error": "BookNotFound"}
        )