"""lowercase project_status_enum values

Revision ID: 006
Revises: 005
Create Date: 2026-05-23

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LOWERCASE_VALUES = ("draft", "published", "archived")
UPPERCASE_VALUES = tuple(value.upper() for value in LOWERCASE_VALUES)


def _has_native_pg_enum(connection: sa.Connection) -> bool:
    result = connection.execute(
        sa.text(
            """
            SELECT EXISTS (
                SELECT 1
                FROM pg_type t
                JOIN pg_namespace n ON n.oid = t.typnamespace
                WHERE t.typname = 'project_status_enum'
                  AND t.typtype = 'e'
            )
            """
        )
    )
    return bool(result.scalar())


def _migrate_native_pg_enum_to_lowercase(connection: sa.Connection) -> None:
    values_sql = ", ".join(f"'{value}'" for value in LOWERCASE_VALUES)
    connection.execute(
        sa.text(f"CREATE TYPE project_status_enum_new AS ENUM ({values_sql})")
    )
    connection.execute(
        sa.text(
            """
            ALTER TABLE projects
            ALTER COLUMN status TYPE project_status_enum_new
            USING lower(status::text)::project_status_enum_new
            """
        )
    )
    connection.execute(sa.text("DROP TYPE project_status_enum"))
    connection.execute(
        sa.text("ALTER TYPE project_status_enum_new RENAME TO project_status_enum")
    )


def _migrate_native_pg_enum_to_uppercase(connection: sa.Connection) -> None:
    values_sql = ", ".join(f"'{value}'" for value in UPPERCASE_VALUES)
    connection.execute(
        sa.text(f"CREATE TYPE project_status_enum_old AS ENUM ({values_sql})")
    )
    connection.execute(
        sa.text(
            """
            ALTER TABLE projects
            ALTER COLUMN status TYPE project_status_enum_old
            USING upper(status::text)::project_status_enum_old
            """
        )
    )
    connection.execute(sa.text("DROP TYPE project_status_enum"))
    connection.execute(
        sa.text("ALTER TYPE project_status_enum_old RENAME TO project_status_enum")
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
            SET status = lower(status)
            WHERE status IS NOT NULL
              AND status <> lower(status)
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
            SET status = upper(status)
            WHERE status IS NOT NULL
              AND status <> upper(status)
            """
        )
    )
