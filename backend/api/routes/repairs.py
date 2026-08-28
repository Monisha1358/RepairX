from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.repair_orchestrator import RepairOrchestrator


router = APIRouter(
    prefix="/api/v1",
    tags=["Repairs"]
)


class RepairRequest(BaseModel):
    error_type: str
    error_message: str
    traceback: str
    repo_path: str = "demo_repo"


@router.post("/repairs")
def create_repair(request: RepairRequest):

    try:
        orchestrator = RepairOrchestrator(
            request.repo_path
        )

        result = orchestrator.repair(
            error_type=request.error_type,
            error_message=request.error_message,
            traceback=request.traceback
        )

        return result

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail={
                "status": "FAILED",
                "error": str(error)
            }
        )