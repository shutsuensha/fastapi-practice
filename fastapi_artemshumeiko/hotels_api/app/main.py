from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routers import hotels, rooms, auth, bookings, facilities, images

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from app.config import settings
from fastapi_cache.decorator import cache


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(facilities.router)
app.include_router(images.router)