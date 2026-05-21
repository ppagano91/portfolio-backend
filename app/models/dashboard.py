import enum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class DashboardTool(str, enum.Enum):
    POWERBI = "powerbi"
    STREAMLIT = "streamlit"
    DASH = "dash"
    NOTEBOOK = "notebook"
    OTHER = "other"


class Dashboard(Base, TimestampMixin):
    __tablename__ = "dashboards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tool: Mapped[DashboardTool] = mapped_column(
        Enum(DashboardTool, name="dashboard_tool_enum", native_enum=False),
        nullable=False,
        default=DashboardTool.OTHER,
    )
    embed_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    public_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    project: Mapped["Project | None"] = relationship(back_populates="dashboards")
