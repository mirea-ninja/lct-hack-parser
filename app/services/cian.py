from app.models.enums import Segment, Walls
from app.parser.cian_api import SearchParams, parse_analogs


class CianService:
    @staticmethod
    def start_parse():
        address = "г. Москва, ул. Ватутина, д. 11"

        search_params = SearchParams(
            rooms=2,
            segment=Segment.MODERN,
            walls=Walls.BRICK,
            floors=22,
        )
        df = parse_analogs(address, search_params)
        print(df)
        return df.to_json()
