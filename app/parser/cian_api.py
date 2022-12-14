from __future__ import annotations

import datetime
import os
import time
from dataclasses import dataclass
from enum import IntEnum
import math

import numpy as np
import pandas as pd
from geopy.distance import geodesic

import app.parser.driver as driver
from app.models.enums import RepairType, Segment, Walls
from app.parser.utils import get_address_cords


@dataclass(frozen=True)
class SearchParams:
    rooms: int  # Количество комнат
    segment: Segment  # Сегмент
    floors: int  # Этажность дома
    walls: Walls  # Материал стен дома
    radius: int = 1000  # Радиус поиска вокруг адреса


class URLType(IntEnum):
    OFFER_LIST = 1  # В виде списка
    EXPORT = 2  # Экспорт в Excel
    MAP = 3  # На карте


def get_segment(year: int) -> Segment:
    """Получить сегмент по году постройки дома

    Args:
        year (int): год постройки дома

    Returns:
        Segment: сегмент дома. До 2-х лет - новостройка, современное от 89-го года, старый жилой фонд - до 89-го года.
    """
    year_now = datetime.datetime.now().year

    if year_now - year < 2:
        return Segment.NEW
    elif year >= 1989:
        return Segment.MODERN

    return Segment.OLD


def _get_polygon_param(lat, lon, radius):
    polygon = [
        geodesic(kilometers=radius / 1000).destination(point=(lat, lon), bearing=angle) for angle in range(0, 360, 10)
    ]

    polygon = ",".join([f"{p.longitude}_{p.latitude}" for p in polygon])
    return polygon


def _get_bbox_param(lat, lon, radius):
    bbox = geodesic(kilometers=radius / 1000).destination(point=(lat, lon), bearing=0)
    bbox = ",".join(
        [
            f"{bbox.longitude}_{bbox.latitude}",
            f"{bbox.longitude}_{bbox.latitude}",
            f"{bbox.longitude}_{bbox.latitude}",
            f"{bbox.longitude}_{bbox.latitude}",
        ]
    )
    return bbox


def get_url_by_cords(
    lat: float,
    lon: float,
    params: SearchParams,
    radius: int = 1000,
    url_type: URLType = URLType.OFFER_LIST,
):
    """Рассчитывает url для запроса по координатам

    Args:
        lat (float): Широта центра
        lon (float): Долгота центра
        params (SearchParams): Параметры поиска
        radius (int, optional): Радиус поиска. По умолчанию 1000. Радиус поиска в метрах.
        url_type (URLType, optional): Тип генерируемой ссылки. По умолчанию URLType.OFFER_LIST.
    """

    # Параметры:
    # bbox - координаты левого верхнего и правого нижнего угла прямоугольника (для поиска в прямоугольнике)
    # center - координаты центра прямоугольника (для поиска в радиусе)
    # lat - широта центра прямоугольника
    # lon - долгота центра прямоугольника
    # radius - радиус поиска в метрах (для поиска в радиусе)

    # Параметры:
    # deal_type - тип сделки (продажа, аренда)
    # offer_type - тип предложения (квартиры, дома, земля)
    # region - регион (Москва - 1)
    # zoom - масштаб карты (от 0 до 19)
    # min_house_year - минимальный год постройки дома
    # max_house_year - максимальный год постройки дома
    # minfloorn - минимальный этаж
    # maxfloorn - максимальный этаж
    # house_material[0]=1 - материал стен дома (1 - кирпич, 2 - монолит, 3 - панель, 4-блочный, 5 - деревянный,
    # 6 - сталинский, 8 - кирпично-монолитный)

    # room1=1 - 1 комнатная
    # room2=1 - 2 комнатная
    # room3=1 - 3 комнатная
    # room4=1 - 4 комнатная
    # room5=1 - 5 комнатная
    # room6=1 - 6 комнатная
    # room9=1 - студия

    # Радиус земли в метрах

    cian_house_material = {
        Walls.BRICK: 1,
        Walls.MONOLITH: 2,
        Walls.PANEL: 3,
    }

    min_year, max_year = params.segment.get_min_max_years()

    try:
        rooms = {
            0: "room9=1",
            1: "room1=1",
            2: "room2=1",
            3: "room3=1",
            4: "room4=1",
            5: "room5=1",
            6: "room6=1",
        }[params.rooms]
    except KeyError as e:
        raise ValueError(f"Неподдерживаемое количество комнат: {params.rooms}") from e

    # # материал стен дома. Раскомментировать, если нужно
    # walls = f"house_material[0]={cian_house_material[params.walls]}"
    # # сдвоенный тип
    # if params.walls in [Walls.BRICK, Walls.MONOLITH]:
    #     walls += "&house_material[1]=8"
    walls = ""

    # год постройки
    year = f"min_house_year={min_year}&max_house_year={max_year}"

    # этажность
    floors = f"minfloorn={max(params.floors - 3, 1)}&maxfloorn={params.floors + 3}"

    url = ""
    if url_type == URLType.OFFER_LIST:
        url = (
            f"https://www.cian.ru/cat.php?center={lat},{lon}&deal_type=sale&engine_version=2&offer_type=flat"
            f"&origin=map&zoom=15&{rooms}&{walls}&{year}&{floors}"
        )

    elif url_type == URLType.EXPORT:
        url = (
            f"https://www.cian.ru/export/xls/offers/?deal_type=sale&engine_version=2&offer_type=flat&region=1"
            f"&{rooms}&{floors}&{year}&{walls}"
        )

    elif url_type == URLType.MAP:
        url = (
            f"https://www.cian.ru/map/?center={lat},{lon}&deal_type=sale&engine_version=2&offer_type=flat"
            f"&{rooms}&{walls}&{year}&{floors}"
        )

    polygon = _get_polygon_param(lat, lon, radius)
    bbox = _get_bbox_param(lat, lon, radius)

    if url_type != URLType.MAP:
        url += f"&bbox={bbox}"
    url += f"&in_polygon[0]={polygon}&origin=map&polygon_name[0]=Область поиска"

    return url.replace("&&", "&").replace("?&", "?")


def parse_analogs(address: str, search_params: SearchParams) -> pd.DataFrame:
    lat, lon = get_address_cords(address)

    url = get_url_by_cords(lat, lon, search_params, radius=search_params.radius, url_type=URLType.EXPORT)

    unique_folder_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    downloaded_file = os.path.join(f"/app/app/parser/data/{unique_folder_name}/offers.xlsx")

    time_passed = 0
    try:
        chromium = driver.create(unique_folder_name)
        chromium.get(url)

        while True:
            time.sleep(0.1)
            time_passed += 0.1

            if os.path.exists(downloaded_file):
                break
            if time_passed > 10:
                raise TimeoutError("Не удалось скачать файл")

    except Exception as e:
        raise e
    finally:
        chromium.quit()

    df = pd.read_excel(downloaded_file)

    if len(df) < 1:
        raise ValueError("Не найдено достаточного количества аналогов")

    columns = {
        "ID": "id",
        "Количество комнат": "rooms",
        "Тип": "type",
        "Метро": "metro",
        "Адрес": "address",
        "Площадь, м2": "area",
        "Дом": "house",
        "Парковка": "parking",
        "Цена": "price",
        "Телефоны": "phones",
        "Описание": "description",
        "Ремонт": "repair",
        "Площадь комнат, м2": "rooms_area",
        "Балкон": "balcony",
        "Окна": "windows",
        "Санузел": "toilet",
        "Есть телефон": "has_phone",
        "Высота потолков, м": "ceiling_height",
        "Лифт": "elevator",
        "Мусоропровод": "chute",
        "Ссылка на объявление": "url",
        "Название ЖК": "project_name",
    }

    df = df.rename(columns=columns)

    for column in columns.values():
        if column not in df.columns:
            df[column] = np.nan

    for column in [
        "id",
        "type",
        "parking",
        "phones",
        "description",
        "rooms_area",
        "windows",
        "toilet",
        "has_phone",
        "ceiling_height",
        "elevator",
        "project_name",
        "chute",
    ]:
        if column in df.columns:
            df = df.drop(columns=[column])

    df = pd.concat([df, df["address"].str.split(", ", expand=True)], axis=1)

    df = df.drop_duplicates()

    df["price"] = df["price"].apply(lambda x: int(x.split(" ")[0]))

    # Площадь кухни, м2
    df["kitchen_area"] = df["area"].apply(lambda x: float(x.split("/")[2]) if len(x.split("/")) == 3 else np.nan)

    # Площадь, м2. Указано в формате "55.0/31.3", где первое число - общая площадь, второе - жилая площадь,
    # или "55.0" - только общая площадь, или "53.1/33.4/7.2" - общая, жилая, кухня
    df["area"] = df["area"].apply(lambda x: float(x.split("/")[0]))

    # Может быть не указано. Иначе в формате "Балкон (1)", "Лоджия (1)"
    df["balcony"] = df["balcony"].apply(
        lambda x: x is not np.nan and ("балкон" in str(x).lower() or "лоджия" in str(x).lower())
    )

    # Удаленность от станции метро (в минутах ходьбы). Указано в 'метро'. Формат: "м. Кунцевская (5 мин пешком)".
    # Внутри скобок может быть написано "None" (ошибка разрабов Циана, наверное). Пример: "м. Кунцевская (None)"
    df["metro"] = df["metro"].apply(
        lambda x: int(x.split("(")[1].split(" ")[0])
        if x is not np.nan and x.split("(")[1].split(" ")[0] != "None"
        else np.nan
    )

    # Если без типа, то это студия
    df["rooms"] = df["rooms"].apply(lambda x: 0 if x is np.nan or x is None or x is math.nan else x)

    df = df.loc[
        df["rooms"].apply(lambda x: "аппартаменты" not in str(x).lower() and "апартаменты" not in str(x).lower())]

    # Количество комнат. Указано в 'rooms'. Формат: "2, Изолированная", где 2 - количество комнат.
    # Тип может быть не указан.
    df["rooms"] = df["rooms"].apply(lambda x: int(x.split(",")[0]) if "," in str(x) else x)

    # Этаж. Указан в 'house'. Формат: "9/14, Панельный", где 9 - этаж, 14 - этажность дома
    df["floor"] = df["house"].apply(lambda x: int(x.split("/")[0]) if x is not np.nan else np.nan)

    # Этажность дома
    df["floors"] = df["house"].apply(lambda x: int(x.split("/")[1].split(",")[0]) if x is not np.nan else np.nan)

    # Сегмент (search_params.segment)
    df["segment"] = df.apply(lambda x: search_params.segment.value, axis=1)

    # Материал стен. Указан в Указан в 'house'. Формат: "9/14, Панельный", где "Панельный" - материал стен.
    # Может быть не указан!
    df["wall_material"] = df["house"].apply(lambda x: x.split(",")[1].strip() if "," in str(x) else np.nan)

    # Ремонт. "Без ремонта" - без отделки, "Евроремонт" - современный, "Косметический" - муниципальный ремонт
    df["repair"] = df["repair"].apply(
        lambda x: RepairType.WITHOUT_REPAIR.value
        if "без ремонта" in str(x).lower()
        else RepairType.MODERN_REPAIR.value
        if "евроремонт" in str(x).lower() or "дизайнерский" in str(x).lower()
        else RepairType.MUNICIPAL_REPAIR.value
        if "косметический" in str(x).lower()
        else np.nan
    )

    df = df.loc[
        (df["wall_material"].isnull())
        | (
            search_params.walls == Walls.BRICK.value
            and df["wall_material"].apply(lambda x: "кирпичный" == str(x).lower() or "сталинский" == str(x).lower())
        )
        | (
            search_params.walls == Walls.MONOLITH.value
            and df["wall_material"].apply(lambda x: "монолитный" in str(x).lower())
        )
        | (
            search_params.walls == Walls.PANEL.value
            and df["wall_material"].apply(lambda x: "панельный" in str(x).lower() or "блочный" in str(x).lower())
        )
    ]

    df["wall_material"] = df["wall_material"].apply(
        lambda x: Walls.MONOLITH.value
        if "монолитный" in str(x).lower() or "монолитно-кирпичный" in str(x).lower()
        else Walls.PANEL.value
        if "панельный" in str(x).lower()
        else Walls.BRICK.value
        if "кирпичный" in str(x).lower()
        else np.nan
    )

    df = df.drop(columns=["house"])

    df.drop_duplicates(inplace=True)

    if len(df) > 10:
        df = df.loc[(df["kitchen_area"].notnull()) & (df["metro"].notnull())]

    os.remove(downloaded_file)

    return df
