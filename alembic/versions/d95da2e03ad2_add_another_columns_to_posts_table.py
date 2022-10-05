"""Add another columns to posts table

Revision ID: d95da2e03ad2
Revises: dbc5d0602bfe
Create Date: 2022-10-05 23:04:31.976364

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd95da2e03ad2'
down_revision = 'dbc5d0602bfe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable = False, server_default=sa.text("'empty'")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
