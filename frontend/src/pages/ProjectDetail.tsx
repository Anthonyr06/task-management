import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { createTask, listTasks, type Task} from "../api/tasks";
import { TaskPriority, TaskStatus } from "../constants/enums";
import { listUsers, type User } from "../api/users";

export function ProjectDetailPage() {
  const { id: projectId } = useParams<{ id: string }>();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<TaskStatus>("to_do" as TaskStatus);
  const [priority, setPriority] = useState<TaskPriority>("medium");
  const [dueDate, setDueDate] = useState<string>(""); 
  const [creating, setCreating] = useState(false);
  const [createErr, setCreateErr] = useState<string | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [assigneeIds, setAssigneeIds] = useState<string[]>([]);


  const safeProjectId = projectId ?? "";

  async function load() {
    if (!safeProjectId) return;
    setLoading(true);
    setErr(null);
    try {
      const [taskData, userData] = await Promise.all([
        listTasks({ project_id: safeProjectId }),
        listUsers(),
       ]);
        setTasks(taskData);
        setUsers(userData);

    } catch (e: any) {
      setErr(e?.response?.data?.detail ?? e?.response?.data?.error?.message ?? "Error cargando tareas");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [safeProjectId]);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreateErr(null);

    if (!safeProjectId) {
      setCreateErr("projectId inválido.");
      return;
    }
    if (!title.trim()) {
      setCreateErr("Title requerido.");
      return;
    }

    setCreating(true);
    try {
      const assignee_ids = assigneeIds;

      const created = await createTask({
        project_id: safeProjectId,
        title: title.trim(),
        description: description.trim() ? description.trim() : null,
        status,
        priority,
        due_date: dueDate ? dueDate : null,
        assignee_ids,
      });

      setTasks((prev) => [created, ...prev]);

      // reset form
      setTitle("");
      setDescription("");
      setStatus("to_do" as TaskStatus);
      setPriority("medium");
      setDueDate("");
      setAssigneeIds([]);
    } catch (e: any) {
      setCreateErr(e?.response?.data?.detail ?? e?.response?.data?.error?.message ?? "Error creando tarea");
    } finally {
      setCreating(false);
    }
  }

  if (!safeProjectId) {
    return (
      <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
        <p>Project id inválido.</p>
        <Link to="/projects">Back</Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <h1 style={{ marginBottom: 4 }}>Project</h1>
          <div style={{ fontSize: 12, color: "#666" }}>id: {safeProjectId}</div>
        </div>

        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={load} disabled={loading}>
            Refresh
          </button>
          <Link to="/projects">Back</Link>
        </div>
      </div>

      <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginTop: 16 }}>
        <h3 style={{ marginTop: 0 }}>Create Task</h3>

        <form onSubmit={onCreate} style={{ display: "grid", gap: 10 }}>
          <input placeholder="title" value={title} onChange={(e) => setTitle(e.target.value)} />

          <input
            placeholder="description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <div style={{ display: "flex", gap: 10 }}>
            <label style={{ display: "grid", gap: 4 }}>
              <span>Status</span>
              <select value={status} onChange={(e) => setStatus(e.target.value as TaskStatus)}>
                <option value="to_do">to_do</option>
                <option value="in_progress">in_progress</option>
                <option value="done">done</option>
                <option value="blocked">blocked</option>
              </select>
            </label>

            <label style={{ display: "grid", gap: 4 }}>
              <span>Priority</span>
              <select value={priority} onChange={(e) => setPriority(e.target.value as TaskPriority)}>
                <option value="low">low</option>
                <option value="medium">medium</option>
                <option value="high">high</option>
                <option value="critical">critical</option>
              </select>
            </label>

            <label style={{ display: "grid", gap: 4 }}>
              <span>Due date</span>
              <input type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} />
            </label>
          </div>

          <label style={{ display: "grid", gap: 6 }}>
            <span>Assignees (multi-select)</span>
            <select
                multiple
                value={assigneeIds}
                onChange={(e) => {
                const ids = Array.from(e.target.selectedOptions).map((o) => o.value);
                setAssigneeIds(ids);
                }}
                style={{ minHeight: 140 }}
            >
                {users.map((u) => (
                <option key={u.id} value={u.id}>
                    {u.email} ({u.role})
                </option>
                ))}
            </select>
            </label>


          {createErr && <div style={{ color: "crimson" }}>{createErr}</div>}

          <button disabled={creating} type="submit">
            {creating ? "Creating..." : "Create Task"}
          </button>
        </form>
      </div>

      <div style={{ marginTop: 16 }}>
        <h3>Tasks</h3>
        {loading && <div>Loading...</div>}
        {err && <div style={{ color: "crimson" }}>{err}</div>}
        {!loading && !err && tasks.length === 0 && <div>No tasks yet.</div>}

        <div style={{ display: "grid", gap: 12 }}>
          {tasks.map((t) => (
            <div key={t.id} style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
                <strong>{t.title}</strong>
                <small>
                  {t.status} · {t.priority}
                </small>
              </div>

              {t.description && <p style={{ marginBottom: 0 }}>{t.description}</p>}

              <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
                id: {t.id}
                {t.due_date ? ` · due: ${t.due_date}` : ""}
              </div>

              <div style={{ marginTop: 6, fontSize: 12, color: "#555" }}>
                Assignees: {(t.assignees ?? []).map((u) => u.email).join(", ") || "—"}
              </div>

              <div style={{ marginTop: 8 }}>
                <Link to={`/tasks/${t.id}`}>Open task</Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
