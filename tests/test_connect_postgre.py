# Проверяем коннект с постгресом
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import pytest
import sqlalchemy as sa

load_dotenv()


POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB_NAME = os.getenv('POSTGRES_DB_NAME')

if not all([POSTGRES_USER,
            POSTGRES_PASSWORD,
            POSTGRES_HOST,
            POSTGRES_DB_NAME]
           ):
    raise ValueError(
        "Переменные конфига PostgreSQL установлены неверно."
    )

# Асинк постгрес
DATABASE_URL = ('postgresql+asyncpg://'
                f'{POSTGRES_USER}:{POSTGRES_PASSWORD}'
                f'@{POSTGRES_HOST}/{POSTGRES_DB_NAME}')
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.mark.asyncio
async def test_postgres_connection():
    async with async_session() as session:
        result = await session.execute(sa.text("SELECT 1"))
        assert result.scalar() == 1
