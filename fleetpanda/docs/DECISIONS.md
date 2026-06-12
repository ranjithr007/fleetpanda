# Technical Decisions


## Architecture


Used Clean Layered Architecture:


API Routes

↓

Services

↓

Repositories

↓

Database



## Framework

FastAPI selected because:

- high performance
- automatic OpenAPI documentation
- dependency injection support



## Database

SQL Server with SQLAlchemy ORM.


Reasons:

- transactions
- locking support
- relational consistency



## Vehicle Allocation


Problem:

Two admins allocate same vehicle.


Solution:

- check existing allocation
- database unique constraint
- handle IntegrityError



## Inventory Consistency


Delivery completion uses a single transaction:


1. Update order status

2. Increase inventory

3. Create inventory transaction


Rollback on failure.



## GPS Design


Two table approach:


gps_location_history

- stores all points


vehicle_current_location

- optimized dashboard lookup



## Authentication


Out of scope.

Stub user model added for future extension.



## Real Time Updates


WebSocket intentionally skipped.

Out of scope.