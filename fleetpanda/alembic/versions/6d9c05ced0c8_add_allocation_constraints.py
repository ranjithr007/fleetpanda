"""add_allocation_constraints

Revision ID: 6d9c05ced0c8
Revises: 68a45c97005c
Create Date: 2026-06-13 10:37:10.741721

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6d9c05ced0c8"
down_revision: Union[str, Sequence[str], None] = "68a45c97005c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.execute("""
    IF NOT EXISTS (
        SELECT 1 
        FROM sys.indexes 
        WHERE name='UX_active_vehicle_allocation'
    )
    BEGIN
        CREATE UNIQUE INDEX UX_active_vehicle_allocation
        ON allocations(vehicle_id)
        WHERE status='ACTIVE'
    END
    """)

    op.execute("""
    IF NOT EXISTS (
        SELECT 1 
        FROM sys.indexes 
        WHERE name='UX_active_driver_allocation'
    )
    BEGIN
        CREATE UNIQUE INDEX UX_active_driver_allocation
        ON allocations(user_id)
        WHERE status='ACTIVE'
    END
    """)

    op.execute("""
    IF NOT EXISTS (
        SELECT 1
        FROM sys.check_constraints
        WHERE name='CK_allocation_status'
    )
    BEGIN
        ALTER TABLE allocations
        ADD CONSTRAINT CK_allocation_status
        CHECK(
            status IN
            (
            'ACTIVE',
            'COMPLETED',
            'CANCELLED'
            )
        )
    END
    """)


def downgrade() -> None:

    op.execute("""
    IF EXISTS (
        SELECT 1 
        FROM sys.indexes
        WHERE name='UX_active_vehicle_allocation'
    )
    DROP INDEX UX_active_vehicle_allocation 
    ON allocations
    """)

    op.execute("""
    IF EXISTS (
        SELECT 1 
        FROM sys.indexes
        WHERE name='UX_active_driver_allocation'
    )
    DROP INDEX UX_active_driver_allocation 
    ON allocations
    """)

    op.execute("""
    IF EXISTS (
        SELECT 1
        FROM sys.check_constraints
        WHERE name='CK_allocation_status'
    )
    ALTER TABLE allocations
    DROP CONSTRAINT CK_allocation_status
    """)
