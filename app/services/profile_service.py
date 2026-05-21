from app.core.errors import NotFoundError
from app.models.experience import Experience
from app.models.profile import Profile
from app.repositories.experience_repository import ExperienceRepository
from app.repositories.profile_repository import ProfileRepository
from app.schemas.experience import ExperiencePublic
from app.schemas.profile import ProfileCreate, ProfilePublic, ProfileRead, ProfileUpdate
from app.utils.slug import ensure_unique_slug, slugify


class ProfileService:
    def __init__(
        self,
        profile_repo: ProfileRepository,
        experience_repo: ExperienceRepository | None = None,
    ) -> None:
        self.profile_repo = profile_repo
        self.experience_repo = experience_repo

    def _sort_experiences(self, experiences: list[Experience]) -> list[Experience]:
        return sorted(
            experiences,
            key=lambda e: (
                e.sort_order,
                -int(e.is_current),
                -(e.start_date.toordinal() if e.start_date else 0),
            ),
        )

    def _published_experiences(self, profile: Profile) -> list[ExperiencePublic]:
        published = [exp for exp in profile.experiences if exp.published]
        ordered = self._sort_experiences(published)
        return [ExperiencePublic.model_validate(exp) for exp in ordered]

    def _to_public(self, profile: Profile, *, include_experiences: bool = True) -> ProfilePublic:
        payload = ProfilePublic.model_validate(profile)
        if include_experiences:
            payload.experiences = self._published_experiences(profile)
        else:
            payload.experiences = []
        return payload

    def get_public_profile(self) -> ProfilePublic:
        profile = self.profile_repo.get_active(with_experiences=True)
        if not profile:
            raise NotFoundError("Perfil")
        return self._to_public(profile)

    def get_profile_by_slug(self, slug: str) -> ProfilePublic:
        profile = self.profile_repo.get_by_slug(slug, with_experiences=True)
        if not profile:
            raise NotFoundError("Perfil", slug)
        return self._to_public(profile)

    def _build_slug(self, name: str, slug: str | None) -> str:
        base_slug = slugify(slug or name)
        return ensure_unique_slug(base_slug, self.profile_repo.get_all_slugs())

    def create_profile(self, data: ProfileCreate) -> ProfileRead:
        slug = self._build_slug(data.name, data.slug)
        profile = Profile(slug=slug, **data.model_dump(exclude={"slug"}))
        created = self.profile_repo.create(profile)
        return ProfileRead.model_validate(created)

    def update_profile(self, profile_id: int, data: ProfileUpdate) -> ProfileRead:
        profile = self.profile_repo.get_by_id(profile_id)
        if not profile:
            raise NotFoundError("Perfil", profile_id)

        update_data = data.model_dump(exclude_unset=True)
        if "slug" in update_data or "name" in update_data:
            new_slug = update_data.get("slug") or profile.slug
            if "name" in update_data and "slug" not in update_data:
                new_slug = slugify(update_data["name"])
            existing_slugs = [
                s for s in self.profile_repo.get_all_slugs() if s != profile.slug
            ]
            update_data["slug"] = ensure_unique_slug(slugify(new_slug), existing_slugs)

        for field, value in update_data.items():
            setattr(profile, field, value)

        updated = self.profile_repo.update(profile)
        return ProfileRead.model_validate(updated)

    def delete_profile(self, profile_id: int) -> None:
        profile = self.profile_repo.get_by_id(profile_id)
        if not profile:
            raise NotFoundError("Perfil", profile_id)
        self.profile_repo.delete(profile)
