from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self, db):

        self.repo = AnalyticsRepository(db)

    def driver_performance(self):

        data = self.repo.driver_performance()

        return [
            {"driver_id": x.driver_id, "deliveries": x.total_deliveries} for x in data
        ]

    def vehicle_utilization(self):

        data = self.repo.vehicle_utilization()

        return [
            {"vehicle_id": x.vehicle_id, "total_shifts": x.total_shifts} for x in data
        ]

    def incident_summary(self):

        data = self.repo.incident_summary()

        return [{"incident_type": x[0], "count": x[1]} for x in data]