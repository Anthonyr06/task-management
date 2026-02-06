from datetime import datetime, timezone
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.core.db import Base
from src.models.enums import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    email = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False)
    
    password_hash = Column(String(255), nullable=False)

    role = Column(
        String(50), nullable=False, default=UserRole.member.value
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

    projects = relationship("Project", back_populates="owner")
    comments = relationship("Comment", back_populates="author")

    tasks_assigned = relationship(
        "Task",
        secondary="task_assignees",
        back_populates="assignees",
    )
