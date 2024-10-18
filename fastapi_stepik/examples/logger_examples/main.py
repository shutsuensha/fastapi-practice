from fastapi import FastAPI
from loguru import logger

app = FastAPI()

logger.add("info.log")


@app.get("/{name}")
async def main_page(name):
    logger.info("Hello from the root path")
    hello_world()
    return {"message": f"Hello {name}"}


def hello_world():
    logger.info("hello() called!")