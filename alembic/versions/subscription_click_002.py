"""Add subscription and click transactions

Revision ID: subscription_click_002
Revises: seed_categories_001
Create Date: 2026-01-05 16:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'subscription_click_002'
down_revision = ('add_language_001', 'phone_auth_migration')
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add subscription columns to users table
    op.add_column('users', sa.Column('is_premium', sa.Boolean(), server_default='false', nullable=False))
    op.add_column('users', sa.Column('subscription_type', sa.String(length=20), nullable=True))
    op.add_column('users', sa.Column('subscription_ends_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('is_trial_used', sa.Boolean(), server_default='false', nullable=False))

    # 2. Create click_transactions table
    op.create_table('click_transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('click_trans_id', sa.BigInteger(), nullable=False),
        sa.Column('service_id', sa.BigInteger(), nullable=False),
        sa.Column('click_paydoc_id', sa.BigInteger(), nullable=False),
        sa.Column('merchant_trans_id', sa.String(), nullable=False),
        sa.Column('amount', sa.Numeric(precision=18, scale=2), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('action', sa.Integer(), nullable=False),
        sa.Column('sign_time', sa.String(), nullable=False),
        sa.Column('error', sa.Integer(), nullable=True),
        sa.Column('error_note', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_click_transactions_click_trans_id'), 'click_transactions', ['click_trans_id'], unique=True)
    op.create_index(op.f('ix_click_transactions_merchant_trans_id'), 'click_transactions', ['merchant_trans_id'], unique=False)


def downgrade() -> None:
    # Drop table
    op.drop_index(op.f('ix_click_transactions_merchant_trans_id'), table_name='click_transactions')
    op.drop_index(op.f('ix_click_transactions_click_trans_id'), table_name='click_transactions')
    op.drop_table('click_transactions')

    # Drop columns
    op.drop_column('users', 'is_trial_used')
    op.drop_column('users', 'subscription_ends_at')
    op.drop_column('users', 'subscription_type')
    op.drop_column('users', 'is_premium')
