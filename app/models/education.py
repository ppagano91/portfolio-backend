import enum
from datetime import date

from sqlalchemy import Boolean, Date, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class EducationType(str, enum.Enum):
    FORMAL = "formal"
    COURSE = "course"


def _education_type_values(enum_cls: type[EducationType]) -> list[str]:
    return [member.value for member in enum_cls]


class Education(Base, TimestampMixin):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[str] = mapped_column(String(255), nullable=False)
    field_of_study: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    institution_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    education_type: Mapped[EducationType] = mapped_column(
        Enum(
            EducationType,
            name="education_type_enum",
            native_enum=False,
            values_callable=_education_type_values,
        ),
        nullable=False,
        default=EducationType.FORMAL,
        index=True,
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    published: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
