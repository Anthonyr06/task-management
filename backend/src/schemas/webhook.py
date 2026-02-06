from datetime import datetime
from uuid import UUID
from typing import List

from pydantic import BaseModel, AnyHttpUrl
from ._base import ORMModel

class WebhookCreate(BaseModel):
    project_id: UUID
    url: AnyHttpUrl
    events: List[str]
    secret: str
    is_active: bool = True

class WebhookUpdate(BaseModel):
    is_active: bool
    
class WebhookOut(ORMModel):
    id: UUID
    project_id: UUID
    url: str
    events: List[str]
    secret: str
    is_active: bool
    created_at: datetime
    