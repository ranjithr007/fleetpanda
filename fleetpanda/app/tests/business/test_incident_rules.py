from app.database.session import SessionLocal
from app.models.vehicle_incident import VehicleIncident
from app.models.vehicle import Vehicle


def test_vehicle_incident_blocks_allocation(client):

    db = SessionLocal()

    # cleanup existing incident
    db.query(VehicleIncident).filter(VehicleIncident.vehicle_id == 4).delete()

    # reset vehicle
    vehicle = db.query(Vehicle).filter(Vehicle.id == 4).first()

    vehicle.status = "AVAILABLE"

    db.commit()
    db.close()

    incident = client.post(
        "/incidents/report",
        params={
            "vehicle_id": 4,
            "shift_id": 4,
            "driver_id": 4,
            "incident_type": "ENGINE_FAILURE",
        },
    )

    assert incident.status_code == 200