
from datetime import date, timedelta
def test_get_vehicles(client):

    response = client.get("/api/admin/vehicles")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_allocate_vehicle(client):

    payload = {"vehicle_id": 1, "driver_id": 1, "allocation_date": str(date.today() + timedelta(days=1))}

    response = client.post("/api/admin/allocations", json=payload)

    assert response.status_code in [200, 409]