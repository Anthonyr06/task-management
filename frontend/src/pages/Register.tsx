import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { register } from "../api/auth";

type Role = "admin" | "manager" | "member";

export function RegisterPage() {
  const nav = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<Role>("member");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [ok, setOk] = useState<string | null>(null);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null);
    setOk(null);

    if (!email || !password) {
      setErr("Email y password son requeridos.");
      return;
    }

    if (new TextEncoder().encode(password).length > 72) {
      setErr("Password demasiado largo (bcrypt max 72 bytes).");
      return;
    }

    setLoading(true);
    try {
      await register(email, password, role);
      setOk("Usuario creado. Ahora puedes hacer login.");
      setTimeout(() => nav("/login"), 800);
    } catch (e: any) {
      const msg =
        e?.response?.data?.detail ??
        e?.response?.data?.error?.message ??
        "Error creando usuario.";
      setErr(msg);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 420, margin: "48px auto", padding: 16 }}>
      <h1>Register</h1>

      <form onSubmit={onSubmit} style={{ display: "grid", gap: 12 }}>
        <input
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          type="email"
        />

        <input
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
        />

        <select value={role} onChange={(e) => setRole(e.target.value as Role)}>
          <option value="member">member</option>
          <option value="manager">manager</option>
          <option value="admin">admin</option>
        </select>

        {err && <div style={{ color: "crimson" }}>{err}</div>}
        {ok && <div style={{ color: "green" }}>{ok}</div>}

        <button disabled={loading} type="submit">
          {loading ? "Creando..." : "Crear usuario"}
        </button>
      </form>

      <div style={{ marginTop: 12 }}>
        <Link to="/login">Volver a Login</Link>
      </div>
    </div>
  );
}
