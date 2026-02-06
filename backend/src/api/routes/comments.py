from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.api.dependencies.auth import get_current_user
from src.schemas.comment import CommentCreate, CommentOut
from src.services.comments import add_comment, get_comments

router = APIRouter(tags=["comments"])


@router.get("/tasks/{task_id}/comments", response_model=list[CommentOut])
def list_comments_route(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_comments(db, current_user, task_id)


@router.post("/tasks/{task_id}/comments", response_model=CommentOut)
def create_comment_route(
    task_id: UUID,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # ignoramos payload.task_id si viene; usamos el path param
    return add_comment(db, current_user, task_id, content=payload.content, mentions=payload.mentions)