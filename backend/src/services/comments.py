from uuid import UUID
from sqlalchemy.orm import Session

from src.repositories.comments import create_comment as repo_create_comment, list_comments_by_task
from src.services.tasks import get_task_or_404


def add_comment(db: Session, current_user, task_id: UUID, *, content: str, mentions):
    
    get_task_or_404(db, current_user, task_id)

    return repo_create_comment(
        db,
        task_id=task_id,
        author_id=current_user.id,
        content=content,
        mentions=mentions,
    )


def get_comments(db: Session, current_user, task_id: UUID):
    get_task_or_404(db, current_user, task_id)
    return list_comments_by_task(db, task_id)