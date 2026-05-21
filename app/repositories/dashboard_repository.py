from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.dashboard import Dashboard


class DashboardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Dashboard]:
        stmt = select(Dashboard).order_by(Dashboard.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, dashboard_id: int) -> Dashboard | None:
        return self.db.get(Dashboard, dashboard_id)

    def create(self, dashboard: Dashboard) -> Dashboard:
        self.db.add(dashboard)
        self.db.commit()
        self.db.refresh(dashboard)
        return dashboard
