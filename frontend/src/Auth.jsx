import { useState } from "react";
import "./Auth.css";

const API_URL = "http://127.0.0.1:8000";

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const switchMode = (newMode) => {
    setMode(newMode);
    setError("");
    setSuccess("");
    setName("");
    setEmail("");
    setPassword("");
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const endpoint =
        mode === "login"
          ? `${API_URL}/api/v1/auth/login`
          : `${API_URL}/api/v1/auth/signup`;

      const body =
        mode === "login"
          ? {
              email,
              password,
            }
          : {
              name,
              email,
              password,
            };

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || data.message || "Something went wrong."
        );
      }

      if (mode === "signup") {
        setSuccess("Account created successfully. You can now sign in.");

        setMode("login");
        setName("");
        setPassword("");

        return;
      }

      const user = data.user;

      localStorage.setItem("repairx_user", JSON.stringify(user));

      onLogin(user);
    } catch (err) {
      setError(err.message || "Unable to connect to RepairX.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-shell">

        {/* LEFT SIDE */}
        <section className="auth-intro">
          <div className="auth-brand">
            <div className="auth-logo">R</div>

            <div>
              <strong>RepairX</strong>
              <span>API Engineering Platform</span>
            </div>
          </div>

          <div className="intro-content">
            <span className="eyebrow">
              API OBSERVABILITY & AUTOMATED REPAIR
            </span>

            <h1>
              Find the problem.
              <br />
              Understand the cause.
              <br />
              <span>Repair it.</span>
            </h1>

            <p>
              RepairX monitors backend applications, investigates failures,
              identifies root causes and guides verified repairs.
            </p>

            <div className="intro-points">
              <div>
                <span>01</span>
                <p>Detect backend failures</p>
              </div>

              <div>
                <span>02</span>
                <p>Trace the root cause</p>
              </div>

              <div>
                <span>03</span>
                <p>Generate and verify repairs</p>
              </div>
            </div>
          </div>
        </section>

        {/* RIGHT SIDE */}
        <section className="auth-card-area">
          <div className="auth-card">

            <div className="auth-heading">
              <span className="auth-label">
                {mode === "login" ? "WELCOME BACK" : "GET STARTED"}
              </span>

              <h2>
                {mode === "login"
                  ? "Sign in to RepairX"
                  : "Create your RepairX account"}
              </h2>

              <p>
                {mode === "login"
                  ? "Access your applications, APIs and repair activity."
                  : "Start monitoring and repairing your backend applications."}
              </p>
            </div>

            {/* MODE SWITCH */}
            <div className="auth-tabs">
              <button
                type="button"
                className={mode === "login" ? "selected" : ""}
                onClick={() => switchMode("login")}
              >
                Sign In
              </button>

              <button
                type="button"
                className={mode === "signup" ? "selected" : ""}
                onClick={() => switchMode("signup")}
              >
                Sign Up
              </button>
            </div>

            <form onSubmit={handleSubmit}>

              {mode === "signup" && (
                <div className="form-group">
                  <label>Full name</label>

                  <input
                    type="text"
                    placeholder="Enter your name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                  />
                </div>
              )}

              <div className="form-group">
                <label>Email address</label>

                <input
                  type="email"
                  placeholder="you@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <div className="password-label">
                  <label>Password</label>

                  {mode === "login" && (
                    <button
                      type="button"
                      className="forgot-button"
                      onClick={() =>
                        setError(
                          "Password reset will be connected in the next authentication step."
                        )
                      }
                    >
                      Forgot password?
                    </button>
                  )}
                </div>

                <input
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>

              {mode === "signup" && (
                <div className="password-note">
                  Use a strong password for your RepairX account.
                </div>
              )}

              {error && (
                <div className="auth-message error">
                  {error}
                </div>
              )}

              {success && (
                <div className="auth-message success">
                  {success}
                </div>
              )}

              <button
                type="submit"
                className="auth-submit"
                disabled={loading}
              >
                {loading
                  ? "Please wait..."
                  : mode === "login"
                  ? "Sign In"
                  : "Create Account"}
              </button>
            </form>

            <div className="auth-footer">
              {mode === "login" ? (
                <>
                  Don't have an account?
                  <button
                    type="button"
                    onClick={() => switchMode("signup")}
                  >
                    Create one
                  </button>
                </>
              ) : (
                <>
                  Already have an account?
                  <button
                    type="button"
                    onClick={() => switchMode("login")}
                  >
                    Sign in
                  </button>
                </>
              )}
            </div>

          </div>

          <div className="auth-bottom">
            RepairX · Backend observability and automated repair
          </div>
        </section>

      </div>
    </div>
  );
}

export default Auth;