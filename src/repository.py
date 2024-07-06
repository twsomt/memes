import uuid

from fastapi import UploadFile, status
from sqlalchemy import select

from src.custom_exceptions import MemeNotFound
from src.database import MemeOrm, new_session
from src.decorators import handle_exceptions, async_cache
from src.functions import extract_relative_path, translit
from src.minio.minio_client import delete_image_from_minio, upload_image_to_minio
from src.schemas import Smeme, SmemeAdd, SmemeDelete, SmemeUpdate


class MemeRepository:

    @classmethod
    @handle_exceptions
    async def add_one(
        cls,
        data: SmemeAdd,
        image: UploadFile
    ) -> Smeme:
        async with new_session() as session:
            unique_id = uuid.uuid4()
            image_filename = await translit(image.filename)
            filename = f"{unique_id}--{image_filename}"
            image_url = await upload_image_to_minio(
                image.file, filename)
            meme_dict = data.model_dump()
            meme_dict['image_path'] = image_url
            meme = MemeOrm(**meme_dict)
            session.add(meme)
            await session.flush()
            await session.commit()
            meme_schema = Smeme.model_validate(meme)
            return meme_schema

    @classmethod
    @handle_exceptions
    @async_cache(ttl=60)
    async def get_all(
        cls,
        offset: int = 0,
        limit: int = 10
    ) -> list[Smeme]:
        async with new_session() as session:
            query = select(MemeOrm).offset(offset).limit(limit)
            result = await session.execute(query)
            meme_models = result.scalars().all()
            meme_schemas = [Smeme.model_validate(
                meme_model) for meme_model in meme_models]
            return meme_schemas

    @classmethod
    @handle_exceptions
    @async_cache(ttl=60)
    async def get_one(
        cls,
        meme_id: int
    ) -> Smeme:
        async with new_session() as session:
            query = select(MemeOrm).where(MemeOrm.id == meme_id)
            result = await session.execute(query)
            meme_model = result.scalars().first()
            if not meme_model:
                raise MemeNotFound()
            meme_schema = Smeme.model_validate(meme_model)
            return meme_schema

    @classmethod
    @handle_exceptions
    async def update_one(
        cls,
        update_data: SmemeUpdate,
        image: UploadFile = None
    ) -> Smeme:
        async with new_session() as session:
            meme_id = update_data.id
            query = select(MemeOrm).where(MemeOrm.id == meme_id)
            result = await session.execute(query)
            meme_model = result.scalars().first()
            if not meme_model:
                raise MemeNotFound()

            if image:
                unique_id = uuid.uuid4()
                filename = f"{update_data.description or 'meme'}-{unique_id}-{image.filename}"
                image_url = await upload_image_to_minio(image.file, filename)
                update_data_dict = update_data.model_dump(exclude_unset=True)
                update_data_dict['image_path'] = image_url
            else:
                update_data_dict = update_data.model_dump(exclude_unset=True)

            for key, value in update_data_dict.items():
                setattr(meme_model, key, value)

            await session.commit()
            await session.refresh(meme_model)
            meme_schema = Smeme.model_validate(meme_model)
            return meme_schema

    @classmethod
    async def delete_one(cls, data: SmemeDelete) -> dict:
        async with new_session() as session:
            # Находим мем по ID
            query = select(MemeOrm).where(MemeOrm.id == data)
            result = await session.execute(query)
            meme_model = result.scalars().first()

            if not meme_model:
                raise MemeNotFound("Meme not found")

            # Извлекаем путь к изображению и удаляем его из MinIO
            image_path = meme_model.image_path
            filename = await extract_relative_path(image_path)
            print(f'Удаляем изображение из MinIO: {filename}')
            await delete_image_from_minio(filename)

            # Удаляем объект из базы данных
            await session.delete(meme_model)
            await session.commit()

            return {"status": "success",
                    "status_code": status.HTTP_204_NO_CONTENT}
