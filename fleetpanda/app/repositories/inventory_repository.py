from app.models.inventory import Inventory
from app.models.inventory_transaction import InventoryTransaction


class InventoryRepository:

    def __init__(self, db):

        self.db = db

    def get_inventory(self, location_id, product_id):

        return (
            self.db.query(Inventory)
            .filter(
                Inventory.location_id == location_id, Inventory.product_id == product_id
            )
            .first()
        )

    def update(self, inventory):

        self.db.add(inventory)

        return inventory

    