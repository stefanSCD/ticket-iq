# Reservation intervals and availability — Architecture decision

Document ID: `TN-RSV-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Borrowers reserve a physical unit for a bounded interval. Availability is computed from committed reservations and operational blocks, so the calendar and the create endpoint must agree when two people compete for the same unit.

## Requirements and guidance

### TN-RSV-ADR-01

PostgreSQL exclusion constraints protect unit intervals from concurrent overlapping writes.

### TN-RSV-ADR-02

The application expands no implicit cleaning buffer around an ordinary reservation.

### TN-RSV-ADR-03

A reservation owns one assigned unit; substitution is an explicit operation rather than a change to the model name.
