import { NavLink } from "react-router-dom";
import { authService } from "../services/authService";
import { useAuthStore } from "../store/authStore";

const Sidebar = () => {
  const { user } = useAuthStore();

  const navItems = [
    { path: "/dashboard", label: "Dashboard", icon: "⊞" },
    { path: "/upload", label: "Upload", icon: "↑" },
    { path: "/search", label: "Search", icon: "⌕" },
  ];

  return (
    <aside
      style={{
        width: "220px",
        height: "100vh",
        background: "#0f0f0f",
        borderRight: "1px solid #1e1e1e",
        display: "flex",
        flexDirection: "column",
        padding: "24px 0",
        position: "fixed",
        left: 0,
        top: 0,
      }}
    >
      {/* Logo */}
      <div style={{ padding: "0 24px 32px" }}>
        <span
          style={{
            fontSize: "18px",
            fontWeight: 700,
            color: "#ffffff",
            letterSpacing: "-0.5px",
          }}
        >
          SmartDocs
        </span>
      </div>

      {/* Nav Items */}
      <nav style={{ flex: 1, padding: "0 12px" }}>
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            style={({ isActive }) => ({
              display: "flex",
              alignItems: "center",
              gap: "10px",
              padding: "10px 12px",
              borderRadius: "6px",
              marginBottom: "4px",
              textDecoration: "none",
              fontSize: "14px",
              color: isActive ? "#ffffff" : "#666666",
              background: isActive ? "#1e1e1e" : "transparent",
              transition: "all 0.15s ease",
            })}
          >
            <span style={{ fontSize: "16px" }}>{item.icon}</span>
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* User + Logout */}
      <div
        style={{
          padding: "16px 24px",
          borderTop: "1px solid #1e1e1e",
        }}
      >
        <div
          style={{
            fontSize: "12px",
            color: "#444444",
            marginBottom: "12px",
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {user?.email}
        </div>
        <button
          onClick={() => authService.logout()}
          style={{
            width: "100%",
            padding: "8px",
            background: "transparent",
            border: "1px solid #1e1e1e",
            borderRadius: "6px",
            color: "#666666",
            fontSize: "13px",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
