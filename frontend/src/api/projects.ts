import { api } from "./client";
import type { ProjectStatus } from "../constants/enums";

export type Project = { id: string; name: string; description?: string|null; status: ProjectStatus };

export async function listProjects() {
  const r = await api.get<Project[]>("/projects");
  return r.data;
}

export async function createProject(input: {name: string; description?: string|null; status: ProjectStatus}) {
  const r = await api.post<Project>("/projects", input);
  return r.data;
}
