"""add content column in post table

Revision ID: 49f13509cc11
Revises: 051780862e0c
Create Date: 2024-10-15 09:53:59.663921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49f13509cc11'
down_revision: Union[str, None] = '051780862e0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
