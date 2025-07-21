"""create_employee_profiles_table

Revision ID: f8d27b634de5
Revises: 552c88c32bed
Create Date: 2024-03-19 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8d27b634de5'
down_revision = '552c88c32bed'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'employee_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(), nullable=False),
        sa.Column('marital_status', sa.String(), nullable=True),
        sa.Column('blood_group', sa.String(), nullable=True),
        sa.Column('nationality', sa.String(), nullable=False),
        sa.Column('emergency_contact_name', sa.String(length=100), nullable=False),
        sa.Column('emergency_contact_relationship', sa.String(length=50), nullable=False),
        sa.Column('emergency_contact_phone', sa.String(length=20), nullable=False),
        sa.Column('current_address', sa.String(length=200), nullable=False),
        sa.Column('permanent_address', sa.String(length=200), nullable=True),
        sa.Column('national_id', sa.String(length=50), nullable=False),
        sa.Column('passport_number', sa.String(length=50), nullable=True),
        sa.Column('tax_id', sa.String(length=50), nullable=True),
        sa.Column('education_level', sa.String(length=100), nullable=True),
        sa.Column('field_of_study', sa.String(length=100), nullable=True),
        sa.Column('skills', sa.String(length=500), nullable=True),
        sa.Column('employee_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('employee_id'),
        sa.UniqueConstraint('national_id'),
        sa.UniqueConstraint('passport_number'),
        sa.UniqueConstraint('tax_id')
    )
    op.create_index(op.f('ix_employee_profiles_id'), 'employee_profiles', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_employee_profiles_id'), table_name='employee_profiles')
    op.drop_table('employee_profiles')
