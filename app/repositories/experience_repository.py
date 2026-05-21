from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.experience import Experience


class ExperienceRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _ordered(self, stmt):
        return stmt.order_by(
            Experience.sort_order.asc(),
            Experience.is_current.desc(),
            Experience.start_date.desc().nulls_last(),
        )

    def get_all(self, *, published_only: bool = True) -> list[Experience]:
        stmt = select(Experience)
        if published_only:
            stmt = stmt.where(Experience.published.is_(True))
        return list(self.db.scalars(self._ordered(stmt)).all())

    def get_by_id(self, experience_id: int) -> Experience | None:
        stmt = select(Experience).where(Experience.id == experience_id)
        return self.db.scalar(stmt)

    def get_by_profile(
        self,
        profile_id: int,
        *,
        published_only: bool = True,
    ) -> list[Experience]:
        stmt = select(Experience).where(Experience.profile_id == profile_id)
        if published_only:
            stmt = stmt.where(Experience.published.is_(True))
        return list(self.db.scalars(self._ordered(stmt)).all())

    def create(self, experience: Experience) -> Experience:
        self.db.add(experience)
        self.db.commit()
        self.db.refresh(experience)
        return experience

    def update(self, experience: Experience) -> Experience:
        self.db.commit()
        self.db.refresh(experience)
        return experience

    def delete(self, experience: Experience) -> None:
        self.db.delete(experience)
        self.db.commit()
