# Reservation approval — Workflow

Document ID: `TN-APR-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

High-value equipment uses a staff approval gate. An approval belongs to a specific request version; it is neither a standing privilege for a borrower nor permission to ignore an availability conflict.

## Requirements and guidance

### TN-APR-WF-01

The approval inbox lists the borrower, purpose, asset, requested interval, and request version for the manager's labs.

### TN-APR-WF-02

Before approving, the server rechecks the actor's grant and verifies that the request version has not changed.

### TN-APR-WF-03

Approval and rejection both append an audit event with the decision maker and the request version.

### TN-APR-WF-04

Delegation to a temporary approver is being explored; delegation scope and expiry have not been agreed.
