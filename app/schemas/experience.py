from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ExperienceBase(BaseModel):
    profile_id: int
    company: str = Field(..., min_length=1, max_length=255)
    position: str = Field(..., min_length=1, max_length=255)
    employment_type: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    summary: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    company_url: str | None = Field(None, max_length=500)
    sort_order: int = 0
    published: bool = True


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    profile_id: int | None = None
    company: str | None = Field(None, min_length=1, max_length=255)
    position: str | None = Field(None, min_length=1, max_length=255)
    employment_type: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=255)
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None
    summary: str | None = None
    responsibilities: list[str] | None = None
    technologies: list[str] | None = None
    company_url: str | None = Field(None, max_length=500)
    sort_order: int | None = None
    published: bool | None = None


class ExperienceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile_id: int
    company: str
    position: str
    employment_type: str | None
    location: str | None
    start_date: date | None
    end_date: date | None
    is_current: bool
    summary: str | None
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    company_url: str | None
    sort_order: int
    published: bool
    created_at: datetime
    updated_at: datetime


class ExperiencePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    position: str
    employment_type: str | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    summary: str | None = None
    responsibilities: list[str] = Field(default_factory=list)
    technologies: list[str] = Field(default_factory=list)
    company_url: str | None = None
    sort_order: int = 0
