from app.repositories.optimization_repository import OptimizationRepository


class OptimizationService:

    def __init__(self, db):

        self.repo = OptimizationRepository(db)

    def recommend_driver(self):

        drivers = self.repo.available_drivers()

        scores = []

        for d in drivers:

            score = d.experience_years * 10

            scores.append({"driver_id": d.id, "score": score})

        return sorted(scores, key=lambda x: x["score"], reverse=True)

    def recommend_vehicle(self):

        vehicles = self.repo.available_vehicles()

        scores = []

        for v in vehicles:

            score = v.capacity_gallons / 100

            scores.append({"vehicle_id": v.id, "score": score})

        return sorted(scores, key=lambda x: x["score"], reverse=True)