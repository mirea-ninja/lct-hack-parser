import pandas as pd
import requests
from fastapi.encoders import jsonable_encoder

from app.config import config
from app.models import ApartmentBase
from app.models.enums import RepairType, Segment, Walls
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
            radius=search.radius,
        )

        df = parse_analogs(address, search_params)

        addresses = df["address"].to_list()
        unique_addresses = list(set(addresses))

        cords = [get_address_cords(address) for address in unique_addresses]
        addresses_dict = dict(zip(unique_addresses, cords))

        df["lat"] = df["address"].map(addresses_dict).apply(lambda x: x[0])
        df["lon"] = df["address"].map(addresses_dict).apply(lambda x: x[1])

        apartments = [
            ApartmentBase(
                address=a["address"],
                link=a["url"],
                lat=a["lat"],
                lon=a["lon"],
                rooms=a["rooms"],
                segment=Segment(a["segment"]),
                floors=a["floors"],
                walls=None if pd.isna(a["wall_material"]) else Walls(a["wall_material"]),
                floor=a["floor"],
                apartment_area=a["area"],
                kitchen_area=None if pd.isna(a["kitchen_area"]) else a["kitchen_area"],
                has_balcony=None if pd.isna(a["balcony"]) else bool(a["balcony"]),
                distance_to_metro=None if pd.isna(a["metro"]) else a["metro"],
                quality=None if pd.isna(a["repair"]) else RepairType(a["repair"]),
                m2price=a["price"] / a["area"],
                price=a["price"],
            )
            for a in df.to_dict(orient="records")
        ]

        headers = {
            "Authorization": f"Bearer {config.BACKEND_AUTH_TOKEN}",
        }

        response = requests.post(
            f"{config.BACKEND_API_URL}/query/{search.query_id}/subquery/{search.subquery_id}/analogs",
            headers=headers,
            json=jsonable_encoder(apartments),
        )

        return apartments
