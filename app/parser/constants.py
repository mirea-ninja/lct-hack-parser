from datetime import datetime
from enum import Enum


class Walls(Enum):
    BRICK = "кирпич"
    PANEL = "панель"
    MONOLITH = "монолит"


class Segment(Enum):
    NEW = "новостройка"
    MODERN = "современное жилье"
    OLD = "старый жилой фонд"

    def get_min_max_years(self) -> tuple[int, int]:
        if self == Segment.NEW:
            return 2020, datetime.now().year
        elif self == Segment.MODERN:
            return 1989, 2020
        elif self == Segment.OLD:
            return 0, 1989


class RepairType(Enum):
    WITHOUT_REPAIR = "без отделки"
    MUNICIPAL_REPAIR = "муниципальный ремонт"
    MODERN_REPAIR = "современная ремонт"
