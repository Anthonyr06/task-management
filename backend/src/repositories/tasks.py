from uuid import UUID
from sqlalchemy.orm import Session

from src.models.task import Task


def get_task(db: Session, task_id: UUID) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()


def list_tasks(
    db: Session,
    *,
    project_id: UUID | None = None,
    status: str | None = None,
    assignee_id: UUID | None = None,
) -> list[Task]:
    q = db.query(Task)

    if project_id:
        q = q.filter(Task.project_id == project_id)
    if status:
        q = q.filter(Task.status == status)
    if assignee_id:
        q = q.join(Task.assignees).filter_by(id=assignee_id)

    return q.order_by(Task.created_at.desc()).all()


def create_task(
    db: Session,
    *,
    project_id: UUID,
    title: str,
    description: str | None,
    status: str,
    priority: str,
    due_date,
) -> Task:
    t = Task(
        project_id=project_id,
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=due_date,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
