# Pickup deadlines and no-shows — Workflow

Document ID: `TN-NOS-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Uncollected reservations need a defined lifecycle after the start time. No-show processing releases a booked slot and may supply operational data, but it must never race with a successful physical handover.

## Requirements and guidance

### TN-NOS-WF-01

The pickup screen shows the scheduled start and current pickup deadline in the owning lab time zone.

### TN-NOS-WF-02

The expiry worker rechecks reservation state under the same lock used for checkout.

### TN-NOS-WF-03

The no-show event can trigger waiting-list processing after the expiry transaction commits.

### TN-NOS-WF-04

Excused no-shows and their effect on future borrowing are not yet governed by an approved policy.
