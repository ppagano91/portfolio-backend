"""create education table

Revision ID: 007
Revises: 006
Create Date: 2026-05-23

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("institution", sa.String(length=255), nullable=False),
        sa.Column("degree", sa.String(length=255), nullable=False),
        sa.Column("field_of_study", sa.String(length=255), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("institution_url", sa.String(length=500), nullable=True),
        sa.Column(
            "education_type",
            sa.Enum(
                "formal",
                "course",
                name="education_type_enum",
                native_enum=False,
            ),
            nullable=False,
            server_default="formal",
        ),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_education_start_date", "education", ["start_date"], unique=False)
    op.create_index("ix_education_education_type", "education", ["education_type"], unique=False)
    op.create_index("ix_education_sort_order", "education", ["sort_order"], unique=False)
    op.create_index("ix_education_published", "education", ["published"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_education_published", table_name="education")
    op.drop_index("ix_education_sort_order", table_name="education")
    op.drop_index("ix_education_education_type", table_name="education")
    op.drop_index("ix_education_start_date", table_name="education")
    op.drop_table("education")
    op.execute("DROP TYPE IF EXISTS education_type_enum")
