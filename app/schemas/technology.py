from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.technology import TechnologyCategory


class TechnologyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: TechnologyCategory = TechnologyCategory.OTHER
    icon_url: str | None = Field(None, max_length=500)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category(cls, value: object) -> object:
        if isinstance(value, str):
            return value.lower()
        return value


class TechnologyCreate(TechnologyBase):
    pass


class TechnologyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: TechnologyCategory
    icon_url: str | None
