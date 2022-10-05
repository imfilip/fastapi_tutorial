"""Create whole posts table

Revision ID: a8aa86a325a5
Revises: d95da2e03ad2
Create Date: 2022-10-05 23:18:05.760623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8aa86a325a5'
down_revision = 'd95da2e03ad2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable = False, server_default="TRUE"))
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")))
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
