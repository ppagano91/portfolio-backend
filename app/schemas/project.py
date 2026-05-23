from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.project import ProjectStatus, ProjectType
from app.schemas.dashboard import DashboardRead
from app.schemas.notebook import NotebookRead


def _normalize_enum_string(value: object) -> object:
    if isinstance(value, str):
        return value.lower()
    return value


class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    summary: str | None = None
    description: str | None = None
    project_type: ProjectType = ProjectType.OTHER
    status: ProjectStatus = ProjectStatus.DRAFT
    cover_image_url: str | None = Field(None, max_length=500)
    repository_url: str | None = Field(None, max_length=500)
    demo_url: str | None = Field(None, max_length=500)
    documentation_url: str | None = Field(None, max_length=500)
    featured: bool = False
    published: bool = False
    technology_ids: list[int] = Field(default_factory=list)

    @field_validator("project_type", mode="before")
    @classmethod
    def normalize_project_type(cls, value: object) -> object:
        return _normalize_enum_string(value)

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: object) -> object:
        return _normalize_enum_string(value)


class ProjectCreate(ProjectBase):
    slug: str | None = Field(None, max_length=255)


class ProjectUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, max_length=255)
    summary: str | None = None
    description: str | None = None
    project_type: ProjectType | None = None
    status: ProjectStatus | None = None
    cover_image_url: str | None = Field(None, max_length=500)
    repository_url: str | None = Field(None, max_length=500)
    demo_url: str | None = Field(None, max_length=500)
    documentation_url: str | None = Field(None, max_length=500)
    featured: bool | None = None
    published: bool | None = None
    technology_ids: list[int] | None = None

    @field_validator("project_type", mode="before")
    @classmethod
    def normalize_project_type(cls, value: object) -> object:
        return _normalize_enum_string(value)

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value: object) -> object:
        return _normalize_enum_string(value)


class TechnologyBrief(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    icon_url: str | None = None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: str | None
    description: str | None
    project_type: ProjectType
    status: ProjectStatus
    cover_image_url: str | None
    repository_url: str | None
    demo_url: str | None
    documentation_url: str | None
    featured: bool
    published: bool
    created_at: datetime
    updated_at: datetime
    technologies: list[TechnologyBrief] = Field(default_factory=list)


class ProjectLocationRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ProjectDetailRead(ProjectRead):
    dashboards: list[DashboardRead] = Field(default_factory=list)
    notebooks: list[NotebookRead] = Field(default_factory=list)
    locations: list[ProjectLocationRead] = Field(default_factory=list)
