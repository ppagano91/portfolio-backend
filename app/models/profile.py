from sqlalchemy import JSON, Boolean, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.experience import Experience


class Profile(Base, TimestampMixin):
    __tablename__ = "profiles"
    __table_args__ = (UniqueConstraint("slug", name="uq_profiles_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    subtitle: Mapped[str | None] = mapped_column(String(500), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    profile_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cv_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    about_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    about_content: Mapped[str | None] = mapped_column(Text, nullable=True)
    focus_areas: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    key_skills: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    experiences: Mapped[list[Experience]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        order_by=[
            Experience.sort_order.asc(),
            Experience.is_current.desc(),
            Experience.start_date.desc().nulls_last(),
        ],
    )
