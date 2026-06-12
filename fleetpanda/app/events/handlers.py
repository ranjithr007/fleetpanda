
from app.events.events import DeliveryCompletedEvent, IncidentCreatedEvent


def audit_delivery_completed(event: DeliveryCompletedEvent):

    print(f"AUDIT Delivery Completed {event.order_id}")


def notify_incident_created(event: IncidentCreatedEvent):

    print(f"NOTIFY Incident {event.incident_id}")