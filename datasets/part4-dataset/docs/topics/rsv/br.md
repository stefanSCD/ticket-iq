# Reservation intervals and availability — Business rules

Document ID: `TN-RSV-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Borrowers reserve a physical unit for a bounded interval. Availability is computed from committed reservations and operational blocks, so the calendar and the create endpoint must agree when two people compete for the same unit.

## Requirements and guidance

### TN-RSV-BR-01

Reservation intervals are half-open: [startAt, endAt); one booking may start exactly when the preceding booking ends.

### TN-RSV-BR-02

Confirmed and AwaitingApproval reservations block their assigned unit; Draft and Cancelled reservations do not block availability.

### TN-RSV-BR-03

A normal reservation must last at least 30 minutes and no more than 72 hours.

### TN-RSV-BR-04

Reservation timestamps are stored as UTC instants and displayed in the owning lab time zone.

### TN-RSV-BR-05

A unit cannot be reserved across an active maintenance block.
