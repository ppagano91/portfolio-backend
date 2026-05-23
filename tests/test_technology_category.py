import pytest
from pydantic import ValidationError

from app.models.technology import TechnologyCategory
from app.schemas.technology import TechnologyCreate, TechnologyRead


class TestTechnologyCategoryEnum:
    def test_enum_values_are_lowercase(self) -> None:
        for member in TechnologyCategory:
            assert member.value == member.value.lower()
            assert member.name == member.name.upper()

    def test_all_expected_members_exist(self) -> None:
        expected = {
            "BACKEND",
            "FRONTEND",
            "DATABASE",
            "GIS",
            "DATA",
            "DEVOPS",
            "OTHER",
        }
        assert {member.name for member in TechnologyCategory} == expected


class TestTechnologyCategorySchema:
    def test_accepts_lowercase_category(self) -> None:
        payload = TechnologyCreate(name="Rust", category="backend")
        assert payload.category == TechnologyCategory.BACKEND
        assert payload.category.value == "backend"

    def test_accepts_uppercase_category_and_normalizes(self) -> None:
        payload = TechnologyCreate(name="Rust", category="BACKEND")
        assert payload.category == TechnologyCategory.BACKEND
        assert payload.category.value == "backend"

    def test_accepts_mixed_case_category(self) -> None:
        payload = TechnologyCreate(name="Vue", category="FrontEnd")
        assert payload.category == TechnologyCategory.FRONTEND
        assert payload.category.value == "frontend"

    def test_rejects_invalid_category(self) -> None:
        with pytest.raises(ValidationError):
            TechnologyCreate(name="Invalid", category="mobile")

    def test_read_schema_serializes_lowercase_value(self) -> None:
        read = TechnologyRead(
            id=1,
            name="Python",
            category=TechnologyCategory.BACKEND,
            icon_url=None,
        )
        dumped = read.model_dump()
        assert dumped["category"] == "backend"

    def test_read_schema_accepts_lowercase_string(self) -> None:
        read = TechnologyRead.model_validate(
            {
                "id": 1,
                "name": "Python",
                "category": "backend",
                "icon_url": None,
            }
        )
        assert read.category == TechnologyCategory.BACKEND


class TestTechnologyCategorySqlAlchemyBinding:
    def test_enum_uses_values_not_names(self) -> None:
        from app.models.technology import Technology, _technology_category_values

        column = Technology.__table__.c.category
        assert _technology_category_values(TechnologyCategory) == [
            member.value for member in TechnologyCategory
        ]
        assert column.type.enums == [member.value for member in TechnologyCategory]
