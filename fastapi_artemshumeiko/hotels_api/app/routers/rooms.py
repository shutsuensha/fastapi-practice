from fastapi import APIRouter, status, HTTPException, Query
from app.routers.dependencies import db
from app.schemas.rooms import RoomIn, RoomOut, RoomPatch
from sqlalchemy import insert, select, func, delete, update, not_, or_, and_
from app.models import RoomsOrm, HotelsOrm, BookingsOrm
from datetime import date

router = APIRouter(prefix="/hotels", tags=["rooms"])


@router.get("/{hotel_id}/rooms", response_model=list[RoomOut])
async def get_rooms(hotel_id: int, db: db, date_from: date = Query(), date_to: date = Query()):
    hotel = await db.scalar(select(HotelsOrm).where(HotelsOrm.id == hotel_id))
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='hotel not found'
        )
    
    query = select(RoomsOrm).where(
        RoomsOrm.hotel_id == hotel_id,
        not_(
            select(BookingsOrm.room_id)
            .where(
                BookingsOrm.room_id == RoomsOrm.id,
                or_(
                    and_(
                        BookingsOrm.date_from <= date_to,
                        BookingsOrm.date_to >= date_from
                    ),
                    and_(
                        BookingsOrm.date_from >= date_from,
                        BookingsOrm.date_to <= date_to
                    )
                )
            ).exists()
        )
    )
    rooms = await db.scalars(query)
    return rooms    


@router.get("/{hotel_id}/rooms/{room_id}", response_model=RoomOut)
async def get_room(hotel_id: int, room_id: int, db: db):
    hotel = await db.scalar(select(HotelsOrm).where(HotelsOrm.id == hotel_id))
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='hotel not found'
        )
    room = await db.scalar(select(RoomsOrm).where(RoomsOrm.hotel_id == hotel_id, RoomsOrm.id == room_id))
    if room is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='room not found'
        )
    return room


@router.post("/{hotel_id}/rooms", response_model=RoomOut, status_code=status.HTTP_201_CREATED)
async def create_room(hotel_id: int, db: db, room_in: RoomIn):
    hotel = await db.scalar(select(HotelsOrm).where(HotelsOrm.id == hotel_id))
    if hotel is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='hotel not found'
        )
    room = await db.scalar(insert(RoomsOrm).values(hotel_id=hotel_id, **room_in.model_dump()).returning(RoomsOrm))
    await db.commit()
    return room


@router.put("/{hotel_id}/rooms/{room_id}", response_model=RoomOut)
async def edit_room(hotel_id: int, room_id: int, db: db, room_in: RoomIn):
    await get_room(hotel_id, room_id, db)
    room = await db.scalar(update(RoomsOrm)
                           .where(RoomsOrm.hotel_id == hotel_id, RoomsOrm.id == room_id)
                           .values(hotel_id=hotel_id, **room_in.model_dump())
                           .returning(RoomsOrm))
    await db.commit()
    return room



@router.patch("/{hotel_id}/rooms/{room_id}", response_model=RoomOut)
async def partially_edit_room(hotel_id: int, room_id: int, db: db, room_in: RoomPatch):
    await get_room(hotel_id, room_id, db)
    room = await db.scalar(update(RoomsOrm)
                           .where(RoomsOrm.hotel_id == hotel_id, RoomsOrm.id == room_id)
                           .values(hotel_id=hotel_id, **room_in.model_dump(exclude_unset=True))
                           .returning(RoomsOrm))
    await db.commit()
    return room



@router.delete("/{hotel_id}/rooms/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(hotel_id: int, room_id: int, db: db):
    await get_room(hotel_id, room_id, db)
    await db.execute(delete(RoomsOrm).where(RoomsOrm.hotel_id == hotel_id, RoomsOrm.id == room_id))
    await db.commit()
