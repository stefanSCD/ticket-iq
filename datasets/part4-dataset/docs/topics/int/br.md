# External API and webhook delivery — Business rules

Document ID: `TN-INT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A course scheduler integrates with ToolNest through a versioned REST API and event subscriptions. Integrations receive lab-scoped service credentials and must tolerate retries, duplicate webhook deliveries, and stale updates.

## Requirements and guidance

### TN-INT-BR-01

A service credential is scoped to explicit labs and API operations; it never inherits the grants of the staff member who created it.

### TN-INT-BR-02

Webhook payloads contain eventId, eventType, occurredAt, resourceId, and labId, without borrower names or email addresses.

### TN-INT-BR-03

Webhook delivery is at least once; consumers must deduplicate using eventId.

### TN-INT-BR-04

Requests that reuse an Idempotency-Key with a different payload in the same actor-and-route scope return 409 IDEMPOTENCY_MISMATCH.

### TN-INT-BR-05

REST idempotency records are retained for 24 elapsed hours after the original request completes.
