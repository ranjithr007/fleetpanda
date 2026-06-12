from dataclasses import dataclass


@dataclass
class DeliveryCompletedEvent:

    order_id: int

    driver_id: int

    vehicle_id: int


@dataclass
class IncidentCreatedEvent:

    incident_id: int

    vehicle_id: int


@dataclass
class AllocationCreatedEvent:

    allocation_id: int

    vehicle_id: int

    driver_id: int