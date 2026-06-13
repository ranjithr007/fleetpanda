from unittest.mock import MagicMock
from datetime import date, timedelta

from app.services.allocation_service import AllocationService
from app.models.vehicle_allocation import VehicleAllocation
from app.database.session import SessionLocal
from app.models.vehicle import Vehicle


def test_allocation_service_created():

    fake_db = MagicMock()

    service = AllocationService(fake_db)

    assert service is not None


def test_cannot_allocate_out_of_service_vehicle(client):

    db = SessionLocal()

    vehicle = db.query(Vehicle).filter(Vehicle.id == 1).first()

    vehicle.status = "OUT_OF_SERVICE"

    db.commit()
    db.close()

    response = client.post(
        "/api/admin/allocations",
        json={
            "vehicle_id": 1,
            "driver_id": 1,
            "allocation_date": str(date.today() + timedelta(days=1)),
        },
    )

    assert response.status_code == 409


def test_cannot_create_past_allocation(client):

    response = client.post(
        "/api/admin/allocations",
        json={"vehicle_id": 1, "driver_id": 1, "allocation_date": "2020-01-01"},
    )

    assert response.status_code == 404


def test_cancel_active_allocation_blocked(client):

    db = SessionLocal()

    allocation = db.query(VehicleAllocation).filter(VehicleAllocation.id == 1).first()

    assert allocation is not None

    #
    # cleanup existing active allocations
    #
    db.query(VehicleAllocation).filter(
        VehicleAllocation.id != allocation.id,
        VehicleAllocation.status == "ACTIVE",
        (
            (VehicleAllocation.vehicle_id == allocation.vehicle_id)
            | (VehicleAllocation.driver_id == allocation.driver_id)
        ),
    ).update({VehicleAllocation.status: "COMPLETED"}, synchronize_session=False)

    # now safe
    allocation.status = "ACTIVE"

    db.commit()

    response = client.post(f"/api/admin/allocations/{allocation.id}/cancel")

    assert response.status_code == 409

    db.close()