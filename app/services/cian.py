import pandas as pd

from app.models import ApartmentBase
from app.models.enums import Segment, Walls, RepairType
from app.models.search import SearchBase
from app.parser.cian_api import SearchParams, parse_analogs


class CianService:
    @staticmethod
    def start_parse(search: SearchBase) -> list[ApartmentBase]:
        address = "г. Москва, ул. Ватутина, д. 11"

        search_params = SearchParams(
            rooms=2,
            segment=Segment.MODERN,
            walls=Walls.BRICK,
            floors=22,
        )
        df = parse_analogs(address, search_params)
        apartments = []
        for a in df.to_dict(orient="records"):
            apartments.append(
                ApartmentBase(
                    address=a["address"],
                    lat=0,
                    lon=0,
                    rooms=a["rooms"],
                    segment=a["segment"],
                    floors=a["floors"],
                    walls=a["wall_material"] if not pd.isna(a["wall_material"]) else Walls.UNSET,
                    floor=a["floor"],
                    apartment_area=a["area"],
                    kitchen_area=a["kitchen_area"] if not pd.isna(a["kitchen_area"]) else 0,
                    has_balcony=True if a["balcony"] else False,
                    distance_to_metro=a["metro"],
                    quality=a["repair"],
                    m2price=0,
                    price=a["price"],
                )
            )
        return apartments
