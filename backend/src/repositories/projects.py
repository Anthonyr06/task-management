from uuid import UUID
from sqlalchemy.orm import Session

from src.models.project import Project


def get_project(db: Session, project_id: UUID) -> Project | None:
    return db.query(Project).filter(Project.id == project_id).first()


def list_projects(db: Session) -> list[Project]:
    return db.query(Project).order_by(Project.created_at.desc()).all()


def list_projects_by_owner(db: Session, owner_id: UUID) -> list[Project]:
    return (
        db.query(Project)
        .filter(Project.owner_id == owner_id)
        .order_by(Project.created_at.desc())
        .all()
    )


def create_project(
    db: Session, *, name: str, description: str | None, status: str, owner_id: UUID
) -> Project:
    p = Project(name=name, description=description, status=status, owner_id=owner_id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


def update_project(db: Session, project: Project, *, name=None, description=None, status=None) -> Project:
    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if status is not None:
        project.status = status

    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
