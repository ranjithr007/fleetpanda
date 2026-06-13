# FleetPanda Architecture Decisions

## Overview

FleetPanda is designed as a production-ready modular monolith using Clean Architecture principles.

The architecture focuses on:

* Maintainability
* Business workflow isolation
* Data consistency
* Testability
* Future microservice migration

---

# System Architecture


```text
                         +------------------+
                         |                  |
                         |   Client Apps    |
                         |                  |
                         | Web / Mobile UI  |
                         +--------+---------+
                                  |
                                  |
                                  v
                    +-------------+--------------+
                    |                            |
                    |        FastAPI API         |
                    |                            |
                    +-------------+--------------+
                                  |
                                  |
                +-----------------+----------------+
                |                                  |
                v                                  v

        +---------------+                +----------------+
        | Admin Routes  |                | Driver Routes  |
        +-------+-------+                +--------+-------+
                |                                 |
                +---------------+-----------------+
                                |
                                v

                    +-----------+------------+
                    |                        |
                    |    Service Layer       |
                    |                        |
                    +-----------+------------+
                                |
                                v

                    +-----------+------------+
                    |                        |
                    |  Repository Layer      |
                    |                        |
                    +-----------+------------+
                                |
                                v

                    +-----------+------------+
                    |                        |
                    | SQLAlchemy ORM         |
                    |                        |
                    +-----------+------------+
                                |
                                v

                    +-----------+------------+
                    |                        |
                    | SQL Server Database    |
                    |                        |
                    +------------------------+

```

Layer responsibilities are clearly separated.

---

# ADR-001: Backend Framework Selection

## Decision

Use FastAPI as the backend framework.


---

## 2. Backend Module Architecture

Add:

````md
# Backend Module Architecture


```text

app/


 api
  |
  +-- routes
       |
       +-- admin
       |
       +-- driver


          |
          v


      Services
          |
          |
          v

    Repositories

          |
          |
          v

       Models

          |
          |
          v

     SQL Server



Supporting Modules:


core
 |
 +-- config
 +-- exceptions


schemas
 |
 +-- request validation
 +-- response contracts


events
 |
 +-- domain events


database
 |
 +-- session
 +-- migrations

 ```
 ````
## Reason

FastAPI provides:

* High performance API execution
* Dependency injection support
* Automatic OpenAPI documentation
* Strong request validation using Pydantic
* Async capability for future scaling

---

# ADR-002: Clean Architecture Pattern

## Decision

Separate application into independent layers.

Architecture:

```
API Routes

    |

Services

    |

Repositories

    |

Database Models
```

## Reason

Benefits:

* Business logic remains independent
* Easier testing
* Easier maintenance
* Database implementation can change without affecting APIs

---

# ADR-003: API Route Separation

## Decision

Separate APIs based on user responsibility.

Current structure:

```
api/

 └── routes/

      ├── admin/

      └── driver/
```

## Reason

Admin and driver workflows have different security and business requirements.

Admin owns:

* Vehicle management
* Driver management
* Allocation control
* Fleet monitoring

Driver owns:

* Deliveries
* Shifts
* Tracking
* Incident reporting

Benefits:

* Clear ownership
* Better authorization control
* Easier future scaling

---

# ADR-004: Repository Pattern

## Decision

Use repository layer for database access.

Flow:

```
Service

   |

Repository

   |

SQLAlchemy

   |

Database
```

## Reason

Avoid database logic inside APIs.

Benefits:

* Cleaner services
* Easier mocking/testing
* Centralized database operations

---

# ADR-005: Transaction Management

## Decision

Manage transaction boundaries at service layer.

## Reason

Business workflows update multiple resources.

Example:

Cancel Allocation:

```
Start Transaction

        |

Update Allocation

        |

Update Vehicle Status

        |

Create Audit Log

        |

Commit
```

Failure:

```
Exception

   |

Rollback
```

Guarantees:

* Atomic updates
* Data consistency
* No partial changes

---

# ADR-006: Database First Consistency

## Decision

Important business rules are enforced in SQL Server.

Implemented:

* Foreign keys
* Unique constraints
* Check constraints

## Reason

Application validation alone is not enough during concurrent requests.

Database remains the final protection layer.

---

# ADR-007: Inventory Locking Strategy

## Decision

Use pessimistic locking for inventory operations.

Flow:

```
Transaction Start

        |

Lock Inventory Row

        |

Validate Quantity

        |

Update Inventory

        |

Commit
```

## Reason

Inventory accuracy is more important than parallel update speed.

Prevents:

* Race conditions
* Negative inventory
* Lost updates

---

# ADR-008: Driver Ownership Security

## Decision

Validate resource ownership before driver operations.

Example:

Driver API queries include ownership filtering:

```
driver_id = authenticated_driver
```

## Reason

Prevents:

* Unauthorized access
* Cross-driver data visibility
* Horizontal privilege escalation

---

# ADR-009: Shift Lifecycle Management

## Decision

Control shift state transitions through business rules.

Lifecycle:

```
ACTIVE

   |

COMPLETE

   |

COMPLETED
```

Rules:

* One active shift per driver
* Completed shifts cannot change
* Invalid transitions blocked

---

# ADR-010: Event Based Extension

## Decision

Use internal domain events.

## Event Architecture


```text

Business Service


       |

       v


Domain Event


       |


+------+-------+

|              |

v              v


Audit       Future Queue


               |

               v


          Kafka / Worker

```


## Reason

Keeps core workflow independent from integrations.

Future extensions:

* Kafka
* Notifications
* Analytics
* External systems

---

# ADR-011: Testing Strategy

## Decision

Test production failure scenarios.

Coverage:

* Unit tests
* API tests
* Business workflow tests
* Database constraint tests
* Concurrency tests

Validated scenarios:

* Duplicate vehicle allocation
* Inventory race conditions
* Shift conflicts
* Transaction rollback
* Ownership validation

---

# ADR-012: Deployment Direction

## Decision

Keep modular monolith first.

Reason:

Current architecture supports clean extraction into microservices later.

Future:

```
Fleet Service

Driver Service

Inventory Service

Notification Service
```

Communication:

```
REST

+

Message Broker
```

---
# ADR-013 Future Microservice Architecture


```text

              API Gateway

                   |

 -------------------------------------------------

 |                 |              |              |


Fleet Service  Driver Service Inventory Service Notification Service


      |              |             |              |


      DB             DB            DB             DB


                   |

              Event Broker

                   |

                 Kafka

```

---

# Architecture Summary

FleetPanda backend provides:

✔ Clean Architecture

✔ Service isolation

✔ Repository abstraction

✔ SQL Server consistency

✔ Transaction safety

✔ Concurrent request protection

✔ Secure ownership boundaries

✔ Event driven scalability

Designed as:

```
Production Ready Modular Monolith

              |

Future Microservice Platform
```
