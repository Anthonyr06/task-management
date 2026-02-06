from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.db import Base
from src.models.enums import TaskStatus, TaskPriority


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )

    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id"),
        nullable=False,
    )

    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    status = Column(
        String(50),
        nullable=False,
        default=TaskStatus.to_do.value,
    )

    priority = Column(
        String(50),
        nullable=False,
        default=TaskPriority.medium.value,
    )

    due_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    project = relationship("Project", back_populates="tasks")

    # Many-to-many con Users
    assignees = relationship(
        "User",
        secondary="task_assignees",
        back_populates="tasks_assigned",
    )

    comments = relationship("Comment", back_populates="task")
