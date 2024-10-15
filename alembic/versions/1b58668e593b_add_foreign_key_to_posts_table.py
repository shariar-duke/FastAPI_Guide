"""add foreign-key to posts table

Revision ID: 1b58668e593b
Revises: 88ebecfc620e
Create Date: 2024-10-15 11:15:32.446726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b58668e593b'
down_revision: Union[str, None] = '88ebecfc620e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the owner_id column to the posts table
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))

    # Create a foreign key from posts.owner_id to users.id
    op.create_foreign_key(
        'post_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols=['owner_id'],  # Fixed typo from 'ownder_id'
        remote_cols=['id'],
        ondelete='CASCADE'
    )


def downgrade():
    # Drop the foreign key
    op.drop_constraint('post_users_fk', table_name='posts', type_='foreignkey')

    # Drop the owner_id column
    op.drop_column('posts', 'owner_id')
