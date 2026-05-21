from app.models.contact_message import ContactMessage
from sqlalchemy.orm import Session


class ContactRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, contact: ContactMessage) -> ContactMessage:
        self.db.add(contact)
        self.db.commit()
        self.db.refresh(contact)
        return contact
