import { api } from "./client";

export type User = {
  id: string;
  email: string;
  role: string;
};

export async function listUsers() {
  const r = await api.get<User[]>("/users");
  return r.data;
}
