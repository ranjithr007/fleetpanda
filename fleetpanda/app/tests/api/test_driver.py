from datetime import date


def test_driver_deliveries(client):

    response = client.get("/api/driver/deliveries/2")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_tracking(client):

    allocation_response = client.post(
        "/api/admin/allocations",
        json={"vehicle_id": 1, "driver_id": 1, "allocation_date": str(date.today())},
    )

    print("ALLOCATION:", allocation_response.status_code, allocation_response.text)

    shift_response = client.post(
        "/api/driver/shifts/start", json={"driver_id": 1, "vehicle_id": 1}
    )

    print("SHIFT:", shift_response.status_code, shift_response.text)

    response = client.post(
        "/api/driver/tracking/location",
        params={"vehicle_id": 1, "latitude": 12.9, "longitude": 77.5},
    )

    print("TRACKING:", response.status_code, response.text)

    assert response.status_code == 200