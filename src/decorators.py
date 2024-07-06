from typing import Dict
from functools import wraps
from cachetools import TTLCache
import functools

from fastapi import HTTPException, status

from src.custom_exceptions import MemeNotFound


def handle_exceptions(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except MemeNotFound as e:
            raise HTTPException(
                status_code=e.status_code,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    return wrapper


# Словарик для хранения кэшей как будто костыль
cache: Dict[str, TTLCache] = {}


def get_cache(key):
    """ Получаем кеш по ключу """
    if key not in cache:
        cache[key] = TTLCache(maxsize=128, ttl=60)
    return cache[key]


def async_cache(ttl=60):
    """ Кешируем с TTL """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            c = get_cache(key)
            if key in c:
                return c[key]
            result = await func(*args, **kwargs)
            c[key] = result
            return result
        return wrapper
    return decorator
