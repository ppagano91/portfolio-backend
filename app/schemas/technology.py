from pydantic import BaseModel, ConfigDict, Field

from app.models.technology import TechnologyCategory


class TechnologyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: TechnologyCategory = TechnologyCategory.OTHER
    icon_url: str | None = Field(None, max_length=500)


class TechnologyCreate(TechnologyBase):
    pass


class TechnologyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: TechnologyCategory
    icon_url: str | None
