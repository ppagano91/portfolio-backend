import pytest
from pydantic import ValidationError

from app.models.project import Project, ProjectStatus, _project_status_values
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate


class TestProjectStatusEnum:
    def test_enum_values_are_lowercase(self) -> None:
        for member in ProjectStatus:
            assert member.value == member.value.lower()
            assert member.name == member.name.upper()

    def test_all_expected_members_exist(self) -> None:
        expected = {"DRAFT", "PUBLISHED", "ARCHIVED"}
        assert {member.name for member in ProjectStatus} == expected


class TestProjectStatusSchema:
    def test_accepts_lowercase_status(self) -> None:
        payload = ProjectCreate(title="Test", status="published")
        assert payload.status == ProjectStatus.PUBLISHED
        assert payload.status.value == "published"

    def test_accepts_uppercase_status_and_normalizes(self) -> None:
        payload = ProjectCreate(title="Test", status="PUBLISHED")
        assert payload.status == ProjectStatus.PUBLISHED
        assert payload.status.value == "published"

    def test_update_accepts_uppercase_status(self) -> None:
        payload = ProjectUpdate(status="ARCHIVED")
        assert payload.status == ProjectStatus.ARCHIVED
        assert payload.status.value == "archived"

    def test_rejects_invalid_status(self) -> None:
        with pytest.raises(ValidationError):
            ProjectCreate(title="Test", status="pending")

    def test_read_schema_serializes_lowercase_value(self) -> None:
        read = ProjectRead(
            id=1,
            title="Test",
            slug="test",
            summary=None,
            description=None,
            project_type="web",
            status=ProjectStatus.PUBLISHED,
            cover_image_url=None,
            repository_url=None,
            demo_url=None,
            documentation_url=None,
            featured=False,
            published=True,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
        )
        dumped = read.model_dump()
        assert dumped["status"] == "published"


class TestProjectStatusSqlAlchemyBinding:
    def test_enum_uses_values_not_names(self) -> None:
        column = Project.__table__.c.status
        assert _project_status_values(ProjectStatus) == [
            member.value for member in ProjectStatus
        ]
        assert column.type.enums == [member.value for member in ProjectStatus]
