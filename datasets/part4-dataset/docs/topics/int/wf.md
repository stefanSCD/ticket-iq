# External API and webhook delivery — Workflow

Document ID: `TN-INT-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A course scheduler integrates with ToolNest through a versioned REST API and event subscriptions. Integrations receive lab-scoped service credentials and must tolerate retries, duplicate webhook deliveries, and stale updates.

## Requirements and guidance

### TN-INT-WF-01

Staff registering a webhook choose allowed event types and labs within their integration_admin grants.

### TN-INT-WF-02

A failed webhook delivery appears in the integration delivery log with an attempt timestamp and response status.

### TN-INT-WF-03

Webhook signatures use HMAC-SHA256 over the timestamp header, a period, and the raw request body; receivers must preserve the raw bytes.

### TN-INT-WF-04

Webhook replay authorization and the maximum historical replay range remain undecided.
