from app.models.order import Order
from app.models.location import Location


class RouteRepository:

    def __init__(self, db):

        self.db = db

    def get_shift_orders(self, shift_id):

        return self.db.query(Order).filter(Order.shift_id == shift_id).all()

    def update_order(self, order):

        self.db.add(order)

        self.db.commit()

        return order