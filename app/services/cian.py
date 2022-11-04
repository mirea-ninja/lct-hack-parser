import pandas as pd

from app.models import ApartmentBase
from app.models.enums import Walls
from app.models.search import SearchBase
from app.parser.cian_api import SearchParams, parse_analogs
from app.parser.utils import get_address_cords


class CianService:
    @staticmethod
    def start_parse(search: SearchBase) -> list[ApartmentBase]:
        address = search.address

        search_params = SearchParams(
            rooms=search.rooms,
            segment=search.segment,
            walls=search.walls,
            floors=search.floors,
        )

        df = parse_analogs(address, search_params)

        return [
            ApartmentBase(
                address=a["address"],
                lat=get_address_cords(a["address"])[0],
                lon=get_address_cords(a["address"])[1],
                rooms=a["rooms"],
                segment=a["segment"],
                floors=a["floors"],
                walls=Walls.UNSET if pd.isna(a["wall_material"]) else a["wall_material"],
                floor=a["floor"],
                apartment_area=a["area"],
                kitchen_area=-1 if pd.isna(a["kitchen_area"]) else a["kitchen_area"],
                has_balcony=bool(a["balcony"]),
                distance_to_metro=-1 if pd.isna(a["metro"]) else a["metro"],
                quality=a["repair"],
                m2price=-1,
                price=a["price"],
            )
            for a in df.to_dict(orient="records")
        ]
