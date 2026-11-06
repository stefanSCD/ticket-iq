# Pickup deadlines and no-shows — API contract

Document ID: `TN-NOS-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Uncollected reservations need a defined lifecycle after the start time. No-show processing releases a booked slot and may supply operational data, but it must never race with a successful physical handover.

## Requirements and guidance

### TN-NOS-API-01

GET /v1/reservations/{id} returns pickupDeadlineAt as a UTC instant alongside the reservation state.

### TN-NOS-API-02

The internal no-show worker ignores Draft, AwaitingApproval, Cancelled, and Collected reservations.

### TN-NOS-API-03

Reprocessing an expired reservation does not append a second expiry event.

### TN-NOS-API-04

A request that loses a race to a completed checkout returns the current Collected state without releasing the loan's occupancy.
