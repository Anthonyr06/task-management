from datetime import datetime
from uuid import UUID
from pydantic import EmailStr, BaseModel

from ..models.enums import UserRole
from ._base import ORMModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.member

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserRef(ORMModel):
    id: UUID
    email: EmailStr
    role: UserRole

class UserOut(ORMModel):
    id: UUID
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime
    
class UserOut(BaseModel):
    id: UUID
    email: str
    role: str

    class Config:
        from_attributes = True