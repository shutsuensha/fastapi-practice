from fastapi import FastAPI
from app.routers import hotels


app = FastAPI()

app.include_router(hotels.router)