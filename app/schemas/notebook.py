from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotebookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    notebook_url: str | None = Field(None, max_length=500)
    repository_url: str | None = Field(None, max_length=500)
    project_id: int | None = None


class NotebookCreate(NotebookBase):
    pass


class NotebookRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    notebook_url: str | None
    repository_url: str | None
    project_id: int | None
    created_at: datetime
    updated_at: datetime
