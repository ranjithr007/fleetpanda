def test_driver_performance_report(client):

    response = client.get("/analytics/drivers")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

    assert "driver_id" in data[0]

    assert "deliveries" in data[0]


def test_vehicle_utilization_report(client):

    response = client.get("/analytics/vehicles")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

    assert "vehicle_id" in data[0]

    assert "total_shifts" in data[0]


def test_incident_summary_report(client):

    response = client.get("/analytics/incidents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert len(data) > 0

    assert "incident_type" in data[0]

    assert "count" in data[0]