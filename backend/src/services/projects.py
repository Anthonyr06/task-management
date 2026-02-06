from fastapi import HTTPException, status as http_status
from sqlalchemy.orm import Session

from src.models.enums import UserRole
from src.repositories.projects import (
    get_project as repo_get_project,
    list_projects as repo_list_projects,
    list_projects_by_owner as repo_list_by_owner,
    create_project as repo_create_project,
    update_project as repo_update_project,
    delete_project as repo_delete_project,
)


def list_projects(db: Session, current_user):
    # admin ve todo
    if current_user.role == UserRole.admin.value:
        return repo_list_projects(db)
    return repo_list_by_owner(db, current_user.id)



def create_project(db, current_user, *, name: str, description: str | None, project_status: str):
    if current_user.role not in ("admin", "manager"):
        raise HTTPException(status_code=http_status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return repo_create_project(
        db, name=name, description=description, status=project_status, owner_id=current_user.id
    )


def get_project_or_404(db: Session, project_id, current_user):
    project = repo_get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != UserRole.admin.value and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return project


def update_project(db: Session, current_user, project_id, *, name=None, description=None, status_=None):
    project = repo_get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != UserRole.admin.value and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return repo_update_project(db, project, name=name, description=description, status=status_)


def delete_project(db: Session, current_user, project_id):
    project = repo_get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if current_user.role != UserRole.admin.value and project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    repo_delete_project(db, project)
