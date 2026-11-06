# Maintenance and service blocks — Business rules

Document ID: `TN-MNT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Maintenance blocks protect equipment that is being inspected or repaired. Closing a work order is distinct from certifying a unit safe for use, and future reservations must be treated explicitly rather than disappearing from the system.

## Requirements and guidance

### TN-MNT-BR-01

A Scheduled or InProgress maintenance job blocks new reservations for its asset during the maintenance interval.

### TN-MNT-BR-02

Creating maintenance that overlaps a confirmed reservation returns a conflict and requires staff to resolve the booking separately.

### TN-MNT-BR-03

A maintenance job cannot be completed until its service checklist is recorded and an authorized technician signs the result.

### TN-MNT-BR-04

Completing maintenance clears only that job's block; independent safety incidents and retirement still prevent availability.

### TN-MNT-BR-05

A preventive maintenance task becomes due every 90 calendar days after the previous completed preventive service.
