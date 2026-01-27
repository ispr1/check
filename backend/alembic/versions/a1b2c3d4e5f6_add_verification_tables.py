"""Add verification and verification_steps tables

Revision ID: a1b2c3d4e5f6
Revises: 63bc3783ba03
Create Date: 2026-01-27 13:50:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '63bc3783ba03'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop existing types if they exist (from failed previous runs)
    op.execute('DROP TYPE IF EXISTS verificationstatus CASCADE')
    op.execute('DROP TYPE IF EXISTS steptype CASCADE')
    op.execute('DROP TYPE IF EXISTS stepstatus CASCADE')
    
    # Drop tables if they exist (from failed previous runs)
    op.execute('DROP TABLE IF EXISTS verification_steps CASCADE')
    op.execute('DROP TABLE IF EXISTS verifications CASCADE')
    
    # Create verifications table (ENUM types are created automatically by SQLAlchemy)
    op.create_table(
        'verifications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('candidate_id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(length=100), nullable=False),
        sa.Column('token_expires_at', sa.DateTime(), nullable=False),
        sa.Column('status', sa.Enum('CREATED', 'LINK_SENT', 'IN_PROGRESS', 'SUBMITTED', 'SCORED', name='verificationstatus'), nullable=False),
        sa.Column('trust_score', sa.Integer(), nullable=True),
        sa.Column('trust_score_details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('submitted_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('candidate_id'),
        sa.UniqueConstraint('token')
    )
    op.create_index('ix_verifications_id', 'verifications', ['id'], unique=False)
    op.create_index('ix_verifications_candidate_id', 'verifications', ['candidate_id'], unique=False)
    op.create_index('ix_verifications_company_id', 'verifications', ['company_id'], unique=False)
    op.create_index('ix_verifications_token', 'verifications', ['token'], unique=False)
    op.create_index('ix_verifications_status', 'verifications', ['status'], unique=False)
    op.create_index('ix_verifications_company_status', 'verifications', ['company_id', 'status'], unique=False)
    
    # Create verification_steps table
    op.create_table(
        'verification_steps',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('verification_id', sa.Integer(), nullable=False),
        sa.Column('step_type', sa.Enum('PERSONAL_INFO', 'FACE_LIVENESS', 'AADHAAR', 'PAN', 'UAN', 'EDUCATION', 'EXPERIENCE', name='steptype'), nullable=False),
        sa.Column('is_mandatory', sa.Boolean(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', 'SKIPPED', name='stepstatus'), nullable=False),
        sa.Column('input_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('raw_response', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('score_contribution', sa.Integer(), nullable=True),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['verification_id'], ['verifications.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_verification_steps_id', 'verification_steps', ['id'], unique=False)
    op.create_index('ix_verification_steps_verification_id', 'verification_steps', ['verification_id'], unique=False)
    op.create_index('ix_verification_steps_verification_type', 'verification_steps', ['verification_id', 'step_type'], unique=False)


def downgrade() -> None:
    # Drop verification_steps table
    op.drop_index('ix_verification_steps_verification_type', table_name='verification_steps')
    op.drop_index('ix_verification_steps_verification_id', table_name='verification_steps')
    op.drop_index('ix_verification_steps_id', table_name='verification_steps')
    op.drop_table('verification_steps')
    
    # Drop verifications table
    op.drop_index('ix_verifications_company_status', table_name='verifications')
    op.drop_index('ix_verifications_status', table_name='verifications')
    op.drop_index('ix_verifications_token', table_name='verifications')
    op.drop_index('ix_verifications_company_id', table_name='verifications')
    op.drop_index('ix_verifications_candidate_id', table_name='verifications')
    op.drop_index('ix_verifications_id', table_name='verifications')
    op.drop_table('verifications')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS stepstatus')
    op.execute('DROP TYPE IF EXISTS steptype')
    op.execute('DROP TYPE IF EXISTS verificationstatus')
