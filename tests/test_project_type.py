import pytest
from pydantic import ValidationError

from app.models.project import Project, ProjectType, _project_type_values
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate


class TestProjectTypeEnum:
    def test_enum_values_are_lowercase(self) -> None:
        for member in ProjectType:
            assert member.value == member.value.lower()
            assert member.name == member.name.upper()

    def test_all_expected_members_exist(self) -> None:
        expected = {
            "WEB",
            "GIS",
            "DATA",
            "DASHBOARD",
            "NOTEBOOK",
            "API",
            "OTHER",
        }
        assert {member.name for member in ProjectType} == expected

    def test_api_member_value(self) -> None:
        assert ProjectType.API.value == "api"


class TestProjectTypeSchema:
    def test_accepts_lowercase_project_type(self) -> None:
        payload = ProjectCreate(title="Test API", project_type="api")
        assert payload.project_type == ProjectType.API
        assert payload.project_type.value == "api"

    def test_accepts_uppercase_project_type_and_normalizes(self) -> None:
        payload = ProjectCreate(title="Test API", project_type="API")
        assert payload.project_type == ProjectType.API
        assert payload.project_type.value == "api"

    def test_accepts_mixed_case_project_type(self) -> None:
        payload = ProjectCreate(title="GIS App", project_type="GiS")
        assert payload.project_type == ProjectType.GIS
        assert payload.project_type.value == "gis"

    def test_update_accepts_uppercase_project_type(self) -> None:
        payload = ProjectUpdate(project_type="WEB")
        assert payload.project_type == ProjectType.WEB
        assert payload.project_type.value == "web"

    def test_rejects_invalid_project_type(self) -> None:
        with pytest.raises(ValidationError):
            ProjectCreate(title="Invalid", project_type="mobile")

    def test_read_schema_serializes_lowercase_value(self) -> None:
        read = ProjectRead(
            id=1,
            title="API",
            slug="api",
            summary=None,
            description=None,
            project_type=ProjectType.API,
            status="draft",
            cover_image_url=None,
            repository_url=None,
            demo_url=None,
            documentation_url=None,
            featured=False,
            published=False,
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
        )
        dumped = read.model_dump()
        assert dumped["project_type"] == "api"


class TestProjectTypeSqlAlchemyBinding:
    def test_enum_uses_values_not_names(self) -> None:
        column = Project.__table__.c.project_type
        assert _project_type_values(ProjectType) == [member.value for member in ProjectType]
        assert column.type.enums == [member.value for member in ProjectType]
