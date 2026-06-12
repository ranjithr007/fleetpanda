def test_dashboard_summary(client):

    response = client.get("/dashboard/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_vehicles" in data

    assert "available_vehicles" in data

    assert "out_of_service" in data

    assert "active_drivers" in data

    assert "active_shifts" in data

    assert "open_incidents" in data

    assert "completed_orders" in data


def test_dashboard_counts(client):

    response = client.get("/dashboard/summary")

    data = response.json()

    assert data["total_vehicles"] == 10

    assert data["active_drivers"] == 20

    assert data["active_shifts"] == 10