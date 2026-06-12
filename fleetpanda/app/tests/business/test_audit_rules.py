def test_audit_logs_created(client):

    client.post("/allocations/1/cancel")

    response = client.get("/audit/logs")

    assert response.status_code == 200

    assert len(response.json()) > 0