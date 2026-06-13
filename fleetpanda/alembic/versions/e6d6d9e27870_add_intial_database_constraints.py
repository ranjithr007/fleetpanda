"""add_be3_database_constraints

Revision ID: e6d6d9e27870
Revises: ae55efd49662
Create Date: 2026-06-13 10:19:43.933354

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e6d6d9e27870"
down_revision: Union[str, Sequence[str], None] = "ae55efd49662"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    # Add allocation lifecycle
    op.add_column(
        "allocations",
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
    )

    # Only one active allocation per vehicle
    op.execute("""
        CREATE UNIQUE INDEX UX_active_vehicle_allocation
        ON allocations(vehicle_id)
        WHERE status='ACTIVE'
    """)

    # Only one active allocation per driver(user)
    op.execute("""
        CREATE UNIQUE INDEX UX_active_driver_allocation
        ON allocations(user_id)
        WHERE status='ACTIVE'
    """)

    # Valid allocation states only
    op.execute("""
        ALTER TABLE allocations
        ADD CONSTRAINT CK_allocation_status
        CHECK (
            status IN
            ('ACTIVE','COMPLETED','CANCELLED')
        )
    """)


def downgrade():

    op.execute("DROP INDEX UX_active_vehicle_allocation ON allocations")

    op.execute("DROP INDEX UX_active_driver_allocation ON allocations")

    op.execute("ALTER TABLE allocations DROP CONSTRAINT CK_allocation_status")

    op.drop_column("allocations", "status")
