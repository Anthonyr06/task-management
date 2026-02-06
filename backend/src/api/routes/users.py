from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.api.dependencies.auth import get_current_user
from src.schemas.user import UserOut
from src.models.user import User  

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserOut)
def me(current_user=Depends(get_current_user)):
    return current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserOut])
def list_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return db.query(User).order_by(User.email.asc()).all()
