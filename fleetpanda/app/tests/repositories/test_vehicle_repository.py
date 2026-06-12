from unittest.mock import MagicMock

from app.repositories.vehicle_repository import VehicleRepository


def test_vehicle_repository_created():

    db = MagicMock()

    repo = VehicleRepository(db)

    assert repo is not None