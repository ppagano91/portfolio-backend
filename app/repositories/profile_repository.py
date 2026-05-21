from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.profile import Profile


class ProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _with_experiences(self, stmt):
        return stmt.options(selectinload(Profile.experiences))

    def get_active(self, *, with_experiences: bool = False) -> Profile | None:
        stmt = (
            select(Profile)
            .where(Profile.is_active.is_(True))
            .order_by(Profile.sort_order.asc(), Profile.id.asc())
            .limit(1)
        )
        if with_experiences:
            stmt = self._with_experiences(stmt)
        return self.db.scalar(stmt)

    def get_by_id(self, profile_id: int, *, with_experiences: bool = False) -> Profile | None:
        stmt = select(Profile).where(Profile.id == profile_id)
        if with_experiences:
            stmt = self._with_experiences(stmt)
        return self.db.scalar(stmt)

    def get_by_slug(self, slug: str, *, with_experiences: bool = False) -> Profile | None:
        stmt = select(Profile).where(Profile.slug == slug)
        if with_experiences:
            stmt = self._with_experiences(stmt)
        return self.db.scalar(stmt)

    def get_all_slugs(self) -> list[str]:
        stmt = select(Profile.slug)
        return list(self.db.scalars(stmt).all())

    def create(self, profile: Profile) -> Profile:
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def update(self, profile: Profile) -> Profile:
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, profile: Profile) -> None:
        self.db.delete(profile)
        self.db.commit()
