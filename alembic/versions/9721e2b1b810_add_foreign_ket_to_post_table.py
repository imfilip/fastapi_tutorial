"""Add foreign ket to post table

Revision ID: 9721e2b1b810
Revises: 7d4c5317da39
Create Date: 2022-10-08 11:16:19.476532

"""
from threading import local
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9721e2b1b810'
down_revision = '7d4c5317da39'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable = False))
    op.create_foreign_key("posts_users_fk", source_table = "posts", referent_table="users",
        local_cols = ["owner_id"], remote_cols = ["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="posts")
    op.drop_column("posts", "onwer_id")
    pass
