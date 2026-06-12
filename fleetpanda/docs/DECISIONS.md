# FleetPanda Architecture Decisions

## Document Information

  Item           Details
  -------------- ---------------------------------------
  Project        FleetPanda
  Architecture   Modular Monolith / Clean Architecture
  Backend        FastAPI + Python
  Database       SQL Server
  Purpose        Architecture Decision Record

------------------------------------------------------------------------

# 1. System Architecture Decision

FleetPanda follows Clean Architecture principles.

Architecture flow:

API Routes → Services → Repositories → Database

Responsibilities:

-   API layer handles HTTP contracts
-   Service layer owns business workflows
-   Repository layer owns persistence
-   Models represent database entities
-   Schemas manage request and response validation

Benefits:

-   Maintainable code
-   Testable business rules
-   Easier future scaling

------------------------------------------------------------------------

# 2. API Route Organization Decision

FleetPanda separates APIs based on responsibility.

Structure:

app/api/routes/admin

Responsibilities:

-   Vehicle management
-   Driver management
-   Allocations
-   Administrative operations

app/api/routes/driver

Responsibilities:

-   Shift handling
-   Delivery execution
-   Tracking
-   Incident reporting

This keeps operational workflows separated from administration
workflows.

------------------------------------------------------------------------

# 3. Database Decision

SQL Server is selected as the primary database.

Reasons:

-   Strong transactional consistency
-   Relational integrity
-   Enterprise reporting support

Primary domains:

-   Vehicles
-   Drivers
-   Allocations
-   Shifts
-   Orders
-   Inventory
-   Incidents
-   Audit Logs

------------------------------------------------------------------------

# 4. Repository Pattern Decision

Database operations are isolated through repositories.

Service:

-   Executes business rules
-   Controls transactions

Repository:

-   Queries data
-   Persists entities

This prevents business logic from depending directly on database
implementation.

------------------------------------------------------------------------

# 5. Vehicle Allocation Decision

Vehicle allocation follows controlled business rules.

Rules:

-   Vehicle must exist
-   Vehicle must be AVAILABLE
-   Driver must be ACTIVE
-   Duplicate active allocation is prevented

Conflict scenarios return:

409 CONFLICT

Examples:

-   VEHICLE_ALREADY_ALLOCATED
-   VEHICLE_NOT_AVAILABLE

Production consistency strategy:

-   Application validation
-   Database constraints
-   Transaction safety

------------------------------------------------------------------------

# 6. Shift Lifecycle Decision

FleetPanda manages driver shifts using a state-based workflow.

Lifecycle:

CREATED → ACTIVE → COMPLETED

Additional lifecycle support:

CREATED → CANCELLED

Cancellation supports scenarios such as:

-   Driver unavailable
-   Operational changes
-   Vehicle replacement

------------------------------------------------------------------------

# 7. Delivery Lifecycle Decision

Deliveries follow controlled state transitions.

Workflow:

ASSIGNED → IN_PROGRESS → COMPLETED

Alternative flow:

IN_PROGRESS → FAILED

Failed deliveries capture:

-   Failure reason
-   Timestamp
-   Responsible user

Inventory updates happen only after successful completion.

------------------------------------------------------------------------

# 8. Inventory Management Decision

Inventory updates are transaction controlled.

Delivery completion performs:

1.  Validate delivery state
2.  Update inventory quantity
3.  Create inventory transaction
4.  Complete delivery

All operations succeed together or rollback together.

------------------------------------------------------------------------

# 9. Incident Management Decision

Vehicle incidents control fleet availability.

Incident creation:

AVAILABLE Vehicle → Incident Reported → OUT_OF_SERVICE

Incident lifecycle roadmap:

OPEN → RESOLVED

Resolution workflow restores:

OUT_OF_SERVICE → AVAILABLE

------------------------------------------------------------------------

# 10. Audit Trail Decision

FleetPanda records important business changes.

Audit captures:

-   Entity name
-   Entity id
-   Action
-   Old value
-   New value
-   User
-   Timestamp

Examples:

Allocation:

ACTIVE → CANCELLED

Delivery:

IN_PROGRESS → COMPLETED

Vehicle:

AVAILABLE → OUT_OF_SERVICE

------------------------------------------------------------------------

# 11. Event Architecture Decision

FleetPanda uses event-driven design internally.

Events:

-   DeliveryCompletedEvent
-   IncidentCreatedEvent

Benefits:

-   Loose coupling
-   Future integration support

Future enhancement:

Transactional Outbox Pattern with message broker integration.

------------------------------------------------------------------------

# 12. Error Handling Decision

Standard API responses:

400 - Invalid request

404 - Resource not found

409 - Business conflict

422 - Schema validation

500 - Server error

------------------------------------------------------------------------

# 13. Validation Ownership Decision

Schema validation:

-   Required fields
-   Data formats
-   Type validation

Service validation:

-   Business rules
-   Workflow rules
-   State transitions

------------------------------------------------------------------------

# 14. Date And Time Decision

FleetPanda stores timestamps using UTC.

Benefits:

-   Multi-region support
-   Consistent reporting
-   Easier integrations

------------------------------------------------------------------------

# 15. Logging Decision

Application logging and audit logging have separate purposes.

Application logs:

-   Debugging
-   Monitoring
-   Failures

Audit logs:

-   Business history
-   Compliance tracking

------------------------------------------------------------------------

# 16. Testing Decision

Testing follows:

Arrange Act Assert

Test areas:

-   API tests
-   Service tests
-   Business rule tests

Each test prepares required data state independently.

------------------------------------------------------------------------

# 17. Security Roadmap

Planned capabilities:

-   JWT authentication
-   Role based access control
-   API authorization policies
-   Secure configuration handling

------------------------------------------------------------------------

# 18. Scalability Roadmap

Current architecture:

FastAPI Modular Monolith

Future evolution:

-   Redis caching
-   Background workers
-   Kafka/event streaming
-   Docker
-   Kubernetes
-   Microservice separation

Possible future services:

-   Fleet Service
-   Delivery Service
-   Inventory Service
-   Notification Service

------------------------------------------------------------------------

# Architecture Summary

FleetPanda is designed as:

-   Clean Architecture based
-   Test friendly
-   Transaction safe
-   Event ready
-   Cloud ready
-   Future microservice compatible
