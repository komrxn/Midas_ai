"""Add Telegram integration fields to users table

Revision ID: add_telegram_fields
Revises: 
Create Date: 2025-12-16

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_telegram_fields'
down_revision = None  # Update this to your latest migration
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add Telegram integration fields."""
    # Add Telegram fields
    op.add_column('users', sa.Column('telegram_id', sa.BigInteger(), nullable=True))
    op.add_column('users', sa.Column('telegram_username', sa.String(50), nullable=True))
    op.add_column('users', sa.Column('telegram_first_name', sa.String(255), nullable=True))
    op.add_column('users', sa.Column('telegram_last_name', sa.String(255), nullable=True))
    
    # Make hashed_password nullable (Telegram users don't need passwords)
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(255),
                    nullable=True)
    
    # Create indexes
    op.create_index('ix_users_telegram_id', 'users', ['telegram_id'], unique=True)


def downgrade() -> None:
    """Remove Telegram integration fields."""
    # Drop indexes
    op.drop_index('ix_users_telegram_id', table_name='users')
    
    # Remove Telegram fields
    op.drop_column('users', 'telegram_last_name')
    op.drop_column('users', 'telegram_first_name')
    op.drop_column('users', 'telegram_username')
    op.drop_column('users', 'telegram_id')
    
    # Make hashed_password non-nullable again
    op.alter_column('users', 'hashed_password',
                    existing_type=sa.String(255),
                    nullable=False)
