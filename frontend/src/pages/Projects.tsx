import { useEffect, useState } from "react";
import { createProject, listProjects, type Project } from "../api/projects";
import type { ProjectStatus } from "../constants/enums";
import { Link } from "react-router-dom";

export function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<string | null>(null);

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState<ProjectStatus>("active");
  const [creating, setCreating] = useState(false);
  const [createErr, setCreateErr] = useState<string | null>(null);

  async function load() {
    setLoading(true);
    setErr(null);
    try {
      const data = await listProjects();
      setProjects(data);
    } catch (e: any) {
      setErr(e?.response?.data?.detail ?? e?.response?.data?.error?.message ?? "Error cargando proyectos");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function onCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreateErr(null);

    if (!name.trim()) {
      setCreateErr("Name es requerido.");
      return;
    }

    setCreating(true);
    try {
      const p = await createProject({
        name: name.trim(),
        description: description.trim() ? description.trim() : null,
        status,
      });
      setProjects((prev) => [p, ...prev]);
      setName("");
      setDescription("");
      setStatus("active");
    } catch (e: any) {
      const msg =
        e?.response?.data?.detail ??
        e?.response?.data?.error?.message ??
        "Error creando proyecto";
      setCreateErr(msg);
    } finally {
      setCreating(false);
    }
  }

  return (
    <div style={{ maxWidth: 900, margin: "24px auto", padding: 16 }}>
        <Link to="/dashboard">DashBoard</Link>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Projects</h1>
        <button onClick={load} disabled={loading}>
          Refresh
        </button>
      </div>

      <div style={{ border: "1px solid #ddd", borderRadius: 8, padding: 12, marginBottom: 16 }}>
        <h3 style={{ marginTop: 0 }}>Create Project</h3>

        <form onSubmit={onCreate} style={{ display: "grid", gap: 10 }}>
          <input placeholder="name" value={name} onChange={(e) => setName(e.target.value)} />

          <input
            placeholder="description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          <select value={status} onChange={(e) => setStatus(e.target.value as ProjectStatus)}>
            <option value="active">active</option>
            <option value="archived">archived</option>
          </select>

          {createErr && <div style={{ color: "crimson" }}>{createErr}</div>}

          <button disabled={creating} type="submit">
            {creating ? "Creating..." : "Create"}
          </button>

          <small style={{ color: "#555" }}>
            * Solo admin/manager pueden crear. Si eres member verás 403 (correcto).
          </small>
        </form>
      </div>

      {loading && <div>Loading...</div>}
      {err && <div style={{ color: "crimson" }}>{err}</div>}
      {!loading && !err && projects.length === 0 && <div>No projects yet.</div>}

      <div style={{ display: "grid", gap: 12 }}>
        {projects.map((p) => (
          <div key={p.id} style={{ border: "1px solid #eee", borderRadius: 8, padding: 12 }}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 8 }}>
              <Link to={`/projects/${p.id}`}><strong>{p.name}</strong></Link>
              <small>{p.status}</small>
            </div>
            {p.description && <p style={{ marginBottom: 0 }}>{p.description}</p>}
            <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>id: {p.id}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
