from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.repositories.projects import get_project
from src.repositories.webhooks import (
    list_webhooks_by_project,
    create_webhook,
    get_webhook,
    update_webhook_active,
    delete_webhook,
)


def _can_manage_project(current_user, project) -> bool:
    return current_user.role == "admin" or project.owner_id == current_user.id


def list_project_webhooks(db: Session, current_user, project_id: UUID):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    if not _can_manage_project(current_user, project):
        raise HTTPException(403, "Forbidden")
    return list_webhooks_by_project(db, project_id)


def create_project_webhook(db: Session, current_user, project_id: UUID, *, url: str, events: list[str], secret: str, is_active: bool):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    if not _can_manage_project(current_user, project):
        raise HTTPException(403, "Forbidden")
    return create_webhook(db, project_id=project_id, url=url, events=events, secret=secret, is_active=is_active)


def set_webhook_active(db: Session, current_user, webhook_id: UUID, *, is_active: bool):
    w = get_webhook(db, webhook_id)
    if not w:
        raise HTTPException(404, "Webhook not found")
    project = get_project(db, w.project_id)
    if not project or not _can_manage_project(current_user, project):
        raise HTTPException(403, "Forbidden")
    return update_webhook_active(db, w, is_active=is_active)


def remove_webhook(db: Session, current_user, webhook_id: UUID):
    w = get_webhook(db, webhook_id)
    if not w:
        raise HTTPException(404, "Webhook not found")
    project = get_project(db, w.project_id)
    if not project or not _can_manage_project(current_user, project):
        raise HTTPException(403, "Forbidden")
    delete_webhook(db, w)
