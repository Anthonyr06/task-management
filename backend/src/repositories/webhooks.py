from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.models.webhook import Webhook


def list_webhooks_by_project(db: Session, project_id: UUID) -> list[Webhook]:
    return db.query(Webhook).filter(Webhook.project_id == project_id).all()


def create_webhook(
    db: Session,
    *,
    project_id: UUID,
    url: str,
    events: list[str],
    secret: str,
    is_active: bool,
) -> Webhook:
    w = Webhook(
        project_id=project_id,
        url=url,
        events=events,
        secret=secret,
        is_active=is_active,
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


def get_webhook(db: Session, webhook_id: UUID) -> Webhook | None:
    return db.query(Webhook).filter(Webhook.id == webhook_id).first()


def update_webhook_active(db: Session, webhook: Webhook, *, is_active: bool) -> Webhook:
    webhook.is_active = is_active
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


def delete_webhook(db: Session, webhook: Webhook) -> None:
    db.delete(webhook)
    db.commit()


def list_active_for_event(db: Session, project_id: UUID, event: str) -> list[Webhook]:
# Filtra webhooks que tengan el evento en su lista de suscripción
    return (
        db.query(Webhook)
        .filter(
            Webhook.project_id == project_id,
            Webhook.is_active.is_(True),
            Webhook.events.any(event),
        )
        .all()
    )
