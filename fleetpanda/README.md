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

# Database Setup


Configure SQL Server connection.

Run migrations:


```bash
alembic upgrade head
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
- Delivery lifecycle
- Inventory update
- Incident rules
- Shift validations


---

# Documentation


Additional architecture documents:


```
docs/

├── decisions.md

└── diagrams/
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


Designed as:


```
Production Ready Modular Monolith

          |

Future Microservices Architecture
```
