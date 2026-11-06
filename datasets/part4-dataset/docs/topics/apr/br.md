# Reservation approval — Business rules

Document ID: `TN-APR-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

High-value equipment uses a staff approval gate. An approval belongs to a specific request version; it is neither a standing privilege for a borrower nor permission to ignore an availability conflict.

## Requirements and guidance

### TN-APR-BR-01

Equipment with requiresApproval=true creates an AwaitingApproval reservation and blocks its assigned interval while waiting.

### TN-APR-BR-02

Approval requires a lab_manager grant for the owning lab; a borrower cannot approve their own reservation.

### TN-APR-BR-03

Rejection records a mandatory reason, transitions the reservation to Rejected, and releases its interval.

### TN-APR-BR-04

Changing the assigned asset or reservation interval invalidates an existing approval and returns the request to AwaitingApproval.

### TN-APR-BR-05

An approval request expires 24 hours after creation if no decision has been recorded.
