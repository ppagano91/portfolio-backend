from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class ProjectLocation(Base):
    """
    GIS-ready location for projects.
    Geometry: Point in EPSG:4326 (WGS84).
    """

    __tablename__ = "project_locations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    geom = mapped_column(Geometry(geometry_type="POINT", srid=4326), nullable=True)

    project: Mapped["Project"] = relationship(back_populates="locations")
