from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models.enums import UserRole
from src.repositories.tasks import get_task as repo_get_task, list_tasks as repo_list_tasks, create_task as repo_create_task, delete_task as repo_delete_task
from src.repositories.users import get_users_by_ids
from src.repositories.projects import get_project
from src.repositories.tasks import list_tasks as repo_list_tasks

def _can_access_project(current_user, project) -> bool:
    if current_user.role == UserRole.admin.value:
        return True
    return project.owner_id == current_user.id


def list_tasks(db: Session, current_user, *, project_id=None, status_=None, assignee_id=None):
    if current_user.role == UserRole.member.value:
        return repo_list_tasks(db, project_id=project_id, status=status_, assignee_id=current_user.id)

    if project_id and current_user.role != UserRole.admin.value:
        project = get_project(db, project_id)
        if not project or project.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    return repo_list_tasks(db, project_id=project_id, status=status_, assignee_id=assignee_id)


def create_task(
    db: Session,
    current_user,
    *,
    project_id: UUID,
    title: str,
    description: str | None,
    status_: str,
    priority: str,
    due_date,
    assignee_ids: list[UUID],
):
    project = get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if not _can_access_project(current_user, project):
        raise HTTPException(status_code=403, detail="Forbidden")

    task = repo_create_task(
        db,
        project_id=project_id,
        title=title,
        description=description,
        status=status_,
        priority=priority,
        due_date=due_date,
    )

    users = get_users_by_ids(db, assignee_ids)
    task.assignees = users
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_my_tasks(db, current_user, *, status_=None, project_id=None):
    return repo_list_tasks(
        db,
        project_id=project_id,
        status=status_,
        assignee_id=current_user.id,
    )

def get_task_or_404(db: Session, current_user, task_id: UUID):
    task = repo_get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role == UserRole.admin.value:
        return task

    if current_user.role == UserRole.member.value:
        if not any(u.id == current_user.id for u in task.assignees):
            raise HTTPException(status_code=403, detail="Forbidden")
        return task

    project = get_project(db, task.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return task


def update_task(
    db: Session,
    current_user,
    task_id: UUID,
    *,
    title=None,
    description=None,
    status_=None,
    priority=None,
    due_date=None,
    assignee_ids=None,  
):
    task = get_task_or_404(db, current_user, task_id)

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if status_ is not None:
        task.status = status_
    if priority is not None:
        task.priority = priority
    if due_date is not None:
        task.due_date = due_date

    if assignee_ids is not None:
        users = get_users_by_ids(db, assignee_ids)
        task.assignees = users

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, current_user, task_id: UUID):
    task = get_task_or_404(db, current_user, task_id)
    repo_delete_task(db, task)
