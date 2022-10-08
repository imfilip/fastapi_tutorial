"""add last few columns to posts table

Revision ID: 7ad2bf3c8e72
Revises: 9721e2b1b810
Create Date: 2022-10-08 11:26:29.322845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ad2bf3c8e72'
down_revision = '9721e2b1b810'
branch_labels = None
depends_on = None


def upgrade() -> None:
    "dummy func"
    pass


def downgrade() -> None:
    "dummy func"
    pass
