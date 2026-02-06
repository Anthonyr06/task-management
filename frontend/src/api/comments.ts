import { api } from "./client";

export type Comment = {
  id: string;
  task_id: string;
  author_id: string;
  content: string;
  mentions?: string[] | null;
  created_at?: string;
};

export async function listComments(taskId: string) {
  const r = await api.get<Comment[]>(`/tasks/${taskId}/comments`);
  return r.data;
}

export async function addComment(
  taskId: string,
  input: { content: string; mentions?: string[] | null }
) {
  const r = await api.post<Comment>(`/tasks/${taskId}/comments`, input);
  return r.data;
}
