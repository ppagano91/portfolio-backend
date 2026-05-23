"""lowercase technology_category_enum values

Revision ID: 004
Revises: 003
Create Date: 2026-05-23

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LOWERCASE_VALUES = (
    "backend",
    "frontend",
    "database",
    "gis",
    "data",
    "devops",
    "other",
)

UPPERCASE_VALUES = tuple(value.upper() for value in LOWERCASE_VALUES)


def _has_native_pg_enum(connection: sa.Connection) -> bool:
    result = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_namespace n ON n.oid = t.typnamespace
                WHERE t.typname = 'technology_category_enum'
                  AND t.typtype = 'e'
            )
            """
        )
    )
    return bool(result.scalar())


def _migrate_native_pg_enum_to_lowercase(connection: sa.Connection) -> None:
    values_sql = ", ".join(f"'{value}'" for value in LOWERCASE_VALUES)
    connection.execute(
        sa.text(f"CREATE TYPE technology_category_enum_new AS ENUM ({values_sql})")
    )
    connection.execute(
        sa.text(
            """
            ALTER TABLE technologies
            ALTER COLUMN category TYPE technology_category_enum_new
            USING lower(category::text)::technology_category_enum_new
            """
        )
    )
    connection.execute(sa.text("DROP TYPE technology_category_enum"))
    connection.execute(
        sa.text("ALTER TYPE technology_category_enum_new RENAME TO technology_category_enum")
    )


def _migrate_native_pg_enum_to_uppercase(connection: sa.Connection) -> None:
    values_sql = ", ".join(f"'{value}'" for value in UPPERCASE_VALUES)
    connection.execute(
        sa.text(f"CREATE TYPE technology_category_enum_old AS ENUM ({values_sql})")
    )
    connection.execute(
        sa.text(
            """
            ALTER TABLE technologies
            ALTER COLUMN category TYPE technology_category_enum_old
            USING upper(category::text)::technology_category_enum_old
            """
        )
    )
    connection.execute(sa.text("DROP TYPE technology_category_enum"))
    connection.execute(
        sa.text("ALTER TYPE technology_category_enum_old RENAME TO technology_category_enum")
    )


def upgrade() -> None:
    connection = op.get_bind()

    if _has_native_pg_enum(connection):
        _migrate_native_pg_enum_to_lowercase(connection)
        return

    connection.execute(
        sa.text(
            """
            UPDATE technologies
            SET category = lower(category)
            WHERE category IS NOT NULL
              AND category <> lower(category)
            """
        )
    )


def downgrade() -> None:
    connection = op.get_bind()

    if _has_native_pg_enum(connection):
        _migrate_native_pg_enum_to_uppercase(connection)
        return

    connection.execute(
        sa.text(
            """
            UPDATE technologies
            SET category = upper(category)
            WHERE category IS NOT NULL
              AND category <> upper(category)
            """
        )
    )
