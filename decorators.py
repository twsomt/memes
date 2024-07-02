import functools

from fastapi import HTTPException, status

from custom_exceptions import MemeNotFound


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
