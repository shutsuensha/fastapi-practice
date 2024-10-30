from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select, insert
from app.models import BookingsOrm, RoomsOrm
from app.routers.dependencies import user_id, db
from app.schemas.bookings import BookingIn, BookingOut

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get('/', response_model=list[BookingOut])
async def get_bookings(db: db):
    bookings = await db.scalars(select(BookingsOrm))
    return bookings


@router.get('/me', response_model=list[BookingOut])
async def get_my_bookings(user_id: user_id, db: db):
    bookings = await db.scalars(select(BookingsOrm).where(BookingsOrm.user_id == user_id))
    return bookings


@router.post('/', response_model=BookingOut)
async def add_booking(user_id: user_id, db: db, booking_in: BookingIn):
    room_id = booking_in.room_id
    room = await db.scalar(select(RoomsOrm).where(RoomsOrm.id == room_id))
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='room not found'
        )
    total_price = room.price * (booking_in.date_to - booking_in.date_from).days
    booking = await db.scalar(insert(BookingsOrm)
                                .values(user_id=user_id, 
                                     price=total_price, 
                                     **booking_in.model_dump())
                                .returning(BookingsOrm))
    await db.commit()
    return booking