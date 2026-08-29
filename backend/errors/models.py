from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from backend.auth.database import Base


class ErrorEvent(Base):
    __tablename__ = "error_events"

    id = Column(Integer, primary_key=True, index=True)

    repository = Column(String, nullable=False)
    endpoint = Column(String, nullable=True)

    error_type = Column(String, nullable=False)
    error_message = Column(Text, nullable=False)

    file_path = Column(String, nullable=True)
    traceback = Column(Text, nullable=True)

    status = Column(String, nullable=False, default="NEW")

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )