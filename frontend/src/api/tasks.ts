import { api } from "./client";
import type { TaskStatus, TaskPriority } from "../constants/enums";
import type { User } from "./users";

export type Task = {
  id: string;
  project_id: string;
  title: string;
  description?: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  due_date?: string | null;
  assignees?: User[];
};

export type ListTasksParams = {
  status?: TaskStatus;
  assignee_id?: string;
  project_id?: string;
};

export async function getTask(taskId: string) {
  const r = await api.get<Task>(`/tasks/${taskId}`);
  return r.data;
}

export async function createTask(input: {
  project_id: string;
  title: string;
  description?: string|null;
  status: TaskStatus;
  priority: TaskPriority;
  due_date?: string|null;
  assignee_ids: string[];
}) {
  const r = await api.post<Task>("/tasks", input);
  return r.data;
}

export async function updateTask(
  taskId: string,
  input: Partial<{
    title: string;
    description: string | null;
    status: TaskStatus;
    priority: TaskPriority;
    due_date: string | null;
    assignee_ids: string[];
  }>
) {
  const r = await api.patch<Task>(`/tasks/${taskId}`, input);
  return r.data;
}


export async function listTasks(params?: ListTasksParams) {
  const r = await api.get<Task[]>("/tasks", { params });
  return r.data;
}
export async function updateTaskStatus(taskId: string, status: TaskStatus) {
  const r = await api.patch(`/tasks/${taskId}`, { status });
  return r.data as Task;
}
