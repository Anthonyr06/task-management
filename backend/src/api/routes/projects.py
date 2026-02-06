from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.api.dependencies.auth import get_current_user
from src.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from src.services.projects import (
    list_projects,
    create_project,
    get_project_or_404,
    update_project,
    delete_project,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_projects(db, current_user)


@router.post("", response_model=ProjectOut)
def create_route(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return create_project(
        db,
        current_user,
        name=payload.name,
        description=payload.description,
        project_status=payload.status.value,
    )



@router.get("/{project_id}", response_model=ProjectOut)
def get_route(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return get_project_or_404(db, project_id, current_user)


@router.patch("/{project_id}", response_model=ProjectOut)
def update_route(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_project(
        db,
        current_user,
        project_id,
        name=payload.name,
        description=payload.description,
        status_=payload.status.value if payload.status else None,
    )


@router.delete("/{project_id}")
def delete_route(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    delete_project(db, current_user, project_id)
    return {"deleted": True}
