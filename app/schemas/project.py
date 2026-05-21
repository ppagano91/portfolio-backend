from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.project import ProjectStatus, ProjectType


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
