# API Specification — Audit evidence bundles

**Project:** LedgerCloud  
**Feature:** audit-evidence  
**Status:** Active  

## Operations

`POST /v1/audit-evidence` creates a audit evidence bundles operation. `GET /v1/audit-evidence/{id}` retrieves the current state of a known operation. `GET /v1/audit-evidence?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/audit-evidence HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-10
X-Correlation-ID: correlation-001
Content-Type: application/json

{"targetId":"ITEM-001","intent":"execute"}
```
The example is illustrative: fields and validation must be reconciled with the specific client and user-facing workflow before deployment.

## Response shape

On accepted asynchronous processing, respond `202` with `{"operationId":"...","status":"pending","correlationId":"..."}`. On synchronous completion respond `200` and the authoritative resulting state. Errors use `{"code":"...","message":"...","correlationId":"..."}`.

## Error classes

`400` invalid input; `401` missing authentication; `403` insufficient access; `404` an unknown authorized resource; `409` state conflict; `429` throttling; `503` transient provider unavailability. A timeout does not prove that no operation happened. Clients should query state before creating new requests.

## Compatibility checks

Contract tests assert stable error codes, authorization, request de-duplication and correlation fields. New optional response fields are allowed. Clients must not depend on undocumented response fields. This interface contract does not define missing product thresholds or timing decisions.
