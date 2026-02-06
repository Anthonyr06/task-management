from datetime import datetime
from uuid import UUID
from typing import Optional, List

from pydantic import BaseModel
from src.models.enums import TaskStatus, TaskPriority
from ._base import ORMModel
from .user import UserRef

class TaskCreate(BaseModel):
    project_id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.to_do
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[datetime] = None
    assignee_ids: List[UUID] = [] 

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    assignee_ids: Optional[List[UUID]] = None

class TaskOut(ORMModel):
    id: UUID
    project_id: UUID
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    assignees: List[UserRef] = []