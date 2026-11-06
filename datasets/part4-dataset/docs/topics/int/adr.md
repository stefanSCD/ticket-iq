# External API and webhook delivery — Architecture decision

Document ID: `TN-INT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A course scheduler integrates with ToolNest through a versioned REST API and event subscriptions. Integrations receive lab-scoped service credentials and must tolerate retries, duplicate webhook deliveries, and stale updates.

## Requirements and guidance

### TN-INT-ADR-01

The public integration API uses the /v1 prefix; internal database tables are not an integration contract.

### TN-INT-ADR-02

Domain events are published from an outbox after the corresponding database transaction commits.

### TN-INT-ADR-03

Idempotency scope includes authenticated actor and route so two different integrations cannot read each other's stored responses by choosing the same key.
