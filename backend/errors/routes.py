from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.auth.database import get_db
from backend.errors.models import ErrorEvent


router = APIRouter(
    prefix="/api/v1/errors",
    tags=["Errors"],
)


class ErrorIngestRequest(BaseModel):
    repository: str
    endpoint: str | None = None
    error_type: str
    error_message: str
    file_path: str | None = None
    traceback: str | None = None


@router.post("")
def ingest_error(
    request: ErrorIngestRequest,
    db: Session = Depends(get_db),
):
    error_event = ErrorEvent(
        repository=request.repository,
        endpoint=request.endpoint,
        error_type=request.error_type,
        error_message=request.error_message,
        file_path=request.file_path,
        traceback=request.traceback,
        status="NEW",
    )

    db.add(error_event)
    db.commit()
    db.refresh(error_event)

    return {
        "status": "RECEIVED",
        "message": "Error successfully ingested by RepairX",
        "error_id": error_event.id,
    }
@router.get("")
def get_errors(
    db: Session = Depends(get_db),
):
    errors = (
        db.query(ErrorEvent)
        .order_by(ErrorEvent.created_at.desc())
        .all()
    )

    return {
        "errors": [
            {
                "id": error.id,
                "repository": error.repository,
                "endpoint": error.endpoint,
                "error_type": error.error_type,
                "error_message": error.error_message,
                "file_path": error.file_path,
                "traceback": error.traceback,
                "status": error.status,
                "created_at": error.created_at.isoformat(),
            }
            for error in errors
        ]
    }