"""add_vehicle_allocation_unique_constraints

Revision ID: bc5ed3131e65
Revises: 6d9c05ced0c8
Create Date: 2026-06-13 12:37:23.238531

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "bc5ed3131e65"
down_revision: Union[str, Sequence[str], None] = "6d9c05ced0c8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.execute("""
        WITH duplicate_allocations AS
        (
            SELECT
                id,
                ROW_NUMBER() OVER
                (
                    PARTITION BY vehicle_id
                    ORDER BY id DESC
                ) rn
            FROM vehicle_allocations
            WHERE status='ACTIVE'
        )
        UPDATE vehicle_allocations
        SET status='CANCELLED'
        WHERE id IN
        (
            SELECT id
            FROM duplicate_allocations
            WHERE rn > 1
        )
        """)
    op.execute("""
    IF NOT EXISTS(
        SELECT 1 
        FROM sys.indexes
        WHERE name='UX_vehicle_active_allocation'
    )
    BEGIN

        CREATE UNIQUE INDEX UX_vehicle_active_allocation
        ON vehicle_allocations(vehicle_id)
        WHERE status='ACTIVE'

    END
    """)

    op.execute("""
    IF NOT EXISTS(
        SELECT 1
        FROM sys.indexes
        WHERE name='UX_driver_active_allocation'
    )
    BEGIN

        CREATE UNIQUE INDEX UX_driver_active_allocation
        ON vehicle_allocations(driver_id)
        WHERE status='ACTIVE'

    END
    """)


def downgrade():

    op.execute("""
    DROP INDEX UX_vehicle_active_allocation
    ON vehicle_allocations
    """)

    op.execute("""
    DROP INDEX UX_driver_active_allocation
    ON vehicle_allocations
    """)
