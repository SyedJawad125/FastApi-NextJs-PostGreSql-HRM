"""initial clean migration

Revision ID: 22ddf1dabfbc
Revises: 
Create Date: 2025-07-29 15:42:03.143325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22ddf1dabfbc'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### Drop dependent table first ###
    op.drop_table('employee_holidays')

    # ### Then drop index and parent table ###
    op.drop_index(op.f('ix_holiday_calendars_id'), table_name='holiday_calendars')
    op.drop_table('holiday_calendars')

    # ### Add new recruitment fields ###
    op.add_column('recruitments', sa.Column('requirements', sa.Text(), nullable=True))
    op.add_column('recruitments', sa.Column('responsibilities', sa.Text(), nullable=True))

    # Step 1: Add enum columns as nullable
    op.add_column('recruitments', sa.Column('job_type', sa.Enum('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERNSHIP', 'FREELANCE', name='jobtype'), nullable=True))
    op.add_column('recruitments', sa.Column('job_level', sa.Enum('ENTRY', 'JUNIOR', 'MID', 'SENIOR', 'LEAD', 'MANAGER', 'DIRECTOR', 'EXECUTIVE', name='joblevel'), nullable=True))
    op.add_column('recruitments', sa.Column('work_mode', sa.Enum('ONSITE', 'REMOTE', 'HYBRID', name='workmode'), nullable=True))
    op.add_column('recruitments', sa.Column('status', sa.Enum('DRAFT', 'ACTIVE', 'PAUSED', 'CLOSED', 'CANCELLED', name='jobstatus'), nullable=True))

    # Step 2: Set defaults for existing rows
    op.execute("UPDATE recruitments SET job_type = 'full_time'")
    op.execute("UPDATE recruitments SET job_level = 'mid'")
    op.execute("UPDATE recruitments SET work_mode = 'onsite'")
    op.execute("UPDATE recruitments SET status = 'draft'")

    # Step 3: Make columns NOT NULL
    op.alter_column('recruitments', 'job_type', nullable=False)
    op.alter_column('recruitments', 'job_level', nullable=False)
    op.alter_column('recruitments', 'work_mode', nullable=False)
    op.alter_column('recruitments', 'status', nullable=False)

    # Remaining fields
    op.add_column('recruitments', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('recruitments', sa.Column('city', sa.String(length=100), nullable=True))
    op.add_column('recruitments', sa.Column('country', sa.String(length=100), nullable=True))
    op.add_column('recruitments', sa.Column('salary_min', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('recruitments', sa.Column('salary_max', sa.Numeric(precision=10, scale=2), nullable=True))
    op.add_column('recruitments', sa.Column('currency', sa.String(length=3), nullable=True))
    op.add_column('recruitments', sa.Column('min_experience_years', sa.Integer(), nullable=True))
    op.add_column('recruitments', sa.Column('max_experience_years', sa.Integer(), nullable=True))
    op.add_column('recruitments', sa.Column('education_level', sa.String(length=100), nullable=True))
    op.add_column('recruitments', sa.Column('max_applicants', sa.Integer(), nullable=True))
    op.add_column('recruitments', sa.Column('auto_close_when_full', sa.Boolean(), nullable=True))
    op.add_column('recruitments', sa.Column('application_instructions', sa.Text(), nullable=True))
    op.add_column('recruitments', sa.Column('required_skills', sa.Text(), nullable=True))
    op.add_column('recruitments', sa.Column('preferred_skills', sa.Text(), nullable=True))
    op.add_column('recruitments', sa.Column('tags', sa.Text(), nullable=True))
    op.add_column('recruitments', sa.Column('last_activity_date', sa.Date(), nullable=True))
    op.add_column('recruitments', sa.Column('contact_email', sa.String(length=255), nullable=True))
    op.add_column('recruitments', sa.Column('contact_phone', sa.String(length=20), nullable=True))
    op.add_column('recruitments', sa.Column('is_urgent', sa.Boolean(), nullable=True))
    op.add_column('recruitments', sa.Column('is_featured', sa.Boolean(), nullable=True))
    op.add_column('recruitments', sa.Column('is_confidential', sa.Boolean(), nullable=True))
    op.add_column('recruitments', sa.Column('allow_remote_candidates', sa.Boolean(), nullable=True))
    op.add_column('recruitments', sa.Column('requires_visa_sponsorship', sa.Boolean(), nullable=True))
    op.add_column('recruitments', sa.Column('view_count', sa.Integer(), nullable=True))
    op.add_column('recruitments', sa.Column('application_count', sa.Integer(), nullable=True))
    op.add_column('recruitments', sa.Column('slug', sa.String(length=255), nullable=True))
    op.add_column('recruitments', sa.Column('meta_description', sa.String(length=160), nullable=True))
    op.add_column('recruitments', sa.Column('external_job_boards', sa.Text(), nullable=True))
    op.add_column('recruitments', sa.Column('published_at', sa.DateTime(), nullable=True))
    op.add_column('recruitments', sa.Column('closed_at', sa.DateTime(), nullable=True))
    op.add_column('recruitments', sa.Column('hiring_manager_id', sa.Integer(), nullable=True))

    op.alter_column('recruitments', 'description',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)

    op.create_index(op.f('ix_recruitments_created_at'), 'recruitments', ['created_at'], unique=False)
    op.create_index(op.f('ix_recruitments_deadline'), 'recruitments', ['deadline'], unique=False)
    op.create_index(op.f('ix_recruitments_job_title'), 'recruitments', ['job_title'], unique=False)
    op.create_index(op.f('ix_recruitments_posted_date'), 'recruitments', ['posted_date'], unique=False)
    op.create_index(op.f('ix_recruitments_slug'), 'recruitments', ['slug'], unique=True)

    op.create_index(op.f('ix_recruitments_status'), 'recruitments', ['status'], unique=False)

    op.create_foreign_key(None, 'recruitments', 'employees', ['hiring_manager_id'], ['id'], ondelete='SET NULL')



def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'recruitments', type_='foreignkey')
    op.drop_index(op.f('ix_recruitments_status'), table_name='recruitments')
    op.drop_index(op.f('ix_recruitments_slug'), table_name='recruitments')
    op.drop_index(op.f('ix_recruitments_posted_date'), table_name='recruitments')
    op.drop_index(op.f('ix_recruitments_job_title'), table_name='recruitments')
    op.drop_index(op.f('ix_recruitments_deadline'), table_name='recruitments')
    op.drop_index(op.f('ix_recruitments_created_at'), table_name='recruitments')
    op.alter_column('recruitments', 'description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
    op.drop_column('recruitments', 'hiring_manager_id')
    op.drop_column('recruitments', 'closed_at')
    op.drop_column('recruitments', 'published_at')
    op.drop_column('recruitments', 'external_job_boards')
    op.drop_column('recruitments', 'meta_description')
    op.drop_column('recruitments', 'slug')
    op.drop_column('recruitments', 'application_count')
    op.drop_column('recruitments', 'view_count')
    op.drop_column('recruitments', 'requires_visa_sponsorship')
    op.drop_column('recruitments', 'allow_remote_candidates')
    op.drop_column('recruitments', 'is_confidential')
    op.drop_column('recruitments', 'is_featured')
    op.drop_column('recruitments', 'is_urgent')
    op.drop_column('recruitments', 'contact_phone')
    op.drop_column('recruitments', 'contact_email')
    op.drop_column('recruitments', 'last_activity_date')
    op.drop_column('recruitments', 'tags')
    op.drop_column('recruitments', 'preferred_skills')
    op.drop_column('recruitments', 'required_skills')
    op.drop_column('recruitments', 'application_instructions')
    op.drop_column('recruitments', 'auto_close_when_full')
    op.drop_column('recruitments', 'max_applicants')
    op.drop_column('recruitments', 'education_level')
    op.drop_column('recruitments', 'max_experience_years')
    op.drop_column('recruitments', 'min_experience_years')
    op.drop_column('recruitments', 'currency')
    op.drop_column('recruitments', 'salary_max')
    op.drop_column('recruitments', 'salary_min')
    op.drop_column('recruitments', 'country')
    op.drop_column('recruitments', 'city')
    op.drop_column('recruitments', 'location')
    op.drop_column('recruitments', 'status')
    op.drop_column('recruitments', 'work_mode')
    op.drop_column('recruitments', 'job_level')
    op.drop_column('recruitments', 'job_type')
    op.drop_column('recruitments', 'responsibilities')
    op.drop_column('recruitments', 'requirements')
    op.create_table('employee_holidays',
    sa.Column('holiday_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('employee_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'], name=op.f('employee_holidays_employee_id_fkey')),
    sa.ForeignKeyConstraint(['holiday_id'], ['holiday_calendars.id'], name=op.f('employee_holidays_holiday_id_fkey'))
    )
    op.create_table('holiday_calendars',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('is_optional', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('is_national', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('department_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_by_user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('updated_by_user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', sa.DATE(), server_default=sa.text('CURRENT_DATE'), autoincrement=False, nullable=True),
    sa.Column('updated_at', sa.DATE(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['created_by_user_id'], ['users.id'], name=op.f('holiday_calendars_created_by_user_id_fkey')),
    sa.ForeignKeyConstraint(['department_id'], ['departments.id'], name=op.f('holiday_calendars_department_id_fkey')),
    sa.ForeignKeyConstraint(['updated_by_user_id'], ['users.id'], name=op.f('holiday_calendars_updated_by_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('holiday_calendars_pkey'))
    )
    op.create_index(op.f('ix_holiday_calendars_id'), 'holiday_calendars', ['id'], unique=False)
    # ### end Alembic commands ###
