# External API and webhook delivery — Staff FAQ

Document ID: `TN-INT-FAQ`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A course scheduler integrates with ToolNest through a versioned REST API and event subscriptions. Integrations receive lab-scoped service credentials and must tolerate retries, duplicate webhook deliveries, and stale updates.

## Requirements and guidance

### TN-INT-FAQ-01

A REST Idempotency-Key can be retried for 48 elapsed hours after the original request completes.

### TN-INT-FAQ-02

A consumer may receive the same webhook event more than once and should use eventId to deduplicate.

### TN-INT-FAQ-03

A service token remains restricted to its configured labs even if its creator later receives access to more labs.
