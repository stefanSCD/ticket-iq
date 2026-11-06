# Pickup deadlines and no-shows — Architecture decision

Document ID: `TN-NOS-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Uncollected reservations need a defined lifecycle after the start time. No-show processing releases a booked slot and may supply operational data, but it must never race with a successful physical handover.

## Requirements and guidance

### TN-NOS-ADR-01

The pickup deadline uses elapsed time rather than a count of business opening minutes.

### TN-NOS-ADR-02

No-show expiry and checkout serialize on the reservation row.

### TN-NOS-ADR-03

The worker records its actual execution time separately from the scheduled pickup deadline.
