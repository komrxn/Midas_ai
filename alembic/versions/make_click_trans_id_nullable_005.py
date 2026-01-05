"""make_click_trans_id_nullable

Revision ID: make_id_null_005
Revises: restore_language_column_004
Create Date: 2026-01-05 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'make_id_null_005'
down_revision: Union[str, None] = 'restore_language_column_004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make click_trans_id nullable
    op.alter_column('click_transactions', 'click_trans_id',
               existing_type=sa.BigInteger(),
               nullable=True)


def downgrade() -> None:
    # Revert to not nullable (might fail if nulls exist)
    op.alter_column('click_transactions', 'click_trans_id',
               existing_type=sa.BigInteger(),
               nullable=False)
