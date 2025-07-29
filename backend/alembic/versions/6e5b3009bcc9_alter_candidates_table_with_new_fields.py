"""Alter candidates table with new fields

Revision ID: 6e5b3009bcc9
Revises: 96c28a94f61a
Create Date: 2025-07-29 10:09:54.222255
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6e5b3009bcc9'
down_revision: Union[str, Sequence[str], None] = '96c28a94f61a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('candidates', sa.Column('address', sa.Text(), nullable=True))
    op.add_column('candidates', sa.Column('resume_url', sa.String(length=500), nullable=True))
    op.add_column('candidates', sa.Column('portfolio_url', sa.String(length=500), nullable=True))
    op.add_column('candidates', sa.Column('linkedin_url', sa.String(length=500), nullable=True))
    op.add_column('candidates', sa.Column('skills', sa.Text(), nullable=True))
    op.add_column('candidates', sa.Column('experience_years', sa.Integer(), nullable=True))
    op.add_column('candidates', sa.Column('education', sa.Text(), nullable=True))
    op.add_column('candidates', sa.Column('is_available', sa.Boolean(), nullable=True))
    op.add_column('candidates', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_candidates_user_id_users', 'candidates', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    op.drop_constraint('fk_candidates_user_id_users', 'candidates', type_='foreignkey')
    op.drop_column('candidates', 'user_id')
    op.drop_column('candidates', 'is_available')
    op.drop_column('candidates', 'education')
    op.drop_column('candidates', 'experience_years')
    op.drop_column('candidates', 'skills')
    op.drop_column('candidates', 'linkedin_url')
    op.drop_column('candidates', 'portfolio_url')
    op.drop_column('candidates', 'resume_url')
    op.drop_column('candidates', 'address')
