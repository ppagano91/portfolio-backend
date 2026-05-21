"""create profiles and experiences tables

Revision ID: 003
Revises: 002
Create Date: 2026-05-21

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("profiles", sa.Column("slug", sa.String(length=255), nullable=True))
    op.add_column("profiles", sa.Column("subtitle", sa.String(length=500), nullable=True))
    op.add_column("profiles", sa.Column("phone", sa.String(length=50), nullable=True))
    op.add_column("profiles", sa.Column("cv_url", sa.String(length=500), nullable=True))
    op.add_column(
        "profiles",
        sa.Column("focus_areas", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "profiles",
        sa.Column("key_skills", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "profiles",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "profiles",
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )

    op.execute(
        """
        UPDATE profiles
        SET
            slug = COALESCE(
                NULLIF(slug, ''),
                lower(regexp_replace(trim(name), '[^a-zA-Z0-9]+', '-', 'g')),
                'patricio-pagano'
            ),
            focus_areas = COALESCE(areas, '[]'::json),
            key_skills = COALESCE(key_skills, '[]'::json),
            summary = COALESCE(summary, ''),
            is_active = COALESCE(is_active, TRUE),
            sort_order = COALESCE(sort_order, 0)
        """
    )

    op.alter_column("profiles", "slug", nullable=False)
    op.alter_column("profiles", "summary", nullable=False)

    op.create_index("ix_profiles_slug", "profiles", ["slug"], unique=False)
    op.create_index("ix_profiles_is_active", "profiles", ["is_active"], unique=False)
    op.create_unique_constraint("uq_profiles_slug", "profiles", ["slug"])

    op.drop_column("profiles", "areas")
    op.drop_column("profiles", "about_focus")
    op.drop_column("profiles", "experience")
    op.drop_column("profiles", "education")

    op.create_table(
        "experiences",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("company", sa.String(length=255), nullable=False),
        sa.Column("position", sa.String(length=255), nullable=False),
        sa.Column("employment_type", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("responsibilities", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("technologies", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("company_url", sa.String(length=500), nullable=True),
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
        sa.ForeignKeyConstraint(["profile_id"], ["profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "profile_id",
            "company",
            "position",
            name="uq_experiences_profile_company_position",
        ),
    )
    op.create_index("ix_experiences_profile_id", "experiences", ["profile_id"], unique=False)
    op.create_index("ix_experiences_published", "experiences", ["published"], unique=False)
    op.create_index("ix_experiences_sort_order", "experiences", ["sort_order"], unique=False)
    op.create_index("ix_experiences_start_date", "experiences", ["start_date"], unique=False)


def downgrade() -> None:
    op.drop_table("experiences")

    op.add_column(
        "profiles",
        sa.Column("areas", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column("profiles", sa.Column("about_focus", sa.Text(), nullable=True))
    op.add_column(
        "profiles",
        sa.Column("experience", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "profiles",
        sa.Column("education", sa.JSON(), nullable=False, server_default="{}"),
    )

    op.execute(
        """
        UPDATE profiles
        SET areas = COALESCE(focus_areas, '[]'::json)
        """
    )

    op.drop_constraint("uq_profiles_slug", "profiles", type_="unique")
    op.drop_index("ix_profiles_is_active", table_name="profiles")
    op.drop_index("ix_profiles_slug", table_name="profiles")

    op.alter_column("profiles", "summary", nullable=True)

    op.drop_column("profiles", "sort_order")
    op.drop_column("profiles", "is_active")
    op.drop_column("profiles", "key_skills")
    op.drop_column("profiles", "focus_areas")
    op.drop_column("profiles", "cv_url")
    op.drop_column("profiles", "phone")
    op.drop_column("profiles", "subtitle")
    op.drop_column("profiles", "slug")
