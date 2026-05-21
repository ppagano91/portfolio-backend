from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.technology import Technology


class TechnologyRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Technology]:
        stmt = select(Technology).order_by(Technology.name)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, technology_id: int) -> Technology | None:
        return self.db.get(Technology, technology_id)

    def get_by_name(self, name: str) -> Technology | None:
        stmt = select(Technology).where(Technology.name == name)
        return self.db.scalar(stmt)

    def get_by_ids(self, technology_ids: list[int]) -> list[Technology]:
        if not technology_ids:
            return []
        stmt = select(Technology).where(Technology.id.in_(technology_ids))
        return list(self.db.scalars(stmt).all())

    def create(self, technology: Technology) -> Technology:
        self.db.add(technology)
        self.db.commit()
        self.db.refresh(technology)
        return technology
