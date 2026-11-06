# Reservation approval — API contract

Document ID: `TN-APR-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

High-value equipment uses a staff approval gate. An approval belongs to a specific request version; it is neither a standing privilege for a borrower nor permission to ignore an availability conflict.

## Requirements and guidance

### TN-APR-API-01

POST /v1/reservations/{id}/approve requires If-Match with the current request version.

### TN-APR-API-02

A stale approval attempt returns 412 VERSION_MISMATCH without changing the reservation.

### TN-APR-API-03

POST /v1/reservations/{id}/reject requires a nonempty reason of at most 500 characters.

### TN-APR-API-04

Self-approval returns 403 SELF_APPROVAL_FORBIDDEN even if the borrower also holds the required manager grant.
