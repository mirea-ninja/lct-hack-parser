from __future__ import annotations

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JOSEError

from app.config import config

bearer_scheme = HTTPBearer()


def verify_access_token(access_token: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        jwt.decode(
            access_token.credentials,
            config.BACKEND_JWT_SECRET,
            algorithms=[config.BACKEND_JWT_ALGORITHM],
            options={"verify_aud": False},
        )
    except JOSEError:
        raise HTTPException(401, "Неверный токен авторизации", headers={"WWW-Authenticate": "Bearer"})
