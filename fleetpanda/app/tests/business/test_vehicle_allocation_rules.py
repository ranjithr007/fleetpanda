
from datetime import date, timedelta
def test_vehicle_double_allocation_blocked(client):

    payload = {"vehicle_id": 1, "driver_id": 1, "allocation_date": str(date.today() + timedelta(days=1))}

    first = client.post("/api/admin/allocations", json=payload)

    second = client.post("/api/admin/allocations", json=payload)

    assert second.status_code == 409