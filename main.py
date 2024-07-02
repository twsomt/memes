from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_tables, delete_tables
from router import router as memes_router
from settings import DEBUG

if DEBUG:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await delete_tables()
        print("База очищена")
        await create_tables()
        print("База готова к работе")
        yield
        print("Выключение")

    app = FastAPI(lifespan=lifespan)
else:
    app = FastAPI()

app.include_router(memes_router)
