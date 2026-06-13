from app.database.session import SessionLocal
from app.models.shift import Shift
from app.models.order import Order

def test_shift_requires_vehicle_allocation(client):

    response = client.post(
        "/api/driver/shifts/start", json={"driver_id": 100, "vehicle_id": 100}
    )

    assert response.status_code == 400


def test_driver_cannot_start_two_active_shifts(client):

    payload = {"driver_id": 1, "vehicle_id": 1}

    first = client.post("/api/driver/shifts/start", json=payload)

    second = client.post("/api/driver/shifts/start", json=payload)

    assert second.status_code == 409


def test_shift_requires_today_allocation(client):

    response = client.post(
        "/api/driver/shifts/start", json={"driver_id": 20, "vehicle_id": 10}
    )

    assert response.status_code == 400


def test_shift_cannot_close_with_pending_delivery(client):

    db = SessionLocal()

    shift = (
        db.query(Shift)
        .join(Order)
        .filter(Order.status.in_(["ASSIGNED", "IN_PROGRESS"]))
        .first()
    )

    assert shift is not None

    shift_id = shift.id

    db.close()

    response = client.post(f"/api/driver/shifts/{shift_id}/end")

    assert response.status_code == 409