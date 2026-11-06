# Reservation intervals and availability — Workflow

Document ID: `TN-RSV-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Borrowers reserve a physical unit for a bounded interval. Availability is computed from committed reservations and operational blocks, so the calendar and the create endpoint must agree when two people compete for the same unit.

## Requirements and guidance

### TN-RSV-WF-01

The availability calendar previews a selected unit and interval, but creation performs a fresh conflict check before commitment.

### TN-RSV-WF-02

When another borrower wins a slot during submission, preserve the losing borrower's form values and show that the slot is no longer available.

### TN-RSV-WF-03

The server rejects an endAt that is not later than startAt before evaluating availability.

### TN-RSV-WF-04

Recurring reservations are under discussion; the team has not chosen all-or-nothing versus partial series acceptance.
