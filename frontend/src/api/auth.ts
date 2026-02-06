import { api } from "./client";

export async function login(email: string, password: string) {
  const r = await api.post("/auth/login", { email, password });
  return r.data as { access_token: string; refresh_token: string; token_type: string };
}

export async function refresh(refreshToken: string) {
  const r = await api.post("/auth/refresh", { refresh_token: refreshToken });
  return r.data as { access_token: string; refresh_token: string; token_type: string };
}

export async function register(email: string, password: string, role: "admin"|"manager"|"member") {
  const r = await api.post("/auth/register", { email, password, role });
  return r.data;
}
