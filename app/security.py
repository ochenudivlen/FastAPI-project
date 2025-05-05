"""
Реализация функционала безопасности: шифрования паролей и работы с JWT-токенами.
"""

import os
from datetime import datetime, timedelta
from typing import Optional

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

# Загрузка секретного ключа и алгоритма шифрования из переменных окружения
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")

if not SECRET_KEY or not ALGORITHM:
    raise RuntimeError("Missing environment variables SECRET_KEY or JWT_ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет совпадение введённого пароля с сохранённым хэшированным значением.

    Arguments:
        plain_password (str): Исходный пароль.
        hashed_password (str): Хэшированный пароль из базы данных.

    Returns:
        bool: Результат сравнения паролей.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Генерирует хэшированное представление пароля.

    Arguments:
        password (str): Пароль, подлежащий хэшированию.

    Returns:
        str: Хэшированная форма пароля.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Формирует JWT-токен с заданными данными и сроком действия.

    Arguments:
        data (dict): Данные для включения в токен.
        expires_delta (Optional[timedelta], optional): Срок жизни токена. По умолчанию None.

    Returns:
        str: Закодированный JWT-токен.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[dict]:
    """
    Декодирует JWT-токен и возвращает его данные.

    Arguments:
        token (str): JWT-токен для декодирования.

    Returns:
        Optional[dict]: Расшифрованные данные токена или None в случае ошибки.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
