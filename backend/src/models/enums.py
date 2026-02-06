import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    manager = "manager"
    member = "member"


class ProjectStatus(str, enum.Enum):
    active = "active"
    archived = "archived"


class TaskStatus(str, enum.Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    done = "done"
    blocked = "blocked"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"