from fastapi import APIRouter
from sqlalchemy import select, insert
from app.schemas.facilities import FacilityIn, FacilityOut
from app.routers.dependencies import db
from app.models import FacilitiesOrm

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get('/', response_model=list[FacilityOut])
async def get_facilities(db: db):
    facilities = await db.scalars(select(FacilitiesOrm))
    return facilities


@router.post('/', response_model=FacilityOut)
async def create_facility(db: db, facility_in: FacilityIn):
    facility = await db.scalar(insert(FacilitiesOrm).values(**facility_in.model_dump()).returning(FacilitiesOrm))
    await db.commit()
    return facility
