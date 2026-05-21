from app.core.errors import NotFoundError
from app.models.experience import Experience
from app.repositories.experience_repository import ExperienceRepository
from app.repositories.profile_repository import ProfileRepository
from app.schemas.experience import ExperienceCreate, ExperiencePublic, ExperienceRead, ExperienceUpdate


class ExperienceService:
    def __init__(
        self,
        experience_repo: ExperienceRepository,
        profile_repo: ProfileRepository,
    ) -> None:
        self.experience_repo = experience_repo
        self.profile_repo = profile_repo

    def _ensure_profile(self, profile_id: int) -> None:
        if not self.profile_repo.get_by_id(profile_id):
            raise NotFoundError("Perfil", profile_id)

    def _to_public(self, experience: Experience) -> ExperiencePublic:
        return ExperiencePublic.model_validate(experience)

    def list_experiences(self, *, published_only: bool = True) -> list[ExperiencePublic]:
        experiences = self.experience_repo.get_all(published_only=published_only)
        return [self._to_public(exp) for exp in experiences]

    def list_profile_experiences(
        self,
        profile_id: int,
        *,
        published_only: bool = True,
    ) -> list[ExperiencePublic]:
        self._ensure_profile(profile_id)
        experiences = self.experience_repo.get_by_profile(
            profile_id, published_only=published_only
        )
        return [self._to_public(exp) for exp in experiences]

    def get_experience(
        self,
        experience_id: int,
        *,
        published_only: bool = False,
    ) -> ExperienceRead:
        experience = self.experience_repo.get_by_id(experience_id)
        if not experience:
            raise NotFoundError("Experiencia", experience_id)
        if published_only and not experience.published:
            raise NotFoundError("Experiencia", experience_id)
        return ExperienceRead.model_validate(experience)

    def get_public_experience(self, experience_id: int) -> ExperiencePublic:
        experience = self.experience_repo.get_by_id(experience_id)
        if not experience or not experience.published:
            raise NotFoundError("Experiencia", experience_id)
        return self._to_public(experience)

    def create_experience(self, data: ExperienceCreate) -> ExperienceRead:
        self._ensure_profile(data.profile_id)
        experience = Experience(**data.model_dump())
        created = self.experience_repo.create(experience)
        return ExperienceRead.model_validate(created)

    def update_experience(self, experience_id: int, data: ExperienceUpdate) -> ExperienceRead:
        experience = self.experience_repo.get_by_id(experience_id)
        if not experience:
            raise NotFoundError("Experiencia", experience_id)

        update_data = data.model_dump(exclude_unset=True)
        new_profile_id = update_data.get("profile_id")
        if new_profile_id is not None:
            self._ensure_profile(new_profile_id)

        for field, value in update_data.items():
            setattr(experience, field, value)

        updated = self.experience_repo.update(experience)
        return ExperienceRead.model_validate(updated)

    def delete_experience(self, experience_id: int) -> None:
        experience = self.experience_repo.get_by_id(experience_id)
        if not experience:
            raise NotFoundError("Experiencia", experience_id)
        self.experience_repo.delete(experience)
