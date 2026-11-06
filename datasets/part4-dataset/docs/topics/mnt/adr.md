# Maintenance and service blocks — Architecture decision

Document ID: `TN-MNT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Maintenance blocks protect equipment that is being inspected or repaired. Closing a work order is distinct from certifying a unit safe for use, and future reservations must be treated explicitly rather than disappearing from the system.

## Requirements and guidance

### TN-MNT-ADR-01

Availability combines independent reservation, maintenance, and safety-block records rather than a single editable available flag.

### TN-MNT-ADR-02

Maintenance state transitions and their availability blocks commit in one transaction.

### TN-MNT-ADR-03

Preventive due dates use the owning lab calendar date, not an assumed fixed number of UTC hours.
