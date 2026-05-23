"""lowercase project_type_enum values

Revision ID: 005
Revises: 004
Create Date: 2026-05-23

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LOWERCASE_VALUES = (
    "web",
    "gis",
    "data",
    "dashboard",
    "notebook",
    "api",
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
                WHERE t.typname = 'project_type_enum'
                  AND t.typtype = 'e'
            )
            """
        )
    )
    return bool(result.scalar())


def _migrate_native_pg_enum_to_lowercase(connection: sa.Connection) -> None:
    values_sql = ", ".join(f"'{value}'" for value in LOWERCASE_VALUES)
    connection.execute(
        sa.text(f"CREATE TYPE project_type_enum_new AS ENUM ({values_sql})")
    )
    connection.execute(
        sa.text(
            """
            ALTER TABLE projects
            ALTER COLUMN project_type TYPE project_type_enum_new
            USING lower(project_type::text)::project_type_enum_new
            """
        )
    )
    connection.execute(sa.text("DROP TYPE project_type_enum"))
    connection.execute(
        sa.text("ALTER TYPE project_type_enum_new RENAME TO project_type_enum")
    )


def _migrate_native_pg_enum_to_uppercase(connection: sa.Connection) -> None:
    values_sql = ", ".join(f"'{value}'" for value in UPPERCASE_VALUES)
    connection.execute(
        sa.text(f"CREATE TYPE project_type_enum_old AS ENUM ({values_sql})")
    )
    connection.execute(
        sa.text(
            """
            ALTER TABLE projects
            ALTER COLUMN project_type TYPE project_type_enum_old
            USING upper(project_type::text)::project_type_enum_old
            """
        )
    )
    connection.execute(sa.text("DROP TYPE project_type_enum"))
    connection.execute(
        sa.text("ALTER TYPE project_type_enum_old RENAME TO project_type_enum")
    )


def upgrade() -> None:
    connection = op.get_bind()

    if _has_native_pg_enum(connection):
        _migrate_native_pg_enum_to_lowercase(connection)
        return

    connection.execute(
        sa.text(
            """
            UPDATE projects
            SET project_type = lower(project_type)
            WHERE project_type IS NOT NULL
              AND project_type <> lower(project_type)
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
            UPDATE projects
            SET project_type = upper(project_type)
            WHERE project_type IS NOT NULL
              AND project_type <> upper(project_type)
            """
        )
    )
