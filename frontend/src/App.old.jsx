import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("repairx_user");
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [form, setForm] = useState({
    repository: "",
    file_path: "",
    error_message: "",
    endpoint: "",
    error_type: "KeyError",
    traceback: "",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogout = () => {
    localStorage.removeItem("repairx_user");
    setUser(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);
    setResult(null);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/api/v1/repairs`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Repair request failed."
        );
      }

      setResult(data);
      setMessage("Repair analysis completed successfully.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="app">
        <div className="login-card">
          <div className="logo">R</div>

          <h1>RepairX</h1>
          <p className="subtitle">
            Intelligent Backend Error Repair
          </p>

          <p className="login-text">
            Please sign in to continue.
          </p>

          <button
            className="primary-btn"
            onClick={() => {
              const demoUser = {
                username: "admin",
                role: "Administrator",
              };

              localStorage.setItem(
                "repairx_user",
                JSON.stringify(demoUser)
              );

              setUser(demoUser);
            }}
          >
            Sign in to RepairX
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="topbar">
        <div className="brand">
          <div className="brand-logo">R</div>

          <div>
            <h2>RepairX</h2>
            <span>Backend Reliability Platform</span>
          </div>
        </div>

        <div className="user-section">
          <div className="user-info">
            <strong>{user.username}</strong>
            <span>{user.role}</span>
          </div>

          <button
            className="logout-btn"
            onClick={handleLogout}
          >
            Sign out
          </button>
        </div>
      </header>

      <main className="dashboard">
        <section className="welcome-section">
          <div>
            <p className="eyebrow">REPAIR CENTER</p>

            <h1>Investigate a backend error</h1>

            <p>
              Submit an error from your application and RepairX
              will analyze the failure, identify the likely root
              cause, and generate a repair.
            </p>
          </div>
        </section>

        <section className="repair-layout">
          <div className="card form-card">
            <div className="card-header">
              <div>
                <h2>New Repair Request</h2>
                <p>
                  Provide the details of the failed request.
                </p>
              </div>

              <span className="status-badge">
                Ready
              </span>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Repository</label>

                  <input
                    type="text"
                    name="repository"
                    value={form.repository}
                    onChange={handleChange}
                    placeholder="e.g. my-backend"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>File Path</label>

                  <input
                    type="text"
                    name="file_path"
                    value={form.file_path}
                    onChange={handleChange}
                    placeholder="e.g. backend/app.py"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Endpoint</label>

                  <input
                    type="text"
                    name="endpoint"
                    value={form.endpoint}
                    onChange={handleChange}
                    placeholder="e.g. POST /api/users"
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Error Type</label>

                  <select
                    name="error_type"
                    value={form.error_type}
                    onChange={handleChange}
                  >
                    <option value="KeyError">
                      KeyError
                    </option>

                    <option value="TypeError">
                      TypeError
                    </option>

                    <option value="ValueError">
                      ValueError
                    </option>

                    <option value="AttributeError">
                      AttributeError
                    </option>

                    <option value="IndexError">
                      IndexError
                    </option>

                    <option value="NameError">
                      NameError
                    </option>

                    <option value="ImportError">
                      ImportError
                    </option>

                    <option value="Exception">
                      Exception
                    </option>
                  </select>
                </div>
              </div>

              <div className="form-group">
                <label>Error Message</label>

                <input
                  type="text"
                  name="error_message"
                  value={form.error_message}
                  onChange={handleChange}
                  placeholder="e.g. 'user_id'"
                  required
                />
              </div>

              <div className="form-group">
                <label>Traceback</label>

                <textarea
                  name="traceback"
                  value={form.traceback}
                  onChange={handleChange}
                  placeholder={`Paste the Python traceback here...

Example:
Traceback (most recent call last):
  File "backend/app.py", line 42, in get_user
    user_id = data["user_id"]
KeyError: 'user_id'`}
                  rows="9"
                  required
                />
              </div>

              <button
                type="submit"
                className="analyze-btn"
                disabled={loading}
              >
                {loading
                  ? "Analyzing..."
                  : "Analyze & Repair"}
              </button>
            </form>

            {message && (
              <div
                className={
                  result
                    ? "success-message"
                    : "error-message"
                }
              >
                {message}
              </div>
            )}
          </div>

          <div className="card result-card">
            <div className="card-header">
              <div>
                <h2>Repair Result</h2>
                <p>
                  Analysis and generated repair will appear here.
                </p>
              </div>
            </div>

            {!result && !loading && (
              <div className="empty-result">
                <div className="empty-icon">✓</div>

                <h3>No repair yet</h3>

                <p>
                  Submit an error to start the RepairX
                  investigation.
                </p>
              </div>
            )}

            {loading && (
              <div className="empty-result">
                <div className="loader"></div>

                <h3>Investigating error...</h3>

                <p>
                  RepairX is analyzing the failure.
                </p>
              </div>
            )}

            {result && (
              <div className="result-content">
                <div className="result-status">
                  <span>Analysis Complete</span>
                </div>

                <pre>
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;