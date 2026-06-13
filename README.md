# FleetPanda Fleet Tracking Platform

A REST API backend for real-time fleet, driver, delivery, inventory, and incident management operations.

Built using FastAPI with Clean Architecture principles for scalable logistics workflows.

---

# Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy ORM
- SQL Server
- Alembic Database Migration
- Pytest
- Pydantic
- Docker Ready
- Database Transactions
- SQL Server Constraints
- Concurrency Control
- Row Level Locking

---

# Architecture


```
Client

  |

FastAPI Routes

  |

Application Services

  |

Repository Layer

  |

SQL Server
```

Architecture principles:

- Clean Architecture
- Service Layer Pattern
- Repository Pattern
- Domain workflow isolation
- Transaction boundary at service layer
- Database consistency first approach
- Event-driven extension support


---

# Project Structure


```
app/

├── api/
│   └── routes/
│       ├── admin/
│       └── driver/
│
├── core/
│   ├── config.py
│   └── exception.py
│
├── database/
│
├── models/
│
├── schemas/
│
├── repositories/
│
├── services/
│
├── events/
│
└── tests/
```


---

# Getting Started


## Create Environment


```bash
python -m venv venv
```


Activate:


Windows:

```bash
venv\Scripts\activate
```


Install dependencies:


```bash
pip install -r requirements.txt
```


---
# Environment Configuration

FleetPanda uses environment variables for application configuration.

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
```

For local SQL Server development:

```env
DATABASE_URL=mssql+pyodbc://localhost/FleetPanda?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes
```

The application reads this configuration during startup.

Never commit `.env` files containing real credentials.

---


# Database Setup


Configure SQL Server connection.

Run migrations:


```bash
alembic upgrade head
```


---

# Database Seeding

FleetPanda provides seed data to quickly prepare a local development environment.

Seed data creates the initial records required for testing fleet workflows.

Seed includes:

- Vehicles
- Drivers
- Locations
- Products
- Inventory
- Vehicle allocations
- Shifts
- Delivery orders
- Order items

---

## Run Database Seed

After applying migrations:

```bash
alembic upgrade head
```

execute:

```bash
python -m app.database.seed
```

---

## Seed Data Flow

The seeded data supports complete end-to-end testing:


```
Vehicle

   +

Driver

   |

Vehicle Allocation

   |

Shift

   |

Delivery Order

   |

Order Items

   |

Delivery Completion

   |

Inventory Update
```

---

## Reset Development Data

For a clean environment:


1. Rollback database

```bash
alembic downgrade base
```

---

# Run Application


```bash
python -m uvicorn app.main:app --reload
```


Swagger:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```


---

# API Overview


## Admin Operations

Base:

```
/api/admin
```


| Operation | Endpoint |
|-|-|
| Manage vehicles | /vehicles |
| Manage drivers | /drivers |
| Allocate vehicle | /allocations |
| Cancel allocation | /allocations/{id}/cancel |
| Monitor fleet | /fleet |


---


## Driver Operations


Base:

```
/api/driver
```


| Operation | Endpoint |
|-|-|
| View deliveries | /deliveries |
| Start delivery | /deliveries/{id}/start |
| Complete delivery | /deliveries/{id}/complete |
| Fail delivery | /deliveries/{id}/fail |
| Send GPS | /tracking/location |
| Report incident | /incidents/report |


---

# Vehicle Allocation Lifecycle


```
AVAILABLE

    |

ALLOCATE

    |

ALLOCATED


    |

INCIDENT

    |

OUT_OF_SERVICE
```


Rules:

| Rule | Handling |
|-|-|
| Duplicate allocation | 409 Conflict |
| Vehicle unavailable | Block allocation |
| Driver inactive | Block allocation |


---

# Delivery Lifecycle


```
ASSIGNED

    |

START

    |

IN_PROGRESS


     +------------+

     |            |

 COMPLETED     FAILED
```


Rules:

- Delivery must start before completion
- Completed delivery cannot be modified
- Inventory updates only after completion


---

# Shift Lifecycle


```
CREATED

   |

ACTIVE

   |

COMPLETED
```


Designed for operational extensions:

```
CANCELLED
```


---

# Inventory Workflow


Delivery completion:


```
Complete Delivery

       |

Inventory Update

       |

Inventory Transaction
```


Ensures:

- Accurate stock
- Movement history
- Traceability

---

---

# Production Hardening


FleetPanda implements backend reliability patterns required for production fleet operations.


## Database Integrity


Critical business rules are protected at database level.


Implemented:

- Foreign key constraints
- Unique constraints
- Check constraints
- Referential integrity


Protects against:

- Invalid relationships
- Duplicate active records
- Data corruption



---


## Transaction Management


Business workflows execute inside database transactions.


Protected workflows:


- Vehicle allocation
- Allocation cancellation
- Inventory deduction
- Shift lifecycle updates


Guarantees:


- Atomic updates
- Automatic rollback
- Consistent state



---


## Concurrency Protection


FleetPanda protects critical resources during simultaneous requests.


Implemented:

- SQL Server row level locking
- Transaction isolation
- Atomic updates


Protected scenarios:


- Multiple users allocating same vehicle
- Concurrent inventory deduction
- Duplicate shift creation



---


## Inventory Locking


Inventory updates use pessimistic locking.


Flow:

```
Request

      |

Lock Inventory Row

      |

Validate Quantity

      |

Update Stock

      |

Commit Transaction
```

---

# Incident Management


Drivers can report vehicle issues.


Workflow:


```
Incident Reported

        |

Vehicle OUT_OF_SERVICE

        |

Allocation Blocked
```


Prevents:

- Negative stock
- Lost updates
- Race conditions



---


## Driver Data Ownership


Driver APIs enforce ownership validation.


Drivers can only access:

- Assigned vehicles
- Own shifts
- Own delivery operations


Prevents:

- Unauthorized resource access
- Horizontal privilege escalation



---


## Shift Lifecycle Protection


Rules:


- Driver can have only one active shift
- Completed shifts cannot be modified
- Invalid transitions are rejected


Lifecycle:

```
ACTIVE

   |

COMPLETE

   |

COMPLETED

```

---

# Audit Trail


Important business events are recorded.


Examples:


- Allocation cancelled
- Delivery completed
- Incident created


Audit stores:


```
entity

action

old value

new value

performed by

timestamp
```


---

# Event Architecture


Internal event bus:


Events:


```
DeliveryCompletedEvent

IncidentCreatedEvent
```


Prepared for future integrations:

- Notifications
- Message brokers
- Analytics


---

# Error Handling


Centralized exception handling:


Examples:


```json
{
 "error_code":"VEHICLE_ALREADY_ALLOCATED",
 "message":"Vehicle already allocated"
}
```


HTTP standards:


| Code | Usage |
|-|-|
|400|Bad request|
|404|Not found|
|409|Business conflict|
|422|Validation error|


---

# Running Tests


Run all:


```bash
pytest
```


Run business tests:


```bash
pytest app/tests/business -v
```


---

# Test Coverage


| Layer | Coverage |
|-|-|
|Service Tests|Business logic|
|API Tests|Endpoints|
|Business Tests|State transitions|


Covered scenarios:


- Vehicle allocation conflicts
- Duplicate allocation prevention
- Delivery lifecycle
- Inventory update
- Inventory concurrency handling
- Incident rules
- Driver ownership validation
- Shift lifecycle validation
- Race condition testing
- Transaction rollback scenarios

---


# Documentation


Additional architecture documents:


```
docs/

├── decisions.md

└── database.md
```


Contains:

- Architecture decisions
- Trade-offs
- Future scalability


---

# Future Roadmap


Planned enhancements:


- Authentication / JWT
- Role Based Access Control
- Redis caching
- Background workers
- Kafka event streaming
- Real-time notifications
- Kubernetes deployment


---

# Status


FleetPanda backend foundation completed.

Implemented:


- Clean Architecture
- SQL Server consistency controls
- Transaction safe workflows
- Concurrent request handling
- Production error handling
- Audit logging
- Automated testing

Designed as:


```
Production Ready Modular Monolith

          |

Future Microservices Architecture
```
