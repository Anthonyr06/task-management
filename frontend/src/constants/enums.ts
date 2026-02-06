export const TaskStatus = {
  TO_DO: "to_do",
  IN_PROGRESS: "in_progress",
  DONE: "done",
  BLOCKED: "blocked",
} as const;

export type TaskStatus = (typeof TaskStatus)[keyof typeof TaskStatus];

export const TaskPriority = {
  LOW: "low",
  MEDIUM: "medium",
  HIGH: "high",
  CRITICAL: "critical",
} as const;

export type TaskPriority = (typeof TaskPriority)[keyof typeof TaskPriority];

export const ProjectStatus = {
  ACTIVE: "active",
  ARCHIVED: "archived"
} as const;

export type ProjectStatus = (typeof ProjectStatus)[keyof typeof ProjectStatus];