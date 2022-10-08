"""add user table

Revision ID: 7d4c5317da39
Revises: a8aa86a325a5
Create Date: 2022-10-08 11:09:06.234606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d4c5317da39'
down_revision = 'a8aa86a325a5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", 
                    sa.Column("id", sa.Integer(), nullable = False),
                    sa.Column("email", sa.String(), nullable = False),
                    sa.Column("password", sa.String(), nullable = False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable = False,
                                            server_default = sa.text("now()")),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")
                    )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
