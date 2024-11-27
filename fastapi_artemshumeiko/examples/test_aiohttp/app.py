import asyncio
import time
import threading

from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Потоков: {threading.active_count()}")
    time.sleep(3)


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Потоков: {threading.active_count()}")
    await asyncio.sleep(3)


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)