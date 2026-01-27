"""Add Phase 2.5 hardening columns to verification_steps

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-27

New columns:
- flags: JSONB - Separate flags for HR visibility
- source: VARCHAR(50) - Who verified (surepass/manual)
- verified_at: TIMESTAMP - When truth was fetched
- review_assets: JSONB - HR-viewable files
- hr_notes: VARCHAR(2000) - HR documentation
- audit_trail: JSONB - Action history per step
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = 'b2c3d4e5f6g7'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add flags column
    op.add_column(
        'verification_steps',
        sa.Column('flags', JSONB, nullable=True)
    )
    
    # Add source column
    op.add_column(
        'verification_steps',
        sa.Column('source', sa.String(50), nullable=True)
    )
    
    # Add verified_at column
    op.add_column(
        'verification_steps',
        sa.Column('verified_at', sa.DateTime(), nullable=True)
    )
    
    # Add review_assets column
    op.add_column(
        'verification_steps',
        sa.Column('review_assets', JSONB, nullable=True)
    )
    
    # Add hr_notes column
    op.add_column(
        'verification_steps',
        sa.Column('hr_notes', sa.String(2000), nullable=True)
    )
    
    # Add audit_trail column
    op.add_column(
        'verification_steps',
        sa.Column('audit_trail', JSONB, nullable=True)
    )
    
    # Set default empty arrays for existing rows
    op.execute("UPDATE verification_steps SET flags = '[]'::jsonb WHERE flags IS NULL")
    op.execute("UPDATE verification_steps SET audit_trail = '[]'::jsonb WHERE audit_trail IS NULL")


def downgrade() -> None:
    op.drop_column('verification_steps', 'audit_trail')
    op.drop_column('verification_steps', 'hr_notes')
    op.drop_column('verification_steps', 'review_assets')
    op.drop_column('verification_steps', 'verified_at')
    op.drop_column('verification_steps', 'source')
    op.drop_column('verification_steps', 'flags')
