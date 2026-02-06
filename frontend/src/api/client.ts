import axios from "axios";
import { useAuthStore } from "../store/auth";
import { refresh } from "./auth";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "/api",
});

api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

let isRefreshing = false;

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    if (err.response?.status !== 401 || original?._retry) throw err;

    const store = useAuthStore.getState();
    if (!store.refreshToken) throw err;

    if (isRefreshing) throw err;
    isRefreshing = true;

    try {
      original._retry = true;
      const data = await refresh(store.refreshToken);
      useAuthStore.getState().setTokens(data.access_token, data.refresh_token);
      original.headers.Authorization = `Bearer ${data.access_token}`;
      return api.request(original);
    } finally {
      isRefreshing = false;
    }
  }
);
