"""add employee loan table with enums

Revision ID: d865d372faa3
Revises: 7d2d34ecc033
Create Date: 2025-08-03 15:02:51.598999

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd865d372faa3'
down_revision: Union[str, Sequence[str], None] = '7d2d34ecc033'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # Create the enum types first (if they don't exist)
    connection = op.get_bind()
    
    # Check if loantype enum exists
    result = connection.execute(sa.text(
        "SELECT 1 FROM pg_type WHERE typname = 'loantype'"
    )).fetchone()
    
    if not result:
        loan_type_enum = postgresql.ENUM(
            'PERSONAL', 'EDUCATIONAL', 'MEDICAL', 'EMERGENCY', 'ADVANCE', 'OTHER', 
            name='loantype'
        )
        loan_type_enum.create(connection)
    
    # Check if loanstatus enum exists
    result = connection.execute(sa.text(
        "SELECT 1 FROM pg_type WHERE typname = 'loanstatus'"
    )).fetchone()
    
    if not result:
        loan_status_enum = postgresql.ENUM(
            'PENDING', 'APPROVED', 'REJECTED', 
            name='loanstatus'
        )
        loan_status_enum.create(connection)
    
    # Add new columns
    op.add_column('employee_loans', sa.Column('request_user_id', sa.Integer(), nullable=True))
    op.add_column('employee_loans', sa.Column('date_requested', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    
    # First, update existing data to match enum values
    connection.execute(sa.text("""
        UPDATE employee_loans 
        SET loan_type = CASE 
            WHEN LOWER(loan_type) LIKE '%personal%' THEN 'PERSONAL'
            WHEN LOWER(loan_type) LIKE '%education%' THEN 'EDUCATIONAL'
            WHEN LOWER(loan_type) LIKE '%medical%' THEN 'MEDICAL'
            WHEN LOWER(loan_type) LIKE '%emergency%' THEN 'EMERGENCY'
            WHEN LOWER(loan_type) LIKE '%advance%' THEN 'ADVANCE'
            ELSE 'OTHER'
        END
    """))
    
    # Update status values to match enum
    connection.execute(sa.text("""
        UPDATE employee_loans 
        SET status = CASE 
            WHEN LOWER(status) LIKE '%pending%' THEN 'PENDING'
            WHEN LOWER(status) LIKE '%approved%' THEN 'APPROVED'
            WHEN LOWER(status) LIKE '%reject%' THEN 'REJECTED'
            ELSE 'PENDING'
        END
    """))
    
    # Now alter columns to use enum types
    op.alter_column('employee_loans', 'loan_type',
               existing_type=sa.VARCHAR(length=100),
               type_=postgresql.ENUM('PERSONAL', 'EDUCATIONAL', 'MEDICAL', 'EMERGENCY', 'ADVANCE', 'OTHER', name='loantype'),
               existing_nullable=False,
               postgresql_using='loan_type::loantype')
    
    op.alter_column('employee_loans', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    
    op.alter_column('employee_loans', 'status',
               existing_type=sa.VARCHAR(length=50),
               type_=postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='loanstatus'),
               nullable=False,
               postgresql_using='status::loanstatus')
    
    # Add foreign key constraint
    op.create_foreign_key('fk_employee_loans_request_user', 'employee_loans', 'users', ['request_user_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    
    # Drop foreign key constraint
    op.drop_constraint('fk_employee_loans_request_user', 'employee_loans', type_='foreignkey')
    
    # Revert columns back to original types
    op.alter_column('employee_loans', 'status',
               existing_type=postgresql.ENUM('PENDING', 'APPROVED', 'REJECTED', name='loanstatus'),
               type_=sa.VARCHAR(length=50),
               nullable=False)
    
    op.alter_column('employee_loans', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    
    op.alter_column('employee_loans', 'loan_type',
               existing_type=postgresql.ENUM('PERSONAL', 'EDUCATIONAL', 'MEDICAL', 'EMERGENCY', 'ADVANCE', 'OTHER', name='loantype'),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
    
    # Drop new columns
    op.drop_column('employee_loans', 'date_requested')
    op.drop_column('employee_loans', 'request_user_id')
    
    # Note: We don't drop the enum types here in case other tables might use them
    # If you want to drop them, uncomment the lines below:
    # postgresql.ENUM(name='loantype').drop(op.get_bind())
    # postgresql.ENUM(name='loanstatus').drop(op.get_bind())