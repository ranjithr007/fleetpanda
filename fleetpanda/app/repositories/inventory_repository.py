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

    def get_inventory_for_update(self, location_id, product_id):
        return (
            self.db.query(Inventory)
            .filter(
                Inventory.location_id == location_id,
                Inventory.product_id == product_id,
            )
            .with_for_update()
            .first()
        )

    def update(self, inventory):

        self.db.add(inventory)

        return inventory