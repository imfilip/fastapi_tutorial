"""Add votes table

Revision ID: e24380d1d373
Revises: 7ad2bf3c8e72
Create Date: 2022-10-08 11:27:44.178042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e24380d1d373'
down_revision = '7ad2bf3c8e72'
branch_labels = None
depends_on = None


def upgrade() -> None:
    "dummy func"
    pass


def downgrade() -> None:
    "dummy func"
    pass
