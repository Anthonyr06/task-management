from uuid import UUID
from sqlalchemy.orm import Session

from src.models.comment import Comment


def list_comments_by_task(db: Session, task_id: UUID) -> list[Comment]:
    return (
        db.query(Comment)
        .filter(Comment.task_id == task_id)
        .order_by(Comment.created_at.asc())
        .all()
    )


def create_comment(
    db: Session,
    *,
    task_id: UUID,
    author_id: UUID,
    content: str,
    mentions: list[UUID] | None,
) -> Comment:
    c = Comment(
        task_id=task_id,
        author_id=author_id,
        content=content,
        mentions=mentions,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c