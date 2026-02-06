from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas.user import UserCreate, UserLogin, UserOut
from src.schemas.auth import TokenPair
from src.services.auth import register, login, refresh
from src.core.rate_limit import rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def register_route(payload: UserCreate, db: Session = Depends(get_db)):
    user = register(db, email=payload.email, password=payload.password, role=payload.role.value)
    return user


@router.post("/login", response_model=TokenPair)
def login_route(payload: UserLogin, db: Session = Depends(get_db)):
    rate_limit(f"login:{payload.email}", limit=10, window_seconds=60)
    return login(db, email=payload.email, password=payload.password)


@router.post("/refresh", response_model=TokenPair)
def refresh_route(refresh_token: str, db: Session = Depends(get_db)):
    tokens = refresh(db, refresh_token=refresh_token)
    return tokens