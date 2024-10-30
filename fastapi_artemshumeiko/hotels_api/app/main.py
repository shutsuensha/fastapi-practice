from fastapi import FastAPI
from app.routers import hotels, rooms, auth, bookings, facilities


app = FastAPI()

app.include_router(auth.router)
app.include_router(hotels.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
app.include_router(facilities.router)