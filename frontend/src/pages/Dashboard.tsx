import { useEffect, useState } from "react";
import { listTasks, updateTaskStatus, type Task } from "../api/tasks";
import type { TaskStatus } from "../constants/enums";
import { useAuthStore } from "../store/auth";
import { Link, useNavigate } from "react-router-dom";
import { TaskCard } from "../components/TaskCard";

export function DashboardPage() {
  const nav = useNavigate();
  const logout = useAuthStore((s) => s.logout);

  const [status, setStatus] = useState<TaskStatus | "all">("all");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setErr(null);
    try {
      const data = await listTasks(status === "all" ? undefined : { status });
      setTasks(data);
    } catch (e: any) {
      setErr(e?.response?.data?.detail ?? "Error cargando tareas");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, [status]);

  async function changeStatus(id: string, s: TaskStatus) {

    setTasks((prev) => prev.map((t) => (t.id === id ? { ...t, status: s } : t)));
    try {
      await updateTaskStatus(id, s);
    } catch {
      load();
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
        <Link to="/projects">Projects</Link>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>My Tasks</h1>
        <button
          onClick={() => {
            logout();
            nav("/login");
          }}
        >
          Logout
        </button>
      </div>

      <div style={{ display: "flex", gap: 8, marginBottom: 12 }}>
        <label>Filter:</label>
        <select value={status} onChange={(e) => setStatus(e.target.value as any)}>
          <option value="all">all</option>
          <option value="to_do">to do</option>
          <option value="in_progress">in progress</option>
          <option value="done">done</option>
          <option value="blocked">blocked</option>
        </select>
        <button onClick={load}>Refresh</button>
      </div>

      {loading && <div>Loading...</div>}
      {err && <div style={{ color: "crimson" }}>{err}</div>}
      {!loading && !err && tasks.length === 0 && <div>No tasks yet.</div>}

      <div style={{ display: "grid", gap: 12 }}>
        {tasks.map((t) => (
          <TaskCard key={t.id} task={t} onChangeStatus={changeStatus} />
        ))}
      </div>
    </div>
  );
}