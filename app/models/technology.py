import enum

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.project import project_technologies


class TechnologyCategory(str, enum.Enum):
    BACKEND = "backend"
    FRONTEND = "frontend"
    DATABASE = "database"
    GIS = "gis"
    DATA = "data"
    DEVOPS = "devops"
    OTHER = "other"


def _technology_category_values(enum_cls: type[TechnologyCategory]) -> list[str]:
    return [member.value for member in enum_cls]


class Technology(Base):
    __tablename__ = "technologies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    category: Mapped[TechnologyCategory] = mapped_column(
        Enum(
            TechnologyCategory,
            name="technology_category_enum",
            native_enum=False,
            values_callable=_technology_category_values,
        ),
        nullable=False,
        default=TechnologyCategory.OTHER,
    )
    icon_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    projects: Mapped[list["Project"]] = relationship(
        secondary=project_technologies,
        back_populates="technologies",
    )
