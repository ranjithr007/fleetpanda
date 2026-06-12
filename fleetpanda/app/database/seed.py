from datetime import datetime, date

from app.database.session import SessionLocal
from app.models.user import User
from app.models.driver import Driver
from app.models.vehicle import Vehicle
from app.models.vehicle_allocation import VehicleAllocation
from app.models.shift import Shift
from app.models.location import Location
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.order import Order
from app.models.order_item import OrderItem
from sqlalchemy import text
from datetime import datetime, timedelta
from app.models.vehicle_incident import VehicleIncident


def seed_data():

    db = SessionLocal()
    print("Deleting old seed data...")

    # Disable FK checks
    db.execute(text("""
            EXEC sp_MSforeachtable 
            'ALTER TABLE ? NOCHECK CONSTRAINT ALL'
            """))

    tables = [
        "inventory_transactions",
        "order_items",
        "orders",
        "gps_locations",
        "gps_location_history",
        "vehicle_current_location",
        "vehicle_incidents",
        "shifts",
        "vehicle_allocations",
        "inventory",
        "products",
        "locations",
        "drivers",
        "vehicles",
        "users",
    ]

    for table in tables:

        db.execute(text(f"DELETE FROM {table}"))

    # Enable FK checks again
    db.execute(text("""
            EXEC sp_MSforeachtable 
            'ALTER TABLE ? WITH CHECK CHECK CONSTRAINT ALL'
            """))

    identity_tables = [
        "users",
        "drivers",
        "vehicles",
        "vehicle_allocations",
        "shifts",
        "locations",
        "products",
        "inventory",
        "orders",
        "order_items",
        "inventory_transactions",
    ]

    for table in identity_tables:

        db.execute(text(f"DBCC CHECKIDENT ('{table}', RESEED, 0)"))
    db.commit()

    print("Old data removed")

    try:

        # avoid duplicate seed
        if db.query(User).count() > 0:

            print("Seed already exists")

            return

        # ======================
        # USERS
        # ======================

        users = []

        admin = User(
            name="Admin",
            email="admin@fleetpanda.com",
            phone="9000000000",
            role="ADMIN",
        )

        users.append(admin)

        for i in range(1, 21):

            users.append(
                User(
                    name=f"Driver {i}",
                    email=f"driver{i}@fleetpanda.com",
                    phone=f"90000000{i:02}",
                    role="DRIVER",
                )
            )

        db.add_all(users)

        db.flush()

        driver_users = [u for u in users if u.role == "DRIVER"]

        # ======================
        # DRIVER PROFILE
        # ======================

        drivers = []
        for index, user in enumerate(driver_users, start=1):

            drivers.append(
                Driver(
                    user_id=user.id,
                    license_number=f"KA-DL-{1000 + index}",
                    experience_years=index % 10 + 1,
                    status="ACTIVE",
                )
            )

        db.add_all(drivers)

        db.flush()

        # ======================
        # VEHICLES
        # ======================

        vehicles = []

        for i in range(1, 11):

            vehicles.append(
                Vehicle(
                    vehicle_number=f"FP-{1000+i}",
                    capacity_gallons=3000 + (i * 500),
                    status="AVAILABLE",
                )
            )

        db.add_all(vehicles)

        db.flush()

        # ======================
        # LOCATIONS
        # ======================

        terminal = Location(
            name="Terminal A",
            location_type="TERMINAL",
            address="Bangalore",
            latitude=12.9716,
            longitude=77.5946,
        )

        hub = Location(
            name="Main Hub",
            location_type="HUB",
            address="Bangalore",
            latitude=12.90,
            longitude=77.50,
        )

        db.add_all([terminal, hub])

        db.flush()

        # ======================
        # PRODUCTS
        # ======================

        diesel = Product(name="Diesel", unit="GALLON", status="ACTIVE")

        petrol = Product(name="Petrol", unit="GALLON", status="ACTIVE")

        db.add_all([diesel, petrol])

        db.flush()

        # ======================
        # INVENTORY
        # ======================

        inventory = Inventory(
            location_id=terminal.id, product_id=diesel.id, quantity=1000
        )

        db.add(inventory)

        db.flush()

        # ======================
        # VEHICLE ALLOCATION
        # ======================

        allocations = []

        for i in range(10):

            allocations.append(
                VehicleAllocation(
                    vehicle_id=vehicles[i].id,
                    driver_id=drivers[i].id,
                    allocation_date=date.today(),
                    status="ALLOCATED",
                )
            )

        db.add_all(allocations)

        db.flush()

        # ======================
        # SHIFT
        # ======================

        shifts = []
        for allocation in allocations:

            shifts.append(
                Shift(
                    allocation_id=allocation.id,
                    start_time=datetime.now(),
                    status="ACTIVE",
                )
            )

        db.add_all(shifts)

        db.flush()

        # ======================
        # ORDER
        # ======================

        orders = []

        for shift_index, shift in enumerate(shifts):

            # 3 deliveries per shift

            for sequence in range(1, 4):

                order = Order(
                    shift_id=shift.id,
                    destination_id=terminal.id,
                    sequence_number=sequence,
                    status="ASSIGNED",
                )

                orders.append(order)

        db.add_all(orders)

        db.flush()

        items = []

        for index, order in enumerate(orders):

            product = diesel if index % 2 == 0 else petrol

            items.append(
                OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity_gallons=500 + (index * 10),
                )
            )

        db.add_all(items)
        # ======================
        # VEHICLE INCIDENTS
        # ======================

        incidents = []

        incident_types = [
            "BREAKDOWN",
            "LOW_FUEL",
            "TYRE_PUNCTURE",
            "ENGINE_ISSUE",
            "ACCIDENT",
            "GPS_FAILURE",
            "MAINTENANCE",
            "BATTERY_FAILURE",
            "OIL_LEAK",
            "BRAKE_FAILURE",
        ]

        for i in range(10):

            incidents.append(
                VehicleIncident(
                    vehicle_id=vehicles[i].id,
                    shift_id=shifts[i].id,
                    driver_id=drivers[i].id,
                    incident_type=incident_types[i],
                    status=("OPEN" if i < 3 else "RESOLVED"),
                    created_at=(datetime.now() - timedelta(days=i)),
                )
            )

        db.add_all(incidents)

        db.flush()

        db.commit()

        print("FleetPanda seed completed successfully")

    except Exception as ex:

        db.rollback()

        print(ex)

    finally:

        db.close()


if __name__ == "__main__":

    seed_data()