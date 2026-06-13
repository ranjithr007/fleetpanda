"""add_status_column

Revision ID: 68a45c97005c
Revises: e6d6d9e27870
Create Date: 2026-06-13 10:29:15.360563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68a45c97005c'
down_revision: Union[str, Sequence[str], None] = 'e6d6d9e27870'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
