from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


def to_camel_case(string: str) -> str:
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class SearchBase(BaseModel):
    query_id: UUID = Field(example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", description="Идентификатор запроса")
    subquery_id: UUID = Field(example="a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11", description="Идентификатор подзапроса")
    address: str = Field(example="Удальцова 5", description="Адрес квартиры")
    rooms: int = Field(example=2, description="Количество комнат")
    segment: str = Field(example="новостройка", description="Сегмент")
    floors: int = Field(example=5, description="Этажность дома")
    walls: str = Field(example="кирпич", description="Материал стен")
    radius: Optional[int] = Field(example=1500, description="Радиус поиска")

    class Config:
        alias_generator = to_camel_case
