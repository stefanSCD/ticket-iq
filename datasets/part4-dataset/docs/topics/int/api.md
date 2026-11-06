# External API and webhook delivery — API contract

Document ID: `TN-INT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A course scheduler integrates with ToolNest through a versioned REST API and event subscriptions. Integrations receive lab-scoped service credentials and must tolerate retries, duplicate webhook deliveries, and stale updates.

## Requirements and guidance

### TN-INT-API-01

Webhook requests include X-ToolNest-Event-Id, X-ToolNest-Timestamp, and X-ToolNest-Signature headers.

### TN-INT-API-02

A versioned mutation with a stale If-Match returns 412 VERSION_MISMATCH rather than overwriting a newer resource.

### TN-INT-API-03

A successful idempotent retry within the retention window returns the original response status and body.

### TN-INT-API-04

Revoking a service credential rejects subsequent requests using that credential without waiting for an application restart.
