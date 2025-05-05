"""
Определение кастомных исключений HTTP для обработки ошибок в приложении.
"""

from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    """
    Базовый класс для кастомных HTTP-исключений.
    """

    def __init__(self, status_code: int, detail: str, headers: dict = None):
        """
        Конструктор исключения.

        Arguments:
            status_code (int): HTTP-код статуса.
            detail (str): Детальная информация об ошибке.
            headers (dict, optional): Дополнительные заголовки HTTP. По умолчанию пусто.
        """
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers or {}


class BookNotFoundError(CustomHTTPException):
    """
    Исключительное событие, возникающее при отсутствии запрашиваемой книги.
    """

    def __init__(self):
        """
        Конструктор исключения "Книга не найдена".
        """
        super().__init__(
            status_code=404,
            detail="Book not found",
            headers={"X-Error": "BookNotFound"}
        )
