from app.events.event_bus import event_bus

from app.events.events import DeliveryCompletedEvent, IncidentCreatedEvent


from app.events.handlers import audit_delivery_completed, notify_incident_created


def register_events():

    event_bus.subscribe(DeliveryCompletedEvent, audit_delivery_completed)

    event_bus.subscribe(IncidentCreatedEvent, notify_incident_created)