// src/pages/Register.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { authService } from "../services/authService"; // ✅ Correct path (if both folders are in /src)

export default function Register() {
  const [formData, setFormData] = useState({
    full_name: "John Doe",
    email: "john@example.com",
    password: "password123",
    phone: "+1234567890"
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const data = await authService.register(formData);
      login(data.user, data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "linear-gradient(135deg, #f0fdfa, #ffffff, #f8fafc)",
        padding: "20px"
      }}
    >
      <div
        style={{
          background: "white",
          padding: "48px",
          borderRadius: "20px",
          boxShadow: "0 20px 60px rgba(0,0,0,0.1)",
          maxWidth: "450px",
          width: "100%"
        }}
      >
        <h1
          style={{
            fontSize: "32px",
            fontWeight: "bold",
            marginBottom: "8px",
            background: "linear-gradient(135deg, #14b8a6, #0d9488)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent"
          }}
        >
          🏥 HealthRecord
        </h1>
        <p style={{ marginBottom: "32px", color: "#64748b" }}>
          Create your account
        </p>

        {error && (
          <div
            style={{
              padding: "12px",
              background: "#fee2e2",
              color: "#dc2626",
              borderRadius: "8px",
              marginBottom: "16px",
              fontSize: "14px"
            }}
          >
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Full Name"
            value={formData.full_name}
            onChange={(e) =>
              setFormData({ ...formData, full_name: e.target.value })
            }
            required
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "12px",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
              fontSize: "14px"
            }}
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) =>
              setFormData({ ...formData, email: e.target.value })
            }
            required
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "12px",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
              fontSize: "14px"
            }}
          />
          <input
            type="password"
            placeholder="Password (min 6 chars)"
            value={formData.password}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
            minLength={6}
            required
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "12px",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
              fontSize: "14px"
            }}
          />
          <input
            type="tel"
            placeholder="Phone (optional)"
            value={formData.phone}
            onChange={(e) =>
              setFormData({ ...formData, phone: e.target.value })
            }
            style={{
              width: "100%",
              padding: "12px",
              marginBottom: "24px",
              border: "1px solid #e2e8f0",
              borderRadius: "8px",
              fontSize: "14px"
            }}
          />
          <button
            type="submit"
            disabled={loading}
            style={{
              width: "100%",
              padding: "12px",
              background: "linear-gradient(135deg, #14b8a6, #0d9488)",
              color: "white",
              border: "none",
              borderRadius: "8px",
              fontWeight: "bold",
              cursor: loading ? "not-allowed" : "pointer",
              opacity: loading ? 0.7 : 1
            }}
          >
            {loading ? "⏳ Creating account..." : "🚀 Create Account"}
          </button>
        </form>

        <p
          style={{
            marginTop: "16px",
            textAlign: "center",
            color: "#64748b",
            fontSize: "14px"
          }}
        >
          Already have an account?{" "}
          <Link
            to="/login"
            style={{
              color: "#14b8a6",
              fontWeight: "bold",
              textDecoration: "none"
            }}
          >
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
}
