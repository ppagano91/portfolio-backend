from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.experience import ExperiencePublic
from app.utils.lists import normalize_string_list


class ProfileBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    title: str = Field(..., min_length=1, max_length=255)
    subtitle: str | None = Field(None, max_length=500)
    summary: str = Field(..., min_length=1)
    location: str | None = Field(None, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)
    linkedin_url: str | None = Field(None, max_length=500)
    github_url: str | None = Field(None, max_length=500)
    profile_image_url: str | None = Field(None, max_length=500)
    cv_url: str | None = Field(None, max_length=500)
    about_title: str | None = Field(None, max_length=255)
    about_content: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    key_skills: list[str] = Field(default_factory=list)
    is_active: bool = True
    sort_order: int = 0

    @field_validator("focus_areas", "key_skills", mode="before")
    @classmethod
    def normalize_list_fields(cls, value: object) -> list[str]:
        return normalize_string_list(value)


class ProfileCreate(ProfileBase):
    slug: str | None = Field(None, max_length=255)


class ProfileUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    slug: str | None = Field(None, max_length=255)
    title: str | None = Field(None, min_length=1, max_length=255)
    subtitle: str | None = Field(None, max_length=500)
    summary: str | None = Field(None, min_length=1)
    location: str | None = Field(None, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)
    linkedin_url: str | None = Field(None, max_length=500)
    github_url: str | None = Field(None, max_length=500)
    profile_image_url: str | None = Field(None, max_length=500)
    cv_url: str | None = Field(None, max_length=500)
    about_title: str | None = Field(None, max_length=255)
    about_content: str | None = None
    focus_areas: list[str] | None = None
    key_skills: list[str] | None = None
    is_active: bool | None = None
    sort_order: int | None = None

    @field_validator("focus_areas", "key_skills", mode="before")
    @classmethod
    def normalize_list_fields(cls, value: object) -> object:
        if value is None:
            return value
        return normalize_string_list(value)


class ProfileRead(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    created_at: datetime
    updated_at: datetime


class ProfilePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    title: str
    subtitle: str | None = None
    summary: str
    location: str | None = None
    email: str | None = None
    phone: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    profile_image_url: str | None = None
    cv_url: str | None = None
    about_title: str | None = None
    about_content: str | None = None
    focus_areas: list[str] = Field(default_factory=list)
    key_skills: list[str] = Field(default_factory=list)
    experiences: list[ExperiencePublic] = Field(default_factory=list)

    @field_validator("focus_areas", "key_skills", mode="before")
    @classmethod
    def normalize_list_fields(cls, value: object) -> list[str]:
        return normalize_string_list(value)
