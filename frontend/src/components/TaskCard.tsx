import { Link } from "react-router-dom";
import type { Task } from "../api/tasks";
import type { TaskStatus } from "../constants/enums";

export function TaskCard({
  task,
  onChangeStatus,
}: {
  task: Task;
  onChangeStatus: (id: string, s: TaskStatus) => void;
}) {
  return (
    <div style={{ border: "1px solid #ddd", padding: 12, borderRadius: 8 }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
        <Link to={`/tasks/${task.id}`}><strong>{task.title}</strong></Link>
        <small>{task.priority}</small>
      </div>

      {task.description && <p>{task.description}</p>}

      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <span>Status:</span>
        <select
          value={task.status}
          onChange={(e) => onChangeStatus(task.id, e.target.value as TaskStatus)}
        >
          <option value="to_do">to do</option>
          <option value="in_progress">in progress</option>
          <option value="done">done</option>
          <option value="blocked">blocked</option>
        </select>
      </div>

      <div style={{ marginTop: 8, fontSize: 12, color: "#555" }}>
        Assignees: {(task.assignees ?? []).map((u) => u.email).join(", ") || "—"}
      </div>
    </div>
  );
}