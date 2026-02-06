from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.api.dependencies.auth import get_current_user
from src.schemas.task import TaskCreate, TaskUpdate, TaskOut
from src.services.tasks import (
    list_tasks,
    create_task,
    get_task_or_404,
    update_task,
    delete_task, 
    list_my_tasks
)

from src.repositories.webhooks import list_active_for_event
from src.services.webhook_dispatcher import send_webhook, build_event

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def list_route(
    project_id: UUID | None = None,
    status: str | None = None,
    assignee_id: UUID | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_tasks(db, current_user, project_id=project_id, status_=status, assignee_id=assignee_id)


@router.post("", response_model=TaskOut)
def create_route(
    payload: TaskCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = create_task(
        db,
        current_user,
        project_id=payload.project_id,
        title=payload.title,
        description=payload.description,
        status_=payload.status.value,
        priority=payload.priority.value,
        due_date=payload.due_date,
        assignee_ids=payload.assignee_ids,
    )

    #disparar webhooks en background
    hooks = list_active_for_event(db, task.project_id, "task.created")
    event_payload = build_event(
        "task.created",
        {"task_id": str(task.id), "project_id": str(task.project_id)},
    )

    for h in hooks:
        background_tasks.add_task(send_webhook, h.url, h.secret, event_payload)

    return task


@router.get("/me", response_model=list[TaskOut])
def my_tasks_route(
    status: str | None = None,
    project_id: UUID | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_my_tasks(db, current_user, status_=status, project_id=project_id)


@router.get("/{task_id}", response_model=TaskOut)
def get_route(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_task_or_404(db, current_user, task_id)


@router.patch("/{task_id}", response_model=TaskOut)
def update_route(
    task_id: UUID,
    payload: TaskUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    task = update_task(
        db,
        current_user,
        task_id,
        title=payload.title,
        description=payload.description,
        status_=payload.status.value if payload.status else None,
        priority=payload.priority.value if payload.priority else None,
        due_date=payload.due_date,
        assignee_ids=payload.assignee_ids,
    )

    hooks = list_active_for_event(db, task.project_id, "task.updated")
    event_payload = build_event(
        "task.updated",
        {"task_id": str(task.id), "project_id": str(task.project_id)},
    )

    for h in hooks:
        background_tasks.add_task(send_webhook, h.url, h.secret, event_payload)

    return task



@router.delete("/{task_id}")
def delete_route(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    delete_task(db, current_user, task_id)
    return {"deleted": True}