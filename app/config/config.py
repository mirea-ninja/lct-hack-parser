from __future__ import annotations

from functools import lru_cache
from typing import List

from dotenv import find_dotenv
from pydantic import BaseSettings


class _Settings(BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Config(_Settings):
    # Debug
    DEBUG: bool

    # Backend
    BACKEND_TTILE: str
    BACKEND_DESCRIPTION: str
    BACKEND_PREFIX: str

    BACKEND_HOST: str
    BACKEND_PORT: int
    BACKEND_RELOAD: bool

    BACKEND_CORS_ORIGINS: List = ["*"]

    BACKEND_JWT_SECRET: str
    BACKEND_JWT_ALGORITHM: str

    BACKEND_DADATA_TOKEN: str

    BACKEND_AUTH_TOKEN: str
    BACKEND_API_URL: str


@lru_cache()
def get_config(env_file: str = ".env") -> Config:
    return Config(_env_file=find_dotenv(env_file))
