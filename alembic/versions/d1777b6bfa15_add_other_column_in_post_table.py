"""add other columns in post table  

Revision ID: d1777b6bfa15
Revises: 1b58668e593b
Create Date: 2024-10-15 11:40:19.296947

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd1777b6bfa15'
down_revision: Union[str, None] = '1b58668e593b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add new columns to the posts table
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(),
                  nullable=False, server_default=sa.text('TRUE'))  # Use sa.text('TRUE') for default
    )
    op.add_column(
        'posts',
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text('now()'),
            nullable=False
        )
    )


def downgrade():
    # Drop the added columns in case of downgrade
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
