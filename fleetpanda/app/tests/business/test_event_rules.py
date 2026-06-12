from app.events.event_bus import event_bus
from app.events.events import DeliveryCompletedEvent


def test_event_publish():

    called = []

    def handler(event):

        called.append(event.order_id)

    event_bus.subscribe(DeliveryCompletedEvent, handler)

    event_bus.publish(DeliveryCompletedEvent(order_id=1, driver_id=1, vehicle_id=1))

    assert called[0] == 1