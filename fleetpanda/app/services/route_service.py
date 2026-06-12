from app.repositories.route_repository import RouteRepository

from app.utils.distance import calculate_distance


class RouteService:

    def __init__(self, db):

        self.repo = RouteRepository(db)

    def optimize_route(self, shift_id):

        orders = self.repo.get_shift_orders(shift_id)

        optimized = []

        current_lat = 12.9716
        current_lon = 77.5946

        for order in orders:

            distance = calculate_distance(
                current_lat,
                current_lon,
                order.destination.latitude,
                order.destination.longitude,
            )

            optimized.append({"order": order, "distance": distance})

        optimized.sort(key=lambda x: x["distance"])

        sequence = 1

        result = []

        for item in optimized:

            order = item["order"]

            order.sequence_number = sequence

            self.repo.update_order(order)

            result.append(
                {
                    "order_id": order.id,
                    "sequence": sequence,
                    "distance_km": round(item["distance"], 2),
                }
            )

            sequence += 1

        return result