import enum

from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

project_technologies = Table(
    "project_technologies",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "technology_id",
        ForeignKey("technologies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class ProjectType(str, enum.Enum):
    WEB = "web"
    GIS = "gis"
    DATA = "data"
    DASHBOARD = "dashboard"
    NOTEBOOK = "notebook"
    API = "api"
    OTHER = "other"


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Project(Base, TimestampMixin):
    __tablename__ = "projects"
    __table_args__ = (UniqueConstraint("slug", name="uq_projects_slug"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_type: Mapped[ProjectType] = mapped_column(
        Enum(ProjectType, name="project_type_enum", native_enum=False),
        nullable=False,
        default=ProjectType.OTHER,
    )
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status_enum", native_enum=False),
        nullable=False,
        default=ProjectStatus.DRAFT,
    )
    cover_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    repository_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    demo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    documentation_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    technologies: Mapped[list["Technology"]] = relationship(
        secondary=project_technologies,
        back_populates="projects",
    )
    dashboards: Mapped[list["Dashboard"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    notebooks: Mapped[list["Notebook"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    locations: Mapped[list["ProjectLocation"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )

