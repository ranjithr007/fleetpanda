# FleetPanda - Architecture & Technical Decisions

## Document Information

| Item | Details |
|---|---|
| Project | FleetPanda |
| Type | Fleet Management Platform |
| Architecture | Clean Architecture |
| Backend | FastAPI |
| Database | SQL Server |
| Language | Python |
| Document Type | Architecture Decision Record |
| Status | Active |

---

# 1. Architecture Decision

## Decision

FleetPanda follows Clean Architecture with clear separation between:

```
API Layer
    |
Service Layer
    |
Repository Layer
    |
Database Layer
```

## Reason

To keep:

- Business logic independent
- Database access isolated
- APIs lightweight
- Testing easier
- Future migration possible


## Final Structure


```
app

├── api
│   └── routes
│       ├── admin
│       └── driver
│
├── services
│
├── repositories
│
├── models
│
├── schemas
│
├── events
│
├── database
│
└── tests
```

---

# 2. Route Separation Decision

## Decision

Separate APIs based on user responsibility.

```
api/routes/admin
api/routes/driver
```

## Admin Responsibilities

- Vehicle management
- Driver management
- Vehicle allocation
- Reports
- Monitoring

## Driver Responsibilities

- Shift operations
- Deliveries
- Location tracking
- Incident reporting


## Reason

Matches real FleetPanda business workflow.

Avoids mixing operational and management APIs.

---

# 3. Database Decision

## Selected

SQL Server

## Reason

Fleet systems require:

- Strong consistency
- Transactions
- Relational integrity
- Reporting support


Core entities:

```
vehicles
drivers
vehicle_allocations
driver_shifts
orders
order_items
inventory
inventory_transactions
vehicle_incidents
audit_logs
```

---

# 4. Repository Pattern Decision

## Decision

All database access goes through repositories.

Example:

```
AllocationService

        |
        v

AllocationRepository

        |
        v

SQL Server
```


## Reason

Service layer should not know SQL details.

Benefits:

- Easy unit testing
- Replace database later
- Cleaner business logic

---

# 5. Vehicle Allocation Decision


## Business Rules


### Vehicle Double Allocation

Decision:

A vehicle cannot have multiple active allocations.


Flow:

```
Request Allocation

        |

Check Existing Allocation

        |

Exists?

 YES ---> 409 Conflict

 NO

        |

Create Allocation
```


HTTP Response:

```
409 VEHICLE_ALREADY_ALLOCATED
```

---

## Out Of Service Vehicle Rule


Decision:

Vehicles with incidents cannot be allocated.


Statuses:

```
AVAILABLE
ALLOCATED
OUT_OF_SERVICE
```

Rule:

```
OUT_OF_SERVICE
        |
        X
 Allocation blocked
```


Response:

```
409 VEHICLE_NOT_AVAILABLE
```

---

# 6. Shift Lifecycle Decision


Driver shift follows state machine.


```
CREATED

   |

START

   |

ACTIVE

   |

END

   |

COMPLETED
```


Invalid transitions return:

```
409 INVALID_SHIFT_STATE
```

---

# 7. Delivery Workflow Decision


Delivery follows controlled lifecycle.


```
ASSIGNED

    |

Driver Start

    |

IN_PROGRESS

    |

Complete Delivery

    |

COMPLETED
```


Rules:

Cannot complete:

```
ASSIGNED delivery
COMPLETED delivery
FAILED delivery
```


Response:

```
409 ORDER_NOT_STARTED
409 ORDER_ALREADY_COMPLETED
```

---

# 8. Inventory Update Decision


## Decision

Inventory updates only after successful delivery completion.


Flow:

```
Delivery Completed Event

        |

Increase Inventory Quantity

        |

Create Inventory Transaction
```


Benefits:

- Auditability
- Prevent wrong stock updates
- Transaction history

---

# 9. Incident Management Decision


## Decision

Vehicle incidents immediately affect vehicle availability.


Flow:


```
Driver Reports Incident


Create Incident

        |

Vehicle Status

AVAILABLE
        |
        v
OUT_OF_SERVICE

        |

Block Future Allocation
```


Rules:

Only one OPEN incident allowed per vehicle.


Conflict:

```
409 INCIDENT_ALREADY_OPEN
```

---

# 10. Audit Logging Decision


## Decision

Every important state change creates audit record.


Table:

audit_logs


Stores:

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


Vehicle Allocation:

```
ACTIVE -> CANCELLED
```


Delivery:

```
IN_PROGRESS -> COMPLETED
```


Vehicle:

```
AVAILABLE -> OUT_OF_SERVICE
```


## Rule

Entity must be saved before audit creation.


Correct:

```
Create Entity

Generate ID

Create Audit
```


---

# 11. Event Driven Decision


## Decision

Use internal event bus.


Events:


```
DeliveryCompletedEvent

IncidentCreatedEvent
```


Benefits:

- Loose coupling
- Easy notification integration
- Future Kafka/RabbitMQ migration


Future:


```
FastAPI

 |

Event Bus

 |

Kafka

 |

Notification Service
```


---

# 12. Error Handling Decision


Standard API errors:


| Scenario | Code |
|-|-|
| Validation failure | 400 |
| Missing Entity | 404 |
| Business conflict | 409 |
| Schema error | 422 |
| Server failure | 500 |


Examples:

```
VEHICLE_ALREADY_ALLOCATED

ORDER_ALREADY_COMPLETED

INCIDENT_ALREADY_OPEN
```

---

# 13. Testing Decision


Testing structure:


```
tests

├── business
├── services
├── api
```


Business tests validate:

- Allocation rules
- Delivery rules
- Inventory rules
- Incident rules


Pattern:


```
Arrange

Act

Assert
```


Each test prepares its own data.

---

# 14. Scalability Decisions


Current:

```
FastAPI Monolith

        |

Clean Modules
```


Future:


```
API Gateway

     |

Microservices


Fleet Service

Delivery Service

Inventory Service

Notification Service
```


---

# 15. Future Enhancements


Planned:


- JWT Authentication
- Role Based Access Control
- Redis caching
- Background jobs
- Real-time driver tracking
- WebSocket notifications
- Kafka event streaming
- Docker deployment
- Kubernetes support
- CI/CD pipeline


---

# Final Architecture Summary


FleetPanda is designed as:

✔ Clean Architecture  
✔ Domain Driven Structure  
✔ Testable Services  
✔ Event Ready  
✔ Cloud Ready  
✔ Microservice Ready  


```
Clients

  |

FastAPI

  |

Services

  |

Repositories

  |

SQL Server
```


```
Events
  |
  +-- Notifications
  |
  +-- Analytics
  |
  +-- Integrations
```


Status:

Production Architecture Foundation Completed
