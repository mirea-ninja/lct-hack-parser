from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ApartmentBase(BaseModel):
    address: str
    lat: Decimal
    lon: Decimal
    rooms: int
    segment: str
    floors: int
    walls: str
    floor: int
    apartment_area: int
    kitchen_area: int
    has_balcony: bool
    distance_to_metro: int
    quality: str
    m2price: Optional[Decimal] = 0
    price: Optional[int] = 0
