import os

from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

load_dotenv()

MINIO_URL = os.getenv('MINIO_URL')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME')

if not all([MINIO_URL, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME]):
    raise ValueError(
        "Переменные конфига MinIO установлены неверно."
    )

# Инициализация клиента Minio
minio_client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


async def upload_image_to_minio(file, filename: str) -> str:
    """
    Загружает изображение в MinIO и возвращает его URL.

    Аргументы:
        file: Файл изображения для загрузки.
        filename: Имя которое будет использовано для загруженного файла.
    """

    # Проверяем есть ли такая корзина и создаем если нет
    found = minio_client.bucket_exists(MINIO_BUCKET_NAME)
    if not found:
        minio_client.make_bucket(MINIO_BUCKET_NAME)
        print("Создана корзина", MINIO_BUCKET_NAME)
    else:
        print("Корзина", MINIO_BUCKET_NAME, "уже существует")

    # Загружаем мемес
    try:
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            filename,
            file,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        return f"{MINIO_URL}/{MINIO_BUCKET_NAME}/{filename}"
    except S3Error as err:
        print(f"Не удалось загрузить {filename} в MinIO: {err}")
        raise


async def delete_image_from_minio(filename: str) -> None:
    """
    Удаляет изображение из MinIO.

    Аргументы:
        filename: Имя файлла который надо удалить.

    """
    # Сразу удаляем мем
    # Если и корзины такой нет то зарейзится ошибка
    try:
        minio_client.remove_object(MINIO_BUCKET_NAME, filename)
    except S3Error as err:
        print(f"Не удалось удалить {filename} из MinIO: {err}")
        raise
