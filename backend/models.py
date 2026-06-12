from datetime import datetime, timezone
from typing import Optional, List
from uuid import uuid4

from sqlmodel import SQLModel, Field, Relationship


def _uuid() -> str:
    return str(uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


# -----------------------
# THUMBNAIL MODEL
# -----------------------
class Thumbnail(SQLModel, table=True):
    id: str = Field(default_factory=_uuid, primary_key=True)

    job_id: str = Field(foreign_key="job.id", index=True)

    style_name: str = Field(index=True)

    imagekit_url: Optional[str] = Field(default=None)

    status: str = Field(default="queued", index=True)
    # queued → generating → uploaded → failed

    error_message: Optional[str] = Field(default=None)

    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    job: Optional["Job"] = Relationship(back_populates="thumbnails")


# -----------------------
# JOB MODEL
# -----------------------
class Job(SQLModel, table=True):
    id: str = Field(default_factory=_uuid, primary_key=True)

    prompt: str
    num_thumbnails: int = Field(default=1, ge=1, le=3)

    headshot_url: str

    status: str = Field(default="queued", index=True)
    # queued → processing → completed → failed → partial_success

    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)

    thumbnails: List[Thumbnail] = Relationship(back_populates="job")