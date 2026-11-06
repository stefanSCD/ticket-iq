# Reservation approval — Architecture decision

Document ID: `TN-APR-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

High-value equipment uses a staff approval gate. An approval belongs to a specific request version; it is neither a standing privilege for a borrower nor permission to ignore an availability conflict.

## Requirements and guidance

### TN-APR-ADR-01

Approvals are versioned decisions stored with the reservation, not mutable boolean fields on user accounts.

### TN-APR-ADR-02

A transaction releases the interval at the same time that rejection becomes visible.

### TN-APR-ADR-03

The expiry worker uses server time and a compare-and-set transition so a completed approval cannot also expire.
