
from app.database.session import SessionLocal
from app.models.order import Order


def test_cannot_complete_without_start(client):

    response = client.post("/api/driver/deliveries/1/complete")

    assert response.status_code == 409


def test_start_and_complete_delivery(client):

    # Arrange
    db = SessionLocal()

    order = db.query(Order).filter(Order.id == 2).first()

    order.status = "ASSIGNED"

    db.commit()
    db.close()

    # Act - start delivery
    start = client.post("/api/driver/deliveries/2/start")

    assert start.status_code == 200

    # Act - complete delivery
    complete = client.post("/api/driver/deliveries/2/complete")

    assert complete.status_code == 200


def test_duplicate_delivery_complete_blocked(client):

    client.post("/api/driver/deliveries/1/start")

    client.post("/api/driver/deliveries/1/complete")

    second = client.post("/api/driver/deliveries/1/complete")

    assert second.status_code == 409


def test_driver_cannot_complete_other_driver_delivery(client):

    response = client.post(
        "/api/driver/deliveries/10/complete", headers={"driver-id":"999"}
    )

    assert response.status_code == 403