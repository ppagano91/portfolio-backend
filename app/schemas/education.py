from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.education import EducationType


class EducationBase(BaseModel):
    institution: str = Field(..., min_length=1, max_length=255)
    degree: str = Field(..., min_length=1, max_length=255)
    field_of_study: str | None = Field(None, max_length=255)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    location: str | None = Field(None, max_length=255)
    institution_url: str | None = Field(None, max_length=500)
    education_type: EducationType = EducationType.FORMAL
    sort_order: int = 0
    published: bool = True

    @field_validator("education_type", mode="before")
    @classmethod
    def normalize_education_type(cls, value: object) -> object:
        if isinstance(value, str):
            return value.lower()
        return value

class EducationCreate(EducationBase):
    pass


class EducationUpdate(BaseModel):
    institution: str | None = Field(None, min_length=1, max_length=255)
    degree: str | None = Field(None, min_length=1, max_length=255)
    field_of_study: str | None = Field(None, max_length=255)
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool | None = None
    location: str | None = Field(None, max_length=255)
    institution_url: str | None = Field(None, max_length=500)
    education_type: EducationType | None = None
    sort_order: int | None = None
    published: bool | None = None

    @field_validator("education_type", mode="before")
    @classmethod
    def normalize_education_type(cls, value: object) -> object:
        if isinstance(value, str):
            return value.lower()
        return value


class EducationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution: str
    degree: str
    field_of_study: str | None
    description: str | None
    start_date: date | None
    end_date: date | None
    is_current: bool
    location: str | None
    institution_url: str | None
    education_type: EducationType
    sort_order: int
    published: bool
    created_at: datetime
    updated_at: datetime


class EducationPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution: str
    degree: str
    field_of_study: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_current: bool = False
    location: str | None = None
    institution_url: str | None = None
    education_type: EducationType
    sort_order: int = 0
