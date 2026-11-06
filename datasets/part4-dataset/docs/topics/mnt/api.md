# Maintenance and service blocks — API contract

Document ID: `TN-MNT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Maintenance blocks protect equipment that is being inspected or repaired. Closing a work order is distinct from certifying a unit safe for use, and future reservations must be treated explicitly rather than disappearing from the system.

## Requirements and guidance

### TN-MNT-API-01

POST /v1/maintenance-jobs requires assetId, startAt, endAt, and reason; overlap returns 409 MAINTENANCE_BOOKING_CONFLICT.

### TN-MNT-API-02

POST /v1/maintenance-jobs/{id}/complete requires checklistResults, outcome, and technician attestation.

### TN-MNT-API-03

Completion records completedAt using server time and does not modify unrelated block records.

### TN-MNT-API-04

A job with missing required checklist results returns 422 SERVICE_CHECKLIST_INCOMPLETE.
