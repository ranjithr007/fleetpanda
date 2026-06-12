from app.database.session import SessionLocal
from app.models.order import Order
def test_complete_delivery_updates_inventory(client):

    db = SessionLocal()

    order = db.query(Order).filter(Order.id == 5).first()

    order.status = "ASSIGNED"

    db.commit()
    db.close()

    response = client.post("/api/driver/deliveries/5/start")

    print("START:", response.status_code, response.json())

    assert response.status_code == 200

    response = client.post("/api/driver/deliveries/5/complete")

    print("COMPLETE:", response.status_code, response.json())

    assert response.status_code == 200


def test_inventory_rollback_on_failure(client):

    response = client.post("/api/driver/deliveries/999/complete")

    assert response.status_code == 404