from fastapi import FastAPI
from app.routers import hotels, rooms, auth


app = FastAPI()

app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(auth.router)