from __future__ import annotations

import requests

from app.config import config

DADATA_API_KEY = config.BACKEND_DADATA_TOKEN


def get_address_cords(address: str) -> tuple:
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
    headers = {
        "Authorization": f"Token {DADATA_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, headers=headers, json={"query": address})
    if response.status_code != 200:
        raise ValueError(f"Ошибка получения координат по адресу {address}") from response.raise_for_status()

    resp = response.json()
    if resp["suggestions"]:
        return (
            float(resp["suggestions"][0]["data"]["geo_lat"]),
            float(resp["suggestions"][0]["data"]["geo_lon"]),
        )
    return None, None
