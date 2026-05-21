from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.dashboard import DashboardTool


class DashboardBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    tool: DashboardTool = DashboardTool.OTHER
    embed_url: str | None = Field(None, max_length=500)
    public_url: str | None = Field(None, max_length=500)
    project_id: int | None = None


class DashboardCreate(DashboardBase):
    pass


class DashboardRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    tool: DashboardTool
    embed_url: str | None
    public_url: str | None
    project_id: int | None
    created_at: datetime
    updated_at: datetime
