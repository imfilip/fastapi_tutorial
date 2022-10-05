"""create post table

Revision ID: dbc5d0602bfe
Revises: 
Create Date: 2022-10-05 22:30:57.463860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbc5d0602bfe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable = False, primary_key = True),
        sa.Column("title", sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
