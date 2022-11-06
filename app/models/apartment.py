from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, HttpUrl

from .enums.apartment import RepairType, Segment, Walls


class ApartmentBase(BaseModel):
    address: str
    link: Optional[HttpUrl] = None
    lat: Decimal
    lon: Decimal
    rooms: int
    segment: Segment
    floors: int
    walls: Optional[Walls] = None
    floor: int
    apartment_area: Decimal
    kitchen_area: Optional[Decimal] = None
    has_balcony: Optional[bool] = None
    distance_to_metro: Optional[int] = None
    quality: Optional[RepairType] = None
    m2price: Optional[Decimal] = None
    price: Optional[int] = None
