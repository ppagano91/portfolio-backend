from app.models.contact_message import ContactMessage
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate


class ContactService:
    def __init__(self, contact_repo: ContactRepository) -> None:
        self.contact_repo = contact_repo

    def create_message(self, data: ContactCreate) -> ContactMessage:
        message = ContactMessage(
            name=data.name,
            email=data.email,
            subject=data.subject,
            message=data.message,
        )
        return self.contact_repo.create(message)
