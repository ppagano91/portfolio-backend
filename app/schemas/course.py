from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CoursePublic(BaseModel):
    """Vista pública de un curso. Mapeada desde el modelo Education (education_type=course)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    institution: str
    description: str | None = None
    category: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    issue_date: date | None = None
    credential_url: str | None = None
    certificate_url: str | None = None
    hours: int | None = None
    skills: list[str] = Field(default_factory=list)
    order_index: int = 0

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: object) -> object:
        if isinstance(value, str):
            return value.lower().strip()
        return value

    @classmethod
    def from_education(cls, education) -> "CoursePublic":
        return cls(
            id=education.id,
            title=education.degree,
            institution=education.institution,
            description=education.description,
            category=education.field_of_study,
            start_date=education.start_date,
            end_date=education.end_date,
            issue_date=education.end_date,
            credential_url=education.institution_url,
            certificate_url=None,
            hours=None,
            skills=[],
            order_index=education.sort_order,
        )
