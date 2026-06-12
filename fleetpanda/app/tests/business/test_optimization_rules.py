def test_driver_recommendation(client):

    response = client.get("/optimization/drivers/recommend")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_vehicle_recommendation(client):

    response = client.get("/optimization/vehicles/recommend")

    assert response.status_code == 200

    assert isinstance(response.json(), list)