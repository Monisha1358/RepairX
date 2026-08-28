from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from backend.auth.database import Base, engine
from backend.auth.routes import router as auth_router
from backend.projects.routes import router as projects_router
from backend.integrations.github_routes import router as github_router
from backend.services.repair_orchestrator import RepairOrchestrator


# ============================================================
# REPAIRX API
# ============================================================

app = FastAPI(
    title="RepairX API",
    version="1.0.0",
    description="AI-powered API observability and automated repair platform",
)


# ============================================================
# DATABASE
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(github_router)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATA MODELS
# ============================================================

class RepairRequest(BaseModel):
    repository: Optional[str] = None
    file_path: Optional[str] = None
    error_message: Optional[str] = None
    endpoint: Optional[str] = None
    error_type: Optional[str] = "KeyError"
    traceback: Optional[str] = None


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "service": "RepairX API",
        "status": "running",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/api/v1/health")
def health():
    return {
        "status": "healthy",
        "service": "RepairX API",
        "version": "1.0.0",
    }


# ============================================================
# CREATE REPAIR
# ============================================================

@app.post("/api/v1/repairs")
def create_repair(request: RepairRequest):

    # --------------------------------------------------------
    # DEMO REPOSITORY
    # --------------------------------------------------------

    repo_path = "demo_repo"

    # --------------------------------------------------------
    # USE PROVIDED TRACEBACK
    # --------------------------------------------------------

    traceback_text = request.traceback

    if not traceback_text:
        traceback_text = f"""Traceback (most recent call last):
  File "{request.file_path or 'demo_repo/app.py'}", line 17, get_user
    username = users[user_id]
KeyError: {request.error_message or '99'}
"""

    # --------------------------------------------------------
    # RUN REPAIRX ORCHESTRATOR
    # --------------------------------------------------------

    try:

        orchestrator = RepairOrchestrator(repo_path)

        result = orchestrator.repair(
            error_type=request.error_type or "KeyError",
            error_message=request.error_message or "99",
            traceback=traceback_text,
        )

        return {
            "status": result.get("status"),
            "message": "Repair pipeline completed",
            "repair": result,
        }

    except Exception as error:

        return {
            "status": "FAILED",
            "message": "Repair pipeline failed",
            "error": str(error),
        }


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
async def startup_event():

    print("========================================")
    print("        RepairX API Started")
    print("========================================")
    print("API      : http://127.0.0.1:8000")
    print("Docs     : http://127.0.0.1:8000/docs")
    print("Frontend : http://localhost:5174")
    print("========================================")