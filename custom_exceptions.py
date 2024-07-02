from fastapi import status


class MemeNotFound(Exception):
    def __init__(self, message='Мем не найден'):
        self.message = message
        self.status_code = status.HTTP_404_NOT_FOUND
        super().__init__(self.message)

    def __str__(self):
        return self.message
