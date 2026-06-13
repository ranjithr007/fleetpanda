from concurrent.futures import ThreadPoolExecutor
from datetime import date
from app.models.vehicle_allocation import VehicleAllocation

from app.database.session import SessionLocal

from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.order import Order


def test_prevent_double_vehicle_allocation(client):

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

    payload = {
        "vehicle_id": vehicle.id,
        "driver_id": driver.id,
        "allocation_date": str(date.today()),
    }

    db.close()

    def allocate():

        return client.post("/api/admin/allocations", json=payload)

    with ThreadPoolExecutor(max_workers=2) as executor:

        results = list(executor.map(lambda _: allocate(), range(2)))

    codes = [r.status_code for r in results]

    assert codes.count(200) == 1
    assert codes.count(409) == 1


def test_prevent_double_delivery_completion(client):

    db = SessionLocal()

    order = db.query(Order).filter(Order.status == "ASSIGNED").first()

    assert order is not None

    order.status = "IN_PROGRESS"

    db.commit()

    order_id = order.id

    db.close()

    def complete():

        return client.post(f"/api/driver/deliveries/{order_id}/complete")

    with ThreadPoolExecutor(max_workers=2) as executor:

        results = list(executor.map(lambda _: complete(), range(2)))

    codes = [r.status_code for r in results]

    assert codes.count(200) == 1
    assert codes.count(409) == 1