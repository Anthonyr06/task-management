from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from src.repositories.users import get_user_by_email, create_user, get_user_by_id
from src.repositories.refresh_tokens import (
    store_refresh_token,
    get_active_refresh_token,
    revoke_refresh_token,
)

# -----------------------
# Register
# -----------------------
def register(db: Session, *, email: str, password: str, role: str):
    existing = get_user_by_email(db, email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    phash = hash_password(password)
    user = create_user(db, email=email, password_hash=phash, role=role)
    return user


# -----------------------
# Login
# -----------------------
def login(db: Session, *, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access = create_access_token(sub=str(user.id), role=user.role)
    refresh, jti, exp = create_refresh_token(sub=str(user.id))

    store_refresh_token(db, user_id=user.id, jti=jti, expires_at=exp.replace(tzinfo=None))

    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
    }

def refresh(db: Session, *, refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    token_type = payload.get("type")
    sub = payload.get("sub")
    jti = payload.get("jti")

    if token_type != "refresh" or not sub or not jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )

    # 1) verificar que el jti exista y no este revocado
    rt = get_active_refresh_token(db, jti)
    if not rt:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token revoked or unknown",
        )

    # 2) verificar expiracion
    now = datetime.now(timezone.utc)
    exp_claim = payload.get("exp")
    if not exp_claim or datetime.fromtimestamp(exp_claim, tz=timezone.utc) < now:
        revoke_refresh_token(db, rt)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    # 3) rotacion: revocar el token actual
    revoke_refresh_token(db, rt)

    # 4) emitir nuevos tokens
    user_id = UUID(sub)
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access = create_access_token(sub=str(user.id), role=user.role)
    new_refresh, new_jti, new_exp = create_refresh_token(sub=str(user.id))

    store_refresh_token(db, user_id=user.id, jti=new_jti, expires_at=new_exp.replace(tzinfo=None))

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
    }
