def test_route_optimization(client):

    response = client.post("/routes/optimize/1")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert "order_id" in data[0]

    assert "sequence" in data[0]