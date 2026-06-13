from datetime import date

from app.database.session import SessionLocal

from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.vehicle_allocation import VehicleAllocation


def test_vehicle_status_changes_after_allocation(client):

    db = SessionLocal()

    vehicle = db.query(Vehicle).first()

    driver = db.query(Driver).filter(Driver.status == "ACTIVE").first()

    assert vehicle is not None
    assert driver is not None

    vehicle.status = "AVAILABLE"

    db.query(VehicleAllocation).filter(
        VehicleAllocation.driver_id == driver.id, VehicleAllocation.status == "ACTIVE"
    ).update({VehicleAllocation.status: "COMPLETED"})

    db.commit()

    response = client.post(
        "/api/admin/allocations",
        json={
            "vehicle_id": vehicle.id,
            "driver_id": driver.id,
            "allocation_date": str(date.today()),
        },
    )

    assert response.status_code == 200

    db.refresh(vehicle)

    assert vehicle.status == "ALLOCATED"

    db.close()