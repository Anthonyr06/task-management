from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.api.dependencies.auth import get_current_user
from src.schemas.webhook import WebhookCreate, WebhookUpdate, WebhookOut
from src.services.webhooks import (
    list_project_webhooks,
    create_project_webhook,
    set_webhook_active,
    remove_webhook,
)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("/projects/{project_id}", response_model=list[WebhookOut])
def list_route(project_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return list_project_webhooks(db, current_user, project_id)


@router.post("/projects/{project_id}", response_model=WebhookOut)
def create_route(project_id: UUID, payload: WebhookCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_project_webhook(
        db,
        current_user,
        project_id,
        url=str(payload.url),
        events=payload.events,
        secret=payload.secret,
        is_active=payload.is_active,
    )


@router.patch("/{webhook_id}", response_model=WebhookOut)
def patch_route(webhook_id: UUID, payload: WebhookUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return set_webhook_active(db, current_user, webhook_id, is_active=payload.is_active)


@router.delete("/{webhook_id}")
def delete_route(webhook_id: UUID, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    remove_webhook(db, current_user, webhook_id)
    return {"deleted": True}
