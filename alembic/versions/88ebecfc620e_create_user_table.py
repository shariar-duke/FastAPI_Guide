"""create user table

Revision ID: 88ebecfc620e
Revises: 49f13509cc11
Create Date: 2024-10-15 10:52:27.472672

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '88ebecfc620e'
down_revision: Union[str, None] = '49f13509cc11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
