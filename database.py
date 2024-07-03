from typing import Optional
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import os

load_dotenv()


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')

# Асинк постгрес
DATABASE_URL = ('postgresql+asyncpg://'
                f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
                f'@{POSTGRES_HOST}/{POSTGRES_DB_NAME}')
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)
new_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Model(DeclarativeBase):
    pass


class MemeOrm(Model):
    __tablename__ = "memes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
