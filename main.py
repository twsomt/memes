from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from router import router as memes_router
from settings import DEBUG

# При дебаге после перезагрузки чистим БД
if DEBUG:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await delete_tables()
        await create_tables()
        yield

    app = FastAPI(lifespan=lifespan)
else:
    app = FastAPI()

app.include_router(memes_router)
