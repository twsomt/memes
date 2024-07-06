from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_tables, delete_tables
from src.router import router as memes_router
from src.settings import DEBUG

# При дебаге после перезагрузки чистим БД


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield

if DEBUG:
    app = FastAPI(lifespan=lifespan)
else:
    app = FastAPI()

app.include_router(memes_router)
