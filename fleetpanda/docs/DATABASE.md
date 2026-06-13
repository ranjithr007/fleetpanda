# FleetPanda Database Design

## Overview

FleetPanda uses SQL Server as the primary relational database.

The schema is designed for:

- Strong consistency
- Transaction safety
- Operational reporting
- Auditability
- Future scalability


Database principles:

- Normalized relational design
- Foreign key relationships
- Database enforced business constraints
- Transaction safe workflows
- Concurrency protection
- Row level locking for critical resources
- Optimized read models where required


---

# Database Technology


| Component | Technology |
|-|-|
| Database | SQL Server |
| ORM | SQLAlchemy |
| Migration | Alembic |
| Access Pattern | Repository Layer |


---


# Entity Relationship Overview


```
Driver

  |

Vehicle Allocation

  |

Shift

  |

Order

  |

Order Items

  |

Inventory Transaction



Vehicle

  |

Allocation

  |

GPS Tracking



Vehicle

  |

Incident

  |

Availability Control
```


---

# Core Tables


# vehicles


Stores fleet vehicle information.


Responsibilities:


- Vehicle identity
- Availability tracking
- Operational status


Important columns:


```
id

vehicle_number

status

created_at
```


Status:


```
AVAILABLE

ALLOCATED

OUT_OF_SERVICE
```


Used by:

- Allocation module
- Incident module
- Tracking module


---


# drivers


Stores driver information.


Responsibilities:


- Driver profile
- Driver availability


Status:


```
ACTIVE

INACTIVE
```


Relationship:


```
Driver

 1

 |

 *

Vehicle Allocation
```


---

# vehicle_allocations


Stores vehicle-driver assignments.


Responsibilities:


- Assign vehicle
- Assign driver
- Maintain allocation history


Relationship:


```
Vehicle

   |

Vehicle Allocation

   |

Driver
```


Status:


```
ACTIVE

CANCELLED
```


Business Rules:


Only available vehicles can be allocated.


Duplicate active allocations are prevented using:


- Service validation
- Database constraint
- Transaction handling


````md
Database Constraint:


```sql
CREATE UNIQUE INDEX uq_vehicle_active_allocation
ON vehicle_allocations(vehicle_id)
WHERE status = 'ACTIVE';
```


---

## 3. Update inventories section

After:

```md
Updated only through delivery completion workflow.
```

Add:

````md
Concurrency Protection:


Inventory updates use pessimistic locking.


Flow:


```
Begin Transaction

      |

Lock Inventory Row

      |

Validate Available Quantity

      |

Update Quantity

      |

Commit
```


Implemented using SQL row locking through SQLAlchemy.


Prevents:


- Lost updates
- Negative inventory
- Concurrent deduction issues


Database Protection:


```sql
CHECK(quantity >= 0)
```

---

# shifts


Stores driver working sessions.


Relationship:


```
Vehicle Allocation

        |

       Shift
```


Lifecycle:


```
CREATED

   |

ACTIVE

   |

COMPLETED
```


Business Constraints:


Only one ACTIVE shift is allowed per driver.


Database Protection:


```sql
CREATE UNIQUE INDEX uq_driver_active_shift
ON shifts(driver_id)
WHERE status='ACTIVE';
```


Prevents:


- Duplicate active sessions
- Concurrent shift creation


---

# orders


Stores delivery information.


Responsibilities:


- Delivery workflow
- Destination tracking
- Status management


Lifecycle:


```
ASSIGNED

    |

IN_PROGRESS

    |

COMPLETED
```


Alternative:


```
FAILED
```


Relationship:


```
Shift

 |

Orders
```


---

# order_items


Stores delivery products.


Relationship:


```
Order

  |

Order Items

  |

Products
```


Stores:


```
product_id

quantity_gallons
```


---

# products


Stores fuel/product catalog.


Examples:


```
Diesel

Petrol
```


Used by:


- Orders
- Inventory


---

# inventories


Stores current stock levels.


Unique inventory:


```
location_id

product_id
```


Tracks:


```
available quantity
```


Updated only through delivery completion workflow.


---

# inventory_transactions


Stores inventory movement history.


Purpose:


- Traceability
- Audit
- Stock reconciliation


Example:


```
DELIVERY_COMPLETED

+500 gallons
```


Relationship:


```
Inventory

     |

Inventory Transactions
```


---

# gps_location_history


Stores driver GPS events.


Purpose:


Historical tracking.


Stores:


```
vehicle

latitude

longitude

timestamp
```


Rules:


GPS update requires active shift.


---

# vehicle_current_location


Optimized read table.


Purpose:


Fleet dashboard performance.


Instead of scanning:


```
gps_location_history
```


Dashboard reads:


```
vehicle_current_location
```


Pattern:


CQRS style read optimization.


---

# vehicle_incidents


Stores vehicle operational issues.


Examples:


- Engine failure
- Maintenance issue
- Breakdown


Workflow:


```
Incident Created

        |

Vehicle OUT_OF_SERVICE
```


Status:


```
OPEN

RESOLVED
```


---

# audit_logs


Stores business activity history.


Captured:


```
entity_name

entity_id

action

old_value

new_value

performed_by

created_at
```


Examples:


Allocation:


```
ACTIVE -> CANCELLED
```


Delivery:


```
IN_PROGRESS -> COMPLETED
```


Incident:


```
AVAILABLE -> OUT_OF_SERVICE
```


---

# Data Consistency Rules


## Allocation Consistency


Prevent duplicate allocation:


Application:

```
Check existing allocation
```


Database:


```
Unique Constraint
```


---

# Transaction Boundaries


Critical workflows execute transactionally.


Examples:


Delivery Completion:


```
Update Delivery

Update Inventory

Create Transaction

Commit
```


Incident:


```
Create Incident

Update Vehicle

Audit

Commit
```


---

# Index Strategy


Recommended indexes:


Vehicle allocation:


```sql
vehicle_id,
allocation_date
```


Tracking:


```sql
vehicle_id,
created_at
```


Orders:


```sql
status
```


---

---

# Database Hardening


FleetPanda applies database-first consistency rules.


## Foreign Key Protection


Relationships are enforced using foreign keys.


Examples:


```
drivers
   |
vehicle_allocations


vehicles
   |
vehicle_allocations


orders
   |
order_items
```


Prevents:


- Orphan records
- Invalid references



---


## Transaction Isolation


Critical workflows execute inside database transactions.


Protected operations:


- Vehicle allocation
- Allocation cancellation
- Delivery completion
- Inventory updates
- Shift lifecycle changes


Failure handling:


```
Operation Start

       |

Database Error?

       |

Rollback

       |

Restore Previous State
```



---


## Concurrency Handling


Race conditions are handled using:


- Database constraints
- Row locks
- Transaction isolation


Protected scenarios:


| Scenario | Protection |
|-|-|
| Two admins allocate same vehicle | Unique constraint |
| Two inventory updates | Row locking |
| Two active shifts | Unique constraint |



---


## Ownership Security


Driver owned data is validated at query level.


Example:


Driver APIs filter using:


```sql
WHERE driver_id = current_driver_id
```


Prevents:


- Unauthorized access
- Cross driver data exposure

---

# Migration Strategy


Alembic manages database changes.


Commands:


Create migration:


```bash
alembic revision --autogenerate -m "message"
```


Apply:


```bash
alembic upgrade head
```


---

# Future Database Enhancements


Planned:


## Authentication Tables


```
users

roles

permissions
```


Supports:


- JWT
- RBAC


---


## Event Outbox


Table:


```
outbox_events
```


Purpose:


Reliable async messaging.


Future:


```
SQL Server

 |

Outbox Worker

 |

Kafka
```


---

# Database Summary


FleetPanda database is designed for:


✔ Relational integrity

✔ Transaction safety

✔ Operational workflows

✔ Audit tracking

✔ Reporting

✔ Future scaling
