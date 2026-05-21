from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notebook import Notebook


class NotebookRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Notebook]:
        stmt = select(Notebook).order_by(Notebook.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, notebook_id: int) -> Notebook | None:
        return self.db.get(Notebook, notebook_id)

    def create(self, notebook: Notebook) -> Notebook:
        self.db.add(notebook)
        self.db.commit()
        self.db.refresh(notebook)
        return notebook
