import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getTask, updateTask, type Task } from "../api/tasks";
import { addComment, listComments, type Comment } from "../api/comments";
import { TaskPriority, TaskStatus } from "../constants/enums";
import { listUsers, type User } from "../api/users";

function getErr(e: any, fallback: string) {
  return e?.response?.data?.detail ?? e?.response?.data?.error?.message ?? fallback;
}

export function TaskDetailPage() {
  const { id: taskId } = useParams<{ id: string }>();
  const safeTaskId = taskId ?? "";

  const [task, setTask] = useState<Task | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [users, setUsers] = useState<User[]>([]);

  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  // comment form
  const [content, setContent] = useState("");
  const [mentionIds, setMentionIds] = useState<string[]>([]);
  const [posting, setPosting] = useState(false);
  const [postErr, setPostErr] = useState<string | null>(null);

  // edit form (un solo objeto)
  const [edit, setEdit] = useState<{
    title: string;
    description: string;
    priority: TaskPriority;
    dueDate: string; // YYYY-MM-DD
  }>({
    title: "",
    description: "",
    priority: "medium",
    dueDate: "",
  });

  const [saving, setSaving] = useState(false);
  const [saveErr, setSaveErr] = useState<string | null>(null);
  const [saveOk, setSaveOk] = useState<string | null>(null);

  // evita race conditions si haces refresh rápido
  const loadSeq = useRef(0);

  // 1) carga users UNA sola vez al montar
  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const u = await listUsers();
        if (!cancelled) setUsers(u);
      } catch {
        // si falla users, no tumba toda la página
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  // 2) load task + comments (depende de taskId)
  const load = useCallback(async () => {
    if (!safeTaskId) return;

    const seq = ++loadSeq.current;
    setLoading(true);
    setErr(null);

    try {
      const [t, c] = await Promise.all([getTask(safeTaskId), listComments(safeTaskId)]);
      if (seq !== loadSeq.current) return; // respuesta vieja, ignórala

      setTask(t);
      setComments(c);

      setEdit({
        title: t.title,
        description: t.description ?? "",
        priority: t.priority,
        dueDate: t.due_date ? t.due_date.slice(0, 10) : "",
      });

      setSaveOk(null);
      setSaveErr(null);
    } catch (e: any) {
      if (seq !== loadSeq.current) return;
      setErr(getErr(e, "Error cargando task"));
    } finally {
      if (seq === loadSeq.current) setLoading(false);
    }
  }, [safeTaskId]);

  useEffect(() => {
    load();
  }, [load]);

  // dirty check para evitar saves inútiles
  const isDirty = useMemo(() => {
    if (!task) return false;
    const origTitle = task.title ?? "";
    const origDesc = task.description ?? "";
    const origPriority = task.priority;
    const origDue = task.due_date ? task.due_date.slice(0, 10) : "";
    return (
      edit.title.trim() !== origTitle ||
      edit.description.trim() !== origDesc ||
      edit.priority !== origPriority ||
      edit.dueDate !== origDue
    );
  }, [task, edit]);

  const changeStatus = useCallback(
    async (s: TaskStatus) => {
      if (!task) return;

      const prev = task.status;
      setTask({ ...task, status: s });

      try {
        const updated = await updateTask(task.id, { status: s });
        setTask(updated);
      } catch {
        setTask({ ...task, status: prev });
      }
    },
    [task]
  );

  const onAddComment = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      setPostErr(null);

      if (!safeTaskId) return;
      if (!content.trim()) {
        setPostErr("El comentario no puede estar vacío.");
        return;
      }

      setPosting(true);
      try {
        const mentions = mentionIds.length ? mentionIds : null;
        const created = await addComment(safeTaskId, { content: content.trim(), mentions });

        setComments((prev) => [...prev, created]);
        setContent("");
        setMentionIds([]);
      } catch (e: any) {
        setPostErr(getErr(e, "Error agregando comentario"));
      } finally {
        setPosting(false);
      }
    },
    [safeTaskId, content, mentionIds]
  );

  const onSaveTask = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!task) return;

      setSaveErr(null);
      setSaveOk(null);

      if (!edit.title.trim()) {
        setSaveErr("Title requerido.");
        return;
      }

      setSaving(true);
      try {
        const updated = await updateTask(task.id, {
          title: edit.title.trim(),
          description: edit.description.trim() ? edit.description.trim() : null,
          priority: edit.priority,
          due_date: edit.dueDate ? edit.dueDate : null,
        });

        setTask(updated);
        setSaveOk("Saved.");
        // opcional: limpia el ok luego
        setTimeout(() => setSaveOk(null), 1200);
      } catch (e: any) {
        setSaveErr(getErr(e, "Error saving"));
      } finally {
        setSaving(false);
      }
    },
    [task, edit]
  );

  if (!safeTaskId) {
    return (
      <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
        <p>Task id inválido.</p>
        <Link to="/projects">Back</Link>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Task</h1>
        <div style={{ display: "flex", gap: 8 }}>
          <button onClick={load} disabled={loading}>
            Refresh
          </button>
          <Link to="/projects">Projects</Link>
        </div>
      </div>

      {loading && <div>Loading...</div>}
      {err && <div style={{ color: "crimson" }}>{err}</div>}

      {!loading && !err && task && (
        <>
          {/* Info */}
          <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
              <strong>{task.title}</strong>
              <small>
                {task.priority}
                {task.due_date ? ` · due: ${task.due_date}` : ""}
              </small>
            </div>

            {task.description && <p>{task.description}</p>}

            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <span>Status:</span>
              <select value={task.status} onChange={(e) => changeStatus(e.target.value as TaskStatus)}>
                <option value="to_do">to_do</option>
                <option value="in_progress">in_progress</option>
                <option value="done">done</option>
                <option value="blocked">blocked</option>
              </select>
            </div>

            <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
              id: {task.id} · project: {task.project_id}
            </div>

            <div style={{ marginTop: 6, fontSize: 12, color: "#555" }}>
              Assignees: {(task.assignees ?? []).map((u) => u.email).join(", ") || "—"}
            </div>
          </div>

          {/* Edit */}
          <div style={{ marginTop: 12, border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
            <h3 style={{ marginTop: 0 }}>Edit Task</h3>

            <form onSubmit={onSaveTask} style={{ display: "grid", gap: 10 }}>
              <input
                value={edit.title}
                onChange={(e) => setEdit((s) => ({ ...s, title: e.target.value }))}
                placeholder="title"
              />

              <textarea
                rows={3}
                value={edit.description}
                onChange={(e) => setEdit((s) => ({ ...s, description: e.target.value }))}
                placeholder="description"
              />

              <label style={{ display: "grid", gap: 6 }}>
                <span>Priority</span>
                <select
                  value={edit.priority}
                  onChange={(e) => setEdit((s) => ({ ...s, priority: e.target.value as TaskPriority }))}
                >
                  <option value="low">low</option>
                  <option value="medium">medium</option>
                  <option value="high">high</option>
                  <option value="critical">critical</option>
                </select>
              </label>

              <label style={{ display: "grid", gap: 6 }}>
                <span>Due date</span>
                <input
                  type="date"
                  value={edit.dueDate}
                  onChange={(e) => setEdit((s) => ({ ...s, dueDate: e.target.value }))}
                />
              </label>

              {saveErr && <div style={{ color: "crimson" }}>{saveErr}</div>}
              {saveOk && <div style={{ color: "green" }}>{saveOk}</div>}

              <button disabled={saving || !isDirty} type="submit">
                {saving ? "Saving..." : !isDirty ? "No changes" : "Save"}
              </button>
            </form>
          </div>

          {/* Comments */}
          <div style={{ marginTop: 16 }}>
            <h3>Comments</h3>

            {comments.length === 0 ? (
              <div>No comments yet.</div>
            ) : (
              <div style={{ display: "grid", gap: 10 }}>
                {comments.map((c) => (
                  <div key={c.id} style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
                    <div style={{ fontSize: 12, color: "#666" }}>
                      author: {c.author_id} {c.created_at ? `· ${c.created_at}` : ""}
                    </div>
                    <div style={{ marginTop: 6 }}>{c.content}</div>
                    <div style={{ marginTop: 6, fontSize: 12, color: "#555" }}>
                      mentions: {(c.mentions ?? []).join(", ") || "—"}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Add comment */}
          <div style={{ marginTop: 16, border: "1px solid #ddd", borderRadius: 8, padding: 12 }}>
            <h3 style={{ marginTop: 0 }}>Add comment</h3>

            <form onSubmit={onAddComment} style={{ display: "grid", gap: 10 }}>
              <textarea
                placeholder="content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                rows={3}
              />

              <label style={{ display: "grid", gap: 6 }}>
                <span>Mentions</span>
                <select
                  multiple
                  value={mentionIds}
                  onChange={(e) => {
                    const ids = Array.from(e.target.selectedOptions).map((o) => o.value);
                    setMentionIds(ids);
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

              {postErr && <div style={{ color: "crimson" }}>{postErr}</div>}

              <button disabled={posting} type="submit">
                {posting ? "Posting..." : "Add Comment"}
              </button>
            </form>
          </div>
        </>
      )}
    </div>
  );
}