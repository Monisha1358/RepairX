import { useEffect, useState } from "react";
import "./App.css";
import Auth from "./Auth";

const API_URL = "http://127.0.0.1:8000";

function App() {
  // ============================================================
  // USER
  // ============================================================

  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem("repairx_user");

    try {
      return savedUser ? JSON.parse(savedUser) : null;
    } catch {
      return null;
    }
  });

  const [active, setActive] = useState("Dashboard");

  // ============================================================
  // BACKEND
  // ============================================================

  const [backend, setBackend] = useState({
    online: false,
    version: "-",
  });

  // ============================================================
  // PROJECTS
  // ============================================================

  const [projects, setProjects] = useState([]);
  const [projectName, setProjectName] = useState("");
  const [repository, setRepository] = useState("");
  const [loadingProjects, setLoadingProjects] = useState(false);
  const [creatingProject, setCreatingProject] = useState(false);
  const [projectMessage, setProjectMessage] = useState("");

  // ============================================================
  // REPAIR
  // ============================================================

  const [repairResult, setRepairResult] = useState(null);

  // ============================================================
  // BACKEND HEALTH
  // ============================================================

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch(
          `${API_URL}/api/v1/health`
        );

        if (!response.ok) {
          throw new Error("Backend error");
        }

        const data = await response.json();

        setBackend({
          online: true,
          version: data.version || "-",
        });
      } catch {
        setBackend({
          online: false,
          version: "-",
        });
      }
    };

    checkBackend();

    const interval = setInterval(checkBackend, 5000);

    return () => clearInterval(interval);
  }, []);

  // ============================================================
  // LOAD PROJECTS
  // ============================================================

  const loadProjects = async () => {
    setLoadingProjects(true);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/projects`
      );

      if (!response.ok) {
        throw new Error("Unable to load projects");
      }

      const data = await response.json();

      setProjects(data.projects || []);
    } catch (error) {
      console.error("Project loading failed:", error);
    } finally {
      setLoadingProjects(false);
    }
  };

  useEffect(() => {
    if (user) {
      loadProjects();
    }
  }, [user]);

  // ============================================================
  // CREATE PROJECT
  // ============================================================

  const createProject = async (event) => {
    event.preventDefault();

    setProjectMessage("");

    if (!projectName.trim() || !repository.trim()) {
      setProjectMessage(
        "Please enter both project name and repository."
      );
      return;
    }

    setCreatingProject(true);

    try {
      const response = await fetch(
        `${API_URL}/api/v1/projects`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: projectName.trim(),
            repository: repository.trim(),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Project creation failed"
        );
      }

      if (data.project) {
        setProjects((previousProjects) => [
          ...previousProjects,
          data.project,
        ]);
      }

      setProjectName("");
      setRepository("");

      setProjectMessage(
        "Project connected successfully."
      );
    } catch (error) {
      setProjectMessage(
        error.message || "Project connection failed."
      );
    } finally {
      setCreatingProject(false);
    }
  };

  // ============================================================
  // LOGIN
  // ============================================================

  const handleLogin = (loggedInUser) => {
    setUser(loggedInUser);
    setActive("Dashboard");

    localStorage.setItem(
      "repairx_user",
      JSON.stringify(loggedInUser)
    );
  };

  // ============================================================
  // LOGOUT
  // ============================================================

  const handleLogout = () => {
    localStorage.removeItem("repairx_user");

    setUser(null);
    setActive("Dashboard");
  };

  // ============================================================
  // GITHUB
  // ============================================================

  const connectGitHub = async () => {
    try {
      const response = await fetch(
        `${API_URL}/api/v1/github/login`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to start GitHub connection."
        );
      }

      if (!data.authorization_url) {
        throw new Error(
          "GitHub authorization URL was not returned."
        );
      }

      window.location.href = data.authorization_url;
    } catch (error) {
      console.error(
        "GitHub connection failed:",
        error
      );

      alert(
        error.message ||
          "GitHub connection could not be started."
      );
    }
  };

  // ============================================================
  // AUTH
  // ============================================================

  if (!user) {
    return <Auth onLogin={handleLogin} />;
  }

  // ============================================================
  // MENU
  // ============================================================

  const menu = [
    "Dashboard",
    "Projects",
    "APIs",
    "Logs",
    "Repairs",
    "GitHub",
  ];

  return (
    <div className="app">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="sidebar">

        <div className="brand">

          <div className="logo">
            R
          </div>

          <div>
            <h2>
              RepairX
            </h2>

            <span>
              AI API Engineer
            </span>
          </div>

        </div>

        <nav>

          {menu.map((item) => (

            <button
              key={item}
              className={
                active === item
                  ? "nav-item active"
                  : "nav-item"
              }
              onClick={() => setActive(item)}
            >

              <span className="nav-icon">

                {item === "Dashboard" && "◆"}

                {item === "Projects" && "▣"}

                {item === "APIs" && "◫"}

                {item === "Logs" && "◷"}

                {item === "Repairs" && "◇"}

                {item === "GitHub" && "●"}

              </span>

              {item}

            </button>

          ))}

        </nav>

        <div className="sidebar-bottom">

          <button
            className={
              active === "Settings"
                ? "nav-item active"
                : "nav-item"
            }
            onClick={() =>
              setActive("Settings")
            }
          >
            ⚙ Settings
          </button>

          <div className="profile">

            <div className="avatar">

              {user.name
                ? user.name
                    .charAt(0)
                    .toUpperCase()
                : "U"}

            </div>

            <div>

              <strong>
                {user.name || "User"}
              </strong>

              <span>
                Developer
              </span>

            </div>

          </div>

          <button
            className="nav-item logout-button"
            onClick={handleLogout}
          >
            ↪ Logout
          </button>

        </div>

      </aside>

      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="main">

        {/* ====================================================
            HEADER
        ==================================================== */}

        <header className="topbar">

          <div>

            <div className="breadcrumb">
              REPAIRX / {active.toUpperCase()}
            </div>

            <h1>
              {active}
            </h1>

            <p>

              {active === "Dashboard" &&
                "Overview of your applications, APIs and automated repairs."}

              {active === "Projects" &&
                "Connect your applications and GitHub repositories."}

              {active === "APIs" &&
                "Monitor API endpoints and request activity."}

              {active === "Logs" &&
                "Inspect application errors and system events."}

              {active === "Repairs" &&
                "Review automated repairs generated by RepairX."}

              {active === "GitHub" &&
                "Manage your connected GitHub repositories."}

              {active === "Settings" &&
                "Manage your RepairX account and preferences."}

            </p>

          </div>

          <div className="header-actions">

            <button className="icon-button">
              ⌕
            </button>

            <button className="icon-button">
              ◔
            </button>

            <div className="user-mini">

              {user.name
                ? user.name
                    .charAt(0)
                    .toUpperCase()
                : "U"}

            </div>

          </div>

        </header>

        {/* ====================================================
            DASHBOARD
        ==================================================== */}

        {active === "Dashboard" && (

          <>

            <div className="backend-status">

              <span
                className={
                  backend.online
                    ? "backend-dot online"
                    : "backend-dot offline"
                }
              />

              <strong>

                {backend.online
                  ? "Backend Online"
                  : "Backend Offline"}

              </strong>

              <span className="api-version">
                API v{backend.version}
              </span>

            </div>

            <section className="stats">

              <Stat
                title="PROJECTS"
                value={String(
                  projects.length
                ).padStart(2, "0")}
              />

              <Stat
                title="APPLICATIONS"
                value={String(
                  projects.length
                ).padStart(2, "0")}
              />

              <Stat
                title="API REQUESTS"
                value="128"
              />

              <Stat
                title="ERROR RATE"
                value="0.8%"
                danger
              />

              <Stat
                title="REPAIRS"
                value="09"
                success
              />

            </section>

            <section className="dashboard-grid">

              {/* ================= ACTIVITY ================= */}

              <div className="panel activity-panel">

                <div className="panel-header">

                  <div>

                    <h2>
                      Recent API Activity
                    </h2>

                    <p>
                      Live requests from your connected application
                    </p>

                  </div>

                  <span className="live">

                    <span className="dot"></span>

                    LIVE

                  </span>

                </div>

                <div className="table">

                  <div className="table-head">

                    <span>
                      METHOD
                    </span>

                    <span>
                      ENDPOINT
                    </span>

                    <span>
                      STATUS
                    </span>

                    <span>
                      LATENCY
                    </span>

                  </div>

                  <Request
                    method="GET"
                    endpoint="/users/1"
                    status="200"
                    latency="38ms"
                  />

                  <Request
                    method="GET"
                    endpoint="/users/2"
                    status="200"
                    latency="42ms"
                  />

                  <Request
                    method="GET"
                    endpoint="/users/99"
                    status="500"
                    latency="91ms"
                    error
                  />

                  <Request
                    method="POST"
                    endpoint="/api/checkout"
                    status="200"
                    latency="126ms"
                  />

                </div>

              </div>

              {/* ================= AI ANALYSIS ================= */}

              <div className="panel analysis-panel">

                <div className="panel-header">

                  <div>

                    <h2>
                      AI Repair Analysis
                    </h2>

                    <p>
                      Latest detected issue
                    </p>

                  </div>

                  <span className="ai-badge">
                    AI
                  </span>

                </div>

                <div className="error-box">

                  <span>
                    500
                  </span>

                  <div>

                    <strong>
                      KeyError
                    </strong>

                    <p>
                      GET /users/99
                    </p>

                  </div>

                </div>

                <div className="analysis-item">

                  <label>
                    ROOT CAUSE
                  </label>

                  <p>
                    The requested user_id does not exist
                    in the users dictionary, causing a
                    direct lookup to fail.
                  </p>

                </div>

                <div className="confidence">

                  <div>

                    <span>
                      CONFIDENCE
                    </span>

                    <strong>
                      100%
                    </strong>

                  </div>

                  <div className="progress">
                    <div></div>
                  </div>

                </div>

                <div className="analysis-item">

                  <label>
                    AFFECTED FILE
                  </label>

                  <code>
                    demo_repo/app.py : 17
                  </code>

                </div>

                <button
                  className="repair-button"
                  onClick={() =>
                    setActive("Repairs")
                  }
                >
                  View Repair →
                </button>

              </div>

            </section>

            {/* ================= PIPELINE ================= */}

            <section className="panel pipeline">

              <div className="panel-header">

                <div>

                  <h2>
                    Repair Pipeline
                  </h2>

                  <p>
                    Automated root-cause-driven repair workflow
                  </p>

                </div>

                <span className="completed">
                  COMPLETED
                </span>

              </div>

              <div className="steps">

                <Step
                  number="01"
                  title="Detect"
                  text="Git Detective"
                />

                <Step
                  number="02"
                  title="Analyze"
                  text="Root Cause"
                />

                <Step
                  number="03"
                  title="Generate"
                  text="Minimal Patch"
                />

                <Step
                  number="04"
                  title="Validate"
                  text="Risk Gate"
                />

                <Step
                  number="05"
                  title="Prove"
                  text="Behavior Test"
                />

                <Step
                  number="06"
                  title="Impact"
                  text="Blast Radius"
                />

              </div>

            </section>

            {/* ================= GITHUB CARD ================= */}

            <section className="github-card">

              <div>

                <div className="github-title">

                  <span className="github-icon">
                    ●
                  </span>

                  <div>

                    <h2>
                      GitHub Repository
                    </h2>

                    <p>
                      Connect a repository to begin automated analysis
                    </p>

                  </div>

                </div>

              </div>

              <button
                className="outline-button"
                onClick={connectGitHub}
              >
                Connect GitHub
              </button>

            </section>

          </>

        )}

        {/* ====================================================
            PROJECTS
        ==================================================== */}

        {active === "Projects" && (

          <section className="projects-page">

            <div className="page-section-header">

              <div>

                <h2>
                  Your Projects
                </h2>

                <p>
                  Connect an application repository to RepairX.
                </p>

              </div>

            </div>

            <div className="panel create-project-panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Connect a Repository
                  </h2>

                  <p>
                    Add your GitHub repository to start
                    monitoring and repairing your application.
                  </p>

                </div>

              </div>

              <form onSubmit={createProject}>

                <div className="form-group">

                  <label>
                    PROJECT NAME
                  </label>

                  <input
                    type="text"
                    placeholder="My Backend API"
                    value={projectName}
                    onChange={(event) =>
                      setProjectName(
                        event.target.value
                      )
                    }
                  />

                </div>

                <div className="form-group">

                  <label>
                    GITHUB REPOSITORY
                  </label>

                  <input
                    type="text"
                    placeholder="https://github.com/username/repository"
                    value={repository}
                    onChange={(event) =>
                      setRepository(
                        event.target.value
                      )
                    }
                  />

                </div>

                <button
                  type="submit"
                  className="repair-button connect-button"
                  disabled={creatingProject}
                >

                  {creatingProject
                    ? "Connecting..."
                    : "Connect Repository →"}

                </button>

                {projectMessage && (

                  <p className="project-message">
                    {projectMessage}
                  </p>

                )}

              </form>

            </div>

            <div className="panel projects-list-panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Connected Projects
                  </h2>

                  <p>
                    Repositories currently connected to RepairX.
                  </p>

                </div>

              </div>

              {loadingProjects ? (

                <div className="loading">
                  Loading projects...
                </div>

              ) : projects.length === 0 ? (

                <div className="no-projects">

                  <div className="empty-icon">
                    ◇
                  </div>

                  <h3>
                    No projects connected
                  </h3>

                  <p>
                    Connect your first GitHub repository above.
                  </p>

                </div>

              ) : (

                <div className="project-list">

                  {projects.map((project) => (

                    <div
                      className="project-row"
                      key={project.id}
                    >

                      <div className="project-info">

                        <div className="project-icon">
                          R
                        </div>

                        <div className="project-details">

                          <strong>
                            {project.name}
                          </strong>

                          <span className="repository-url">
                            {project.repository}
                          </span>

                        </div>

                      </div>

                      <div className="project-status">

                        <span className="status-dot"></span>

                        <span>
                          {project.status || "Connected"}
                        </span>

                      </div>

                    </div>

                  ))}

                </div>

              )}

            </div>

          </section>

        )}

        {/* ====================================================
            APIS
        ==================================================== */}

        {active === "APIs" && (

          <section className="module-page">

            <div className="panel">

              <div className="panel-header">

                <div>

                  <h2>
                    API Monitoring
                  </h2>

                  <p>
                    Monitor endpoints from your connected applications.
                  </p>

                </div>

                <span className="live">

                  <span className="dot"></span>

                  LIVE

                </span>

              </div>

              <div className="module-content">

                <div className="api-item">

                  <code>
                    GET /users/1
                  </code>

                  <span className="status">
                    200
                  </span>

                  <span>
                    38ms
                  </span>

                </div>

                <div className="api-item">

                  <code>
                    GET /users/2
                  </code>

                  <span className="status">
                    200
                  </span>

                  <span>
                    42ms
                  </span>

                </div>

                <div className="api-item error-row">

                  <code>
                    GET /users/99
                  </code>

                  <span className="status error">
                    500
                  </span>

                  <span>
                    91ms
                  </span>

                </div>

              </div>

            </div>

          </section>

        )}

        {/* ====================================================
            LOGS
        ==================================================== */}

        {active === "Logs" && (

          <section className="module-page">

            <div className="panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Application Logs
                  </h2>

                  <p>
                    Recent events detected by RepairX.
                  </p>

                </div>

              </div>

              <div className="log-list">

                <div className="log-item">

                  <span>
                    INFO
                  </span>

                  Application request received

                </div>

                <div className="log-item">

                  <span>
                    INFO
                  </span>

                  User request processed

                </div>

                <div className="log-item error-log">

                  <span>
                    ERROR
                  </span>

                  KeyError detected at /users/99

                </div>

              </div>

            </div>

          </section>

        )}

        {/* ====================================================
            REPAIRS
        ==================================================== */}

        {active === "Repairs" && (

          <section className="module-page">

            <div className="panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Automated Repairs
                  </h2>

                  <p>
                    Root-cause analysis and generated repairs.
                  </p>

                </div>

                <span className="ai-badge">
                  AI
                </span>

              </div>

              <div className="repair-detail">

                <div className="repair-number">
                  500
                </div>

                <div>

                  <h3>
                    KeyError detected
                  </h3>

                  <p>
                    GET /users/99
                  </p>

                  <code>
                    demo_repo/app.py : 17
                  </code>

                </div>

              </div>

              <div className="repair-analysis">

                <label>
                  ROOT CAUSE
                </label>

                <p>
                  The requested user_id does not exist
                  in the users dictionary.
                </p>

              </div>

              <div className="repair-analysis">

                <label>
                  REPAIR PIPELINE
                </label>

                <div className="repair-pipeline-status">

                  <span>
                    ✓ Git Detective
                  </span>

                  <span>
                    ✓ Root Cause
                  </span>

                  <span>
                    ✓ Minimal Patch
                  </span>

                  <span>
                    ✓ Risk Gate
                  </span>

                  <span>
                    ✓ Behavior Test
                  </span>

                  <span>
                    ✓ Blast Radius
                  </span>

                </div>

              </div>

            </div>

          </section>

        )}

        {/* ====================================================
            GITHUB
        ==================================================== */}

        {active === "GitHub" && (

          <section className="module-page">

            <div className="panel">

              <div className="panel-header">

                <div>

                  <h2>
                    GitHub Integration
                  </h2>

                  <p>
                    Repositories available from your GitHub account.
                  </p>

                </div>

                <span className="ai-badge">
                  GITHUB
                </span>

              </div>

              <div className="github-connect">

                <div className="github-large-icon">
                  ●
                </div>

                <h3>
                  Connect GitHub
                </h3>

                <p>
                  Authorize RepairX to access your GitHub
                  repositories and begin automated analysis.
                </p>

                <button
                  className="repair-button"
                  onClick={connectGitHub}
                >
                  Connect GitHub →
                </button>

              </div>

              <div className="module-content">

                <h3>
                  Connected Repositories
                </h3>

                <p>
                  Repositories currently connected to RepairX.
                </p>

                <div className="project-list">

                  <div className="project-row">

                    <div className="project-info">

                      <div className="project-icon">
                        R
                      </div>

                      <div className="project-details">

                        <strong>
                          RepairX-AI
                        </strong>

                        <span className="repository-url">
                          Monisha1358/RepairX-AI
                        </span>

                      </div>

                    </div>

                    <div className="project-status">

                      <span className="status-dot"></span>

                      <span>
                        Public
                      </span>

                    </div>

                  </div>

                  <div className="project-row">

                    <div className="project-info">

                      <div className="project-icon">
                        R
                      </div>

                      <div className="project-details">

                        <strong>
                          RepairX
                        </strong>

                        <span className="repository-url">
                          Monisha1358/RepairX
                        </span>

                      </div>

                    </div>

                    <div className="project-status">

                      <span className="status-dot"></span>

                      <span>
                        Public
                      </span>

                    </div>

                  </div>

                </div>

              </div>

            </div>

          </section>

        )}

        {/* ====================================================
            SETTINGS
        ==================================================== */}

        {active === "Settings" && (

          <section className="module-page">

            <div className="panel">

              <div className="panel-header">

                <div>

                  <h2>
                    Account Settings
                  </h2>

                  <p>
                    Your RepairX account information.
                  </p>

                </div>

              </div>

              <div className="settings-content">

                <div className="setting-row">

                  <span>
                    Name
                  </span>

                  <strong>
                    {user.name || "User"}
                  </strong>

                </div>

                <div className="setting-row">

                  <span>
                    Email
                  </span>

                  <strong>
                    {user.email || "-"}
                  </strong>

                </div>

                <div className="setting-row">

                  <span>
                    Backend
                  </span>

                  <strong
                    className={
                      backend.online
                        ? "success"
                        : "danger"
                    }
                  >
                    {backend.online
                      ? "Connected"
                      : "Offline"}
                  </strong>

                </div>

                <div className="setting-row">

                  <span>
                    API Version
                  </span>

                  <strong>
                    {backend.version}
                  </strong>

                </div>

              </div>

            </div>

          </section>

        )}

      </main>

    </div>
  );
}


/* ============================================================
   STAT
============================================================ */

function Stat({
  title,
  value,
  danger,
  success,
}) {
  return (
    <div className="stat-card">

      <span>
        {title}
      </span>

      <strong
        className={
          danger
            ? "danger"
            : success
            ? "success"
            : ""
        }
      >
        {value}
      </strong>

      <small>
        {danger
          ? "1 recent error"
          : "Last 24 hours"}
      </small>

    </div>
  );
}


/* ============================================================
   REQUEST
============================================================ */

function Request({
  method,
  endpoint,
  status,
  latency,
  error,
}) {
  return (
    <div
      className={
        error
          ? "table-row error-row"
          : "table-row"
      }
    >

      <span className="method">
        {method}
      </span>

      <code>
        {endpoint}
      </code>

      <span
        className={
          error
            ? "status error"
            : "status"
        }
      >
        {status}
      </span>

      <span className="latency">
        {latency}
      </span>

    </div>
  );
}


/* ============================================================
   PIPELINE STEP
============================================================ */

function Step({
  number,
  title,
  text,
}) {
  return (
    <div className="step">

      <div className="step-number">
        {number}
      </div>

      <div className="step-line"></div>

      <strong>
        {title}
      </strong>

      <span>
        {text}
      </span>

    </div>
  );
}


export default App;