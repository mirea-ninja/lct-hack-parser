from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from .enums.apartment import RepairType, Segment, Walls


class ApartmentBase(BaseModel):
    address: str = Field(example="Удальцова 5", description="Адрес квартиры")
    link: Optional[HttpUrl] = Field(
        None, example="https://www.cian.ru/sale/flat/23423423/", description="Ссылка на объявление"
    )
    lat: Decimal = Field(example=55.123456, description="Широта")
    lon: Decimal = Field(example=37.123456, description="Долгота")
    rooms: int = Field(example=2, description="Количество комнат")
    segment: Segment = Field(example="новостройка", description="Сегмент")
    floors: int = Field(example=5, description="Этажность дома")
    walls: Optional[Walls] = Field(None, example="кирпич", description="Материал стен")
    floor: int = Field(example=2, description="Этаж")
    apartment_area: Decimal = Field(None, example=50.0, description="Площадь квартиры")
    kitchen_area: Optional[Decimal] = Field(None, example=10.0, description="Площадь кухни")
    has_balcony: Optional[bool] = Field(None, example=True, description="Наличие балкона")
    distance_to_metro: Optional[int] = Field(None, example=5, description="Расстояние до метро")
    quality: Optional[RepairType] = Field(None, example="хорошее", description="Качество ремонта")
    m2price: Optional[int] = Field(None, example=100000, description="Цена за квадратный метр")
    price: Optional[int] = Field(None, example=5000000, description="Цена квартиры")
