from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.db import Base
from src.models.enums import ProjectStatus


class Project(Base):
    __tablename__ = "projects"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)

    status = Column(
        String(50),
        nullable=False,
        default=ProjectStatus.active.value,
    )

    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.now(timezone.utc), 
        nullable=False)
    
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
    webhooks = relationship("Webhook", back_populates="project")
