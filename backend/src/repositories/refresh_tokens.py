from datetime import datetime, timezone
from sqlalchemy.orm import Session

from src.models.refresh_token import RefreshToken


def store_refresh_token(
    db: Session, *, user_id, jti: str, expires_at: datetime
) -> RefreshToken:
    rt = RefreshToken(user_id=user_id, jti=jti, expires_at=expires_at)
    db.add(rt)
    db.commit()
    db.refresh(rt)
    return rt


def get_active_refresh_token(db: Session, jti: str) -> RefreshToken | None:
    return (
        db.query(RefreshToken)
        .filter(RefreshToken.jti == jti, RefreshToken.revoked_at.is_(None))
        .first()
    )


def revoke_refresh_token(db: Session, token: RefreshToken) -> None:
    token.revoked_at = datetime.now(timezone.utc)
    db.add(token)
    db.commit()