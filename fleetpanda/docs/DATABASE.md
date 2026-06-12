# FleetPanda Database Design


## Overview

Database: SQL Server

The schema follows normalized relational design.


## Core Tables


### users

Stores admin and driver users.

Roles:

- ADMIN
- DRIVER



### drivers

Driver profile information.

Relationship:

users 1 → 1 drivers



### vehicles

Fleet vehicles.

Status:

- AVAILABLE
- ALLOCATED



### vehicle_allocations

Assigns vehicles to drivers per day.


Business Rule:

One vehicle can be allocated once per day.


Enforced using:

- unique constraint
- transaction handling



### shifts

Driver working period.


Relationship:

VehicleAllocation 1 → many Shifts



### orders

Delivery task.


Contains:

- destination
- delivery status



### order_items

Products and quantities.



### products

Fuel products:

- Diesel
- Petrol



### inventories

Current product stock.



### inventory_transactions

Audit history for inventory movements.



### gps_location_history

Stores every GPS update.



### vehicle_current_location

Optimized table for fleet dashboard.



## ER Flow


User

↓

Driver

↓

Vehicle Allocation

↓

Shift

↓

Order

↓

Order Items

↓

Inventory Update



Vehicle

↓

GPS History

↓

Current Location