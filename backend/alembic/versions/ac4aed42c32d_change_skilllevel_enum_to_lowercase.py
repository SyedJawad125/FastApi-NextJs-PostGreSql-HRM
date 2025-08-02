"""Change skilllevel enum to lowercase

Revision ID: ac4aed42c32d
Revises: a75baa62e6a1
Create Date: 2025-08-02 15:09:58.264393
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac4aed42c32d'
down_revision: Union[str, Sequence[str], None] = 'a75baa62e6a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# New lowercase enum type
new_skilllevel = sa.Enum('beginner', 'intermediate', 'advanced', 'expert', name='skilllevel')


def upgrade() -> None:
    # Step 1: Rename the old enum
    op.execute("ALTER TYPE skilllevel RENAME TO skilllevel_old")

    # Step 2: Create new lowercase enum
    new_skilllevel.create(op.get_bind())

    # Step 3: Alter the column to use the new enum
    op.execute("""
        ALTER TABLE employee_skills
        ALTER COLUMN proficiency_level
        TYPE skilllevel
        USING LOWER(proficiency_level::text)::skilllevel
    """)

    # Step 4: Drop the old enum
    op.execute("DROP TYPE skilllevel_old")


def downgrade() -> None:
    # Recreate the old uppercase enum
    old_skilllevel = sa.Enum('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT', name='skilllevel')
    old_skilllevel.create(op.get_bind())

    # Convert the column back to uppercase values
    op.execute("""
        ALTER TABLE employee_skills
        ALTER COLUMN proficiency_level
        TYPE skilllevel
        USING UPPER(proficiency_level::text)::skilllevel
    """)

    # Drop the lowercase enum
    op.execute("DROP TYPE skilllevel")
