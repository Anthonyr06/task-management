import { Routes, Route, Navigate } from "react-router-dom";
import { LoginPage } from "./pages/Login";
import { RegisterPage } from "./pages/Register";
import { DashboardPage } from "./pages/Dashboard";
import { ProjectsPage } from "./pages/Projects";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { ProjectDetailPage } from "./pages/ProjectDetail";
import { TaskDetailPage } from "./pages/TaskDetail";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<DashboardPage />} />
      </Route>

      <Route path="tasks/:id" element={<TaskDetailPage />} />  

      <Route element={<ProtectedRoute />}>
        <Route path="/projects" element={<ProjectsPage />} />
      </Route>

      <Route path="/projects/:id" element={<ProjectDetailPage />} />

      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
