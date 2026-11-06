# Reservation intervals and availability — API contract

Document ID: `TN-RSV-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Borrowers reserve a physical unit for a bounded interval. Availability is computed from committed reservations and operational blocks, so the calendar and the create endpoint must agree when two people compete for the same unit.

## Requirements and guidance

### TN-RSV-API-01

POST /v1/reservations requires assetId, startAt, endAt, and purpose; an overlap returns 409 RESERVATION_CONFLICT.

### TN-RSV-API-02

GET /v1/availability accepts explicit UTC offsets in both interval parameters and returns blocking intervals in UTC.

### TN-RSV-API-03

A successful create returns 201 with the reservation ID and its initial state; clients must not infer success from an availability preview.

### TN-RSV-API-04

Reservation conflicts are enforced inside the same database transaction that creates the reservation.
