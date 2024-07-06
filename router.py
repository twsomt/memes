from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from custom_exceptions import MemeNotFound
from repository import MemeRepository
from schemas import Smeme, SmemeAdd, SmemeDelete, SmemeUpdate
from settings import PREFIX, TAGS

router = APIRouter(
    prefix=PREFIX,
    tags=[TAGS],
)


@router.get("")
async def get_memes(
    offset: int = 0,
    limit: int = 10
) -> list[Smeme]:
    """
    Возвращает список мемов с использованием пагинации.

    Аргументы:
        offset (int, optional): Сдвиг (начиная с какого мемаса возвращать). По умолчанию 0.
        limit (int, optional): Лимит мемов (сколько вернуть). По умолчанию 10.

    Возвращает:
        list[Smeme]: Список объектов Smeme, представляющих мемы.

    Пример:
        Пример запроса для получения первых 10 мемов:

            GET /{PREFIX}/get_memes?offset=0&limit=10
    """
    memes = await MemeRepository.get_all(offset=offset, limit=limit)
    return memes


@router.get("/{meme_id}")
async def get_meme(
    meme_id: int
) -> Smeme:
    """
    Получает информацию о конкретном меме по его ID.

    Аргументы:
        meme_id (int): ID мема.

    Возвращает:
        Smeme: Объект Smeme, представляющий запрошенный мем.

    Пример:
        Пример запроса для получения информации о меме с ID = 1:

            GET /{PREFIX}/{meme_id}
    """
    meme = await MemeRepository.get_one(meme_id)
    if meme is None:
        raise MemeNotFound()
    return meme


@router.post("")
async def add_meme(
    data: Annotated[SmemeAdd, Depends()],
    image: UploadFile = File()
) -> Smeme:
    """
    Добавляет новый мем.

    Аргументы:
        meme (SmemeAdd): Данные нового мема для добавления.

    Возвращает:
        Smeme: Объект Smeme, представляющий только что добавленный мем.

    Пример:
        Пример запроса для добавления нового мема:

            POST /{PREFIX}/add_meme

            {
                "field1": "value1",
                "field2": "value2",
                ...
            }
    """
    new_meme = await MemeRepository.add_one(data, image)
    return new_meme


@router.put("/{meme_id}")
async def update_meme(
    data: Annotated[SmemeUpdate, Depends()],
    image: UploadFile = File(None)
) -> Smeme:
    """
    Обновляет информацию о конкретном меме по его ID.

    Аргументы:
        meme_id (int): ID мема, который надо обновить.
        update_data (SmemeUpdate): Данные для обновления мема.

    Возвращает:
        Smeme: Обновленный объект Smeme, представляющий мем.

    Пример:
        Пример запроса для обновления информации о меме с ID = 1:

            PUT /{PREFIX}/{meme_id}

            {
                "field1": "new_value1",
                "field2": "new_value2",
                ...
            }
    """
    updated_meme = await MemeRepository.update_one(data, image)
    if updated_meme is None:
        raise MemeNotFound()
    return updated_meme


@router.delete("/{meme_id}")
async def delete_meme(
    data: Annotated[SmemeDelete, Depends()]
) -> dict:
    """
    Удаляет информацию о конкретном меме по его ID.

    Аргументы:
        meme_id (int): ID мема, который надо удалить.

    Возвращает:
        dict: Словарь с информацией об успешном удалении мема.

    Пример:
        Пример запроса для удаления мема с идентификатором 1:

            DELETE /{PREFIX}/{meme_id}
    """
    result = await MemeRepository.delete_one(data.id)
    return result
