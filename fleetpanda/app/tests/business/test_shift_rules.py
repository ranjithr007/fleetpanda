
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