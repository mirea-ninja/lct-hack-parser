from pydantic import BaseModel

from app.models.enums import Segment, Walls


class SearchBase(BaseModel):
    address: str
    rooms: int
    segment: Segment
    floors: int
    walls: Walls
