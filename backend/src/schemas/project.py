from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from typing import Optional

from src.models.enums import ProjectStatus
from ._base import ORMModel

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.active

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None

class ProjectOut(ORMModel):
    id: UUID
    name: str
    description: Optional[str]
    status: ProjectStatus
    owner_id: UUID
    created_at: datetime
    updated_at: datetime