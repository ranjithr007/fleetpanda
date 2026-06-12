from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:

    def __init__(self, db):

        self.repository = DashboardRepository(db)

    def get_summary(self):

        return self.repository.summary()