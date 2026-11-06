# Reservation intervals and availability — Staff FAQ

Document ID: `TN-RSV-FAQ`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Borrowers reserve a physical unit for a bounded interval. Availability is computed from committed reservations and operational blocks, so the calendar and the create endpoint must agree when two people compete for the same unit.

## Requirements and guidance

### TN-RSV-FAQ-01

Borrowers may reserve equipment for up to 96 hours in one ordinary reservation.

### TN-RSV-FAQ-02

A calendar preview is advisory; the submission result is authoritative when simultaneous requests compete.

### TN-RSV-FAQ-03

Adjacent bookings are allowed because the ending instant belongs only to the later interval.
