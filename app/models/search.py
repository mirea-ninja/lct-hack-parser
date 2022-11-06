from uuid import UUID

from pydantic import BaseModel

from app.models.enums import Segment, Walls


def to_camel_case(string: str) -> str:
    components = string.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class SearchBase(BaseModel):
    query_id: UUID
    subquery_id: UUID
    address: str
    rooms: int
    segment: Segment
    floors: int
    walls: Walls
    radius: int = 1000

    class Config:
        alias_generator = to_camel_case
