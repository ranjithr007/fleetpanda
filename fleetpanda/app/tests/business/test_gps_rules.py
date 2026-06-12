def test_gps_requires_active_shift(client):

    response = client.post(
        "/api/driver/tracking/location",
        params={"vehicle_id": 999, "latitude": 12.9, "longitude": 77.5},
    )

    assert response.status_code == 400