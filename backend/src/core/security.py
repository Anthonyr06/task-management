from datetime import datetime, timedelta, timezone
from typing import Any, Dict
import uuid

from jose import jwt
from passlib.context import CryptContext

from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd_context.hash(p)

def verify_password(p: str, phash: str) -> bool:
    return pwd_context.verify(p, phash)

def create_access_token(sub: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(minutes=settings.jwt_access_expires_min)
    payload = {"sub": sub, "role": role, "type": "access", "iat": int(now.timestamp()), "exp": exp}
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def create_refresh_token(sub: str) -> tuple[str, str, datetime]:
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=settings.jwt_refresh_expires_days)
    jti = uuid.uuid4().hex
    payload = {"sub": sub, "type": "refresh", "jti": jti, "iat": int(now.timestamp()), "exp": exp}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token, jti, exp