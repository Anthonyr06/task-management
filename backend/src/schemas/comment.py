from datetime import datetime
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel
from ._base import ORMModel
from .user import UserRef

class CommentCreate(BaseModel):
    task_id: UUID
    content: str
    mentions: Optional[List[UUID]] = None 

class CommentOut(ORMModel):
    id: UUID
    task_id: UUID
    author_id: Optional[UUID]
    content: str
    mentions: Optional[List[UUID]]
    created_at: datetime
    updated_at: datetime

    author: Optional[UserRef] = None