# FleetPanda Fleet Tracking Platform

Scaled-down real-time fleet, driver, and delivery tracking backend.


## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQL Server
- Alembic
- Pytest
- Docker


## Architecture


Client

↓

FastAPI Routes

↓

Application Services

↓

Repositories

↓

SQL Server



## Features


### Admin

- Manage vehicles
- Manage drivers
- Vehicle allocation
- Fleet status tracking


### Driver

- View deliveries
- Start / end shift
- Send GPS updates
- Complete or fail delivery


## Business Rules


### Vehicle Allocation

One vehicle can only be assigned to one driver per day.

Handled using:

- validation
- database constraint
- transaction handling


### Inventory

Delivery completion:

- updates order
- increases inventory
- creates transaction record


### GPS

Location updates require active shift.


## Run Locally


Create environment:

```bash
python -m venv venv