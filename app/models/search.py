from uuid import UUID

from pydantic import BaseModel

from app.models.enums import Segment, Walls


class SearchBase(BaseModel):
    query_id: UUID
    subquery_id: UUID
    address: str
    rooms: int
    segment: Segment
    floors: int
    walls: Walls
    radius: int = 1000
