from fastapi import FastAPI
from app.routers import hotels, rooms, auth, bookings


app = FastAPI()

app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)