"""Restore language column to users table

Revision ID: restore_language_column_004
Revises: reseed_categories_003
Create Date: 2026-01-05 16:50:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = 'restore_language_column_004'
down_revision = 'reseed_categories_003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use inspector to check if column exists
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    if 'language' not in columns:
        op.add_column('users', sa.Column('language', sa.String(length=2), server_default='uz', nullable=False))

def downgrade() -> None:
    pass
