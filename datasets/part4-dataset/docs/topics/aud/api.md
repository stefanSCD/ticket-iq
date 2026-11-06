# Audit records and data retention — API contract

Document ID: `TN-AUD-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The audit trail explains sensitive actions without becoming a second copy of all borrower content. Operational retention and account deletion must preserve required transaction references while limiting unnecessary personal data.

## Requirements and guidance

### TN-AUD-API-01

GET /v1/audit-events requires audit_reader for every requested lab and uses cursor pagination.

### TN-AUD-API-02

There is no API for updating the body of an existing audit event.

### TN-AUD-API-03

POST /v1/me/deletion-requests returns 409 ACTIVE_BORROWING_EXISTS when an Open loan or pending inspection blocks deletion.

### TN-AUD-API-04

A retention run records aggregate deletion counts in an operational run summary without copying deleted event bodies.
