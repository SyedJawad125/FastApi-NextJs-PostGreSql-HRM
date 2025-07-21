"""merge branches

Revision ID: 84f04f0acc3e
Revises: 86c7152ab54a, f8d27b634de5
Create Date: 2025-07-21 16:11:56.926814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84f04f0acc3e'
down_revision: Union[str, Sequence[str], None] = ('86c7152ab54a', 'f8d27b634de5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
