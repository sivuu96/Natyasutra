"""Initial content tables: dim_language and cnt_item (subset of the content model).

Source: studio/docs/content-model.md, sections 3.1 and 4.1.
The usr_accounts foreign keys are added when the auth tables exist.

Revision ID: 0001
Revises:
Create Date: 2026-11-27
"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "dim_language",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(10), nullable=False, comment="BCP 47, for example en, ml, hi"),
        sa.Column("label", sa.String(120), nullable=False),
        sa.Column("sort_order", sa.SmallInteger(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("legacy_table", sa.String(40), nullable=True),
        sa.Column("legacy_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_language_code"),
        mysql_charset="utf8mb4",
    )

    op.create_table(
        "cnt_item",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column(
            "kind",
            sa.Enum("collection", "media", "article", "product", name="cnt_item_kind"),
            nullable=False,
        ),
        sa.Column("slug", sa.String(190), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("short_description", sa.String(500), nullable=True),
        sa.Column(
            "status",
            sa.Enum("draft", "review", "published", "archived", name="cnt_item_status"),
            nullable=False,
            server_default="draft",
        ),
        sa.Column(
            "visibility",
            sa.Enum("public", "members", "hidden", name="cnt_item_visibility"),
            nullable=False,
            server_default="public",
        ),
        sa.Column("language_id", sa.SmallInteger(), nullable=True),
        sa.Column("published_from", sa.DateTime(), nullable=True),
        sa.Column("published_to", sa.DateTime(), nullable=True),
        sa.Column("meta_title", sa.String(255), nullable=True),
        sa.Column("meta_description", sa.String(500), nullable=True),
        sa.Column("legacy_table", sa.String(40), nullable=True),
        sa.Column("legacy_id", sa.BigInteger(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("created_by", sa.BigInteger(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column("updated_by", sa.BigInteger(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("kind", "slug", name="uq_item_kind_slug"),
        sa.ForeignKeyConstraint(["language_id"], ["dim_language.id"], name="fk_item_language"),
        mysql_charset="utf8mb4",
    )
    op.create_index("ix_item_status", "cnt_item", ["status", "visibility", "published_from"])
    op.create_index("ix_item_legacy", "cnt_item", ["legacy_table", "legacy_id"])


def downgrade() -> None:
    op.drop_index("ix_item_legacy", table_name="cnt_item")
    op.drop_index("ix_item_status", table_name="cnt_item")
    op.drop_table("cnt_item")
    op.drop_table("dim_language")
