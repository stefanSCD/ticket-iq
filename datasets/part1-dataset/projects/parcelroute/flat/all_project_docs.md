# ParcelRoute — Combined Documentation

All documents below are byte-identical in content to their corresponding structured files. Do not index both representations together.

---

## Document 001

# ParcelRoute — Project overview and glossary

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Scope

ParcelRoute coordinates pickup, tracking, rerouting and delivery evidence for regional carriers. This project is fictional. It has 10 independent feature areas and a set of shared cross-cutting constraints.

## Terms

A request is a user-intended operation. An event records an observed transition. A policy is an approved product decision. A ticket describes work; it does not override a policy unless approved.

## Roles

sender, recipient, dispatcher, delivery agent. Each role is limited to the records and tenants it is authorized to act upon.

## Interpretation

Product policy lives in business rules; functional specifications define user flows; API contracts define network semantics; ADRs explain engineering choices; FAQ is support-facing context. Similarity to a feature does not automatically answer a ticket question.


---

## Document 002

# ParcelRoute — Security and privacy boundaries

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Identity

Bearer tokens identify principals. Services validate token status, tenant scope and record ownership before responding with sensitive state.

## Minimization

Requests and logs should contain stable references rather than passwords, personal attachments or credentials. Synthetic examples in this dataset do not represent real users.

## Audit

Mutations require event correlation and actor attribution. Auditability does not specify a feature-specific retention duration.

## Controls

Duplicate operations must be idempotent, and cross-tenant record access must be rejected before reading protected data.


---

## Document 003

# ParcelRoute — Integration catalogue

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Dependencies

carrier scanner, geocoding provider, email service, parcel locker network. Each provider may fail, delay, duplicate or time out. A timeout does not prove the provider failed to accept an operation.

## Reconciliation

A stable operation ID links local changes to provider acknowledgements. Failed side effects can be reconciled without silently overwriting authoritative data.

## Product choices

A provider offering an API does not make that option a default business requirement. The product owner must explicitly approve user-visible behavior.


---

## Document 004

# ParcelRoute — Quality and observability

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Quality baseline

Event ingestion is at-least-once with de-duplication; shipment location visibility is access-scoped.

## Observability

Services expose correlation IDs, stable error classes, retry queue health and pending-versus-terminal outcomes. Private payloads are redacted.

## Acceptance

Project-wide availability targets do not set feature-specific reminder deadlines, payment thresholds, retry ceilings or retention periods. QA must ask if a product-specific boundary remains undocumented.


---

## Document 005

# ParcelRoute — Support and incident response

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Initial triage

Capture feature key, sanitized error category, request identifier, event time and last confirmed state. Never use a duplicate irreversible operation merely to inspect whether an earlier one succeeded.

## Research order

Read the ticket, business rules, functional specification and API contract. Consult the FAQ and ADR for implementation context.

## Contradictions

If two active sources disagree, preserve both citations and escalate to the product owner. A support agent cannot silently replace an approved rule.

## Follow-up

Record resolution as a new dated decision, not an undocumented implementation default.


---

## Document 006

# ParcelRoute — Requirements decision governance

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Source hierarchy

Approved business rules and functional specifications define intended product behavior. API specifications define interfaces, and ADRs define architecture. FAQ pages describe operational experience.

## Authority

Two active policy sources can genuinely contradict one another; authority or creation date alone must not be used as a guess for missing product approval.

## Ticket changes

The author or product owner approves clarification-derived acceptance criteria before the underlying Jira ticket is updated. Changes require source IDs and a rationale.


---

## Document 007

# ParcelRoute — Acceptance testing patterns

**Status:** Active

## About

ParcelRoute: Parcel delivery operations and shipment tracking. The page is authoritative only in the synthetic project context.

## Testable criteria

Express observable results as Given-When-Then conditions. Cover authorized success, rejected permissions, duplicate requests and external dependencies failing.

## Traceability

Added product constraints must reference an approved document excerpt or a confirmed stakeholder answer. An SLM must not convert an architectural preference into a business rule.

## Missing requirements

If timing, thresholds, payment rules or scope are unspecified, identify the smallest consequential decision and ask one focused question rather than inventing a default.


---

## Document 008

# Functional Specification — Pickup scheduling

**Project:** ParcelRoute  
**Feature:** pickup-booking  
**Status:** Active  

## Business purpose

ParcelRoute uses pickup scheduling to allow a sender to schedule a pickup for a parcel. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated sender opens a record and chooses to schedule a pickup for a parcel.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed sender receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The pickup scheduling action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for pickup scheduling. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 009

# Business Rules — Pickup scheduling

**Project:** ParcelRoute  
**Feature:** pickup-booking  
**Status:** Active  

## Approved feature policy

A pickup may be confirmed only for an address within an enabled service area.

## Eligible actors

Only authenticated sender identities with permission on the relevant record may initiate pickup scheduling operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted pickup scheduling request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Pickup scheduling must be retained for 30 days after closure.

## Positive scenario

Given a sender with record access, when the user requests to schedule a pickup for a parcel, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for pickup scheduling. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 010

# API Specification — Pickup scheduling

**Project:** ParcelRoute  
**Feature:** pickup-booking  
**Status:** Active  

## Operations

`POST /v1/pickups` creates a pickup scheduling operation. `GET /v1/pickups/{id}` retrieves the current state of a known operation. `GET /v1/pickups?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/pickups HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-1
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


---

## Document 011

# FAQ and Support — Pickup scheduling

**Project:** ParcelRoute  
**Feature:** pickup-booking  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible sender to schedule a pickup for a parcel. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Routing provider errors may be retried before the pickup is confirmed. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Pickup scheduling must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the pickup-booking feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 012

# ADR-001 — Transactional Outbox: Pickup scheduling

**Project:** ParcelRoute  
**Feature:** pickup-booking  
**Status:** Active  
**Decision status:** Accepted  

## Context

The pickup scheduling workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a sender attempts to schedule a pickup for a parcel.

## Decision

Record the domain mutation and an outbox entry in one transaction, then deliver external side effects asynchronously.

## Alternatives

The team considered a simple synchronous design. It was rejected because: A synchronous provider call inside the transaction risks long locks and partial failure ambiguity. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for pickup scheduling. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 013

# Functional Specification — Delivery address validation

**Project:** ParcelRoute  
**Feature:** address-check  
**Status:** Active  

## Business purpose

ParcelRoute uses delivery address validation to allow a sender to validate a delivery address before label purchase. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated sender opens a record and chooses to validate a delivery address before label purchase.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed sender receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The delivery address validation action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for delivery address validation. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 014

# Business Rules — Delivery address validation

**Project:** ParcelRoute  
**Feature:** address-check  
**Status:** Active  

## Approved feature policy

An address that fails validation cannot be automatically marked as verified.

## Eligible actors

Only authenticated sender identities with permission on the relevant record may initiate delivery address validation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted delivery address validation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Delivery address validation remain valid for 12 hours after the first request.

## Positive scenario

Given a sender with record access, when the user requests to validate a delivery address before label purchase, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for delivery address validation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 015

# API Specification — Delivery address validation

**Project:** ParcelRoute  
**Feature:** address-check  
**Status:** Active  

## Operations

`POST /v1/address-validations` creates a delivery address validation operation. `GET /v1/address-validations/{id}` retrieves the current state of a known operation. `GET /v1/address-validations?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/address-validations HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-2
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


---

## Document 016

# FAQ and Support — Delivery address validation

**Project:** ParcelRoute  
**Feature:** address-check  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible sender to validate a delivery address before label purchase. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Transient geocoding failures return a pending validation state. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Deduplication keys for Delivery address validation remain valid for 48 hours after the first request.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the address-check feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 017

# ADR-002 — Idempotent Command Handler: Delivery address validation

**Project:** ParcelRoute  
**Feature:** address-check  
**Status:** Active  
**Decision status:** Accepted  

## Context

The delivery address validation workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a sender attempts to validate a delivery address before label purchase.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for delivery address validation. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 018

# Functional Specification — Shipment tracking events

**Project:** ParcelRoute  
**Feature:** tracking  
**Status:** Active  

## Business purpose

ParcelRoute uses shipment tracking events to allow a recipient to see the latest tracking status of a parcel. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated recipient opens a record and chooses to see the latest tracking status of a parcel.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed recipient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The shipment tracking events action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for shipment tracking events. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 019

# Business Rules — Shipment tracking events

**Project:** ParcelRoute  
**Feature:** tracking  
**Status:** Active  

## Approved feature policy

Scanner events are de-duplicated using their carrier event identifier.

## Eligible actors

Only authenticated recipient identities with permission on the relevant record may initiate shipment tracking events operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted shipment tracking events request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Shipment tracking events workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a recipient with record access, when the user requests to see the latest tracking status of a parcel, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for shipment tracking events. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 020

# API Specification — Shipment tracking events

**Project:** ParcelRoute  
**Feature:** tracking  
**Status:** Active  

## Operations

`POST /v1/tracking-events` creates a shipment tracking events operation. `GET /v1/tracking-events/{id}` retrieves the current state of a known operation. `GET /v1/tracking-events?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/tracking-events HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-3
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


---

## Document 021

# FAQ and Support — Shipment tracking events

**Project:** ParcelRoute  
**Feature:** tracking  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible recipient to see the latest tracking status of a parcel. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Out-of-order events are stored with their occurrence time and do not overwrite newer milestones. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Shipment tracking events workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the tracking feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 022

# ADR-003 — Append-only Operation History: Shipment tracking events

**Project:** ParcelRoute  
**Feature:** tracking  
**Status:** Active  
**Decision status:** Accepted  

## Context

The shipment tracking events workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a recipient attempts to see the latest tracking status of a parcel.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for shipment tracking events. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 023

# Functional Specification — Proof of delivery

**Project:** ParcelRoute  
**Feature:** proof-of-delivery  
**Status:** Active  

## Business purpose

ParcelRoute uses proof of delivery to allow a delivery agent to record evidence that a shipment was delivered. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated delivery agent opens a record and chooses to record evidence that a shipment was delivered.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed delivery agent receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The proof of delivery action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for proof of delivery. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 024

# Business Rules — Proof of delivery

**Project:** ParcelRoute  
**Feature:** proof-of-delivery  
**Status:** Active  

## Approved feature policy

Final delivery requires at least one proof artifact: recipient signature or delivery photo.

## Eligible actors

Only authenticated delivery agent identities with permission on the relevant record may initiate proof of delivery operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted proof of delivery request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Proof of delivery remain downloadable for 7 days.

## Positive scenario

Given a delivery agent with record access, when the user requests to record evidence that a shipment was delivered, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for proof of delivery. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 025

# API Specification — Proof of delivery

**Project:** ParcelRoute  
**Feature:** proof-of-delivery  
**Status:** Active  

## Operations

`POST /v1/proof-of-delivery` creates a proof of delivery operation. `GET /v1/proof-of-delivery/{id}` retrieves the current state of a known operation. `GET /v1/proof-of-delivery?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/proof-of-delivery HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-4
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


---

## Document 026

# FAQ and Support — Proof of delivery

**Project:** ParcelRoute  
**Feature:** proof-of-delivery  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible delivery agent to record evidence that a shipment was delivered. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Proof artifacts are staged locally and synchronized after connectivity returns. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational audit extracts for Proof of delivery remain downloadable for 14 days.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the proof-of-delivery feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 027

# ADR-004 — Authorization at API Boundary: Proof of delivery

**Project:** ParcelRoute  
**Feature:** proof-of-delivery  
**Status:** Active  
**Decision status:** Accepted  

## Context

The proof of delivery workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a delivery agent attempts to record evidence that a shipment was delivered.

## Decision

Validate record ownership and tenant scope before dispatching any command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Client-side role checks alone are insufficient to protect cross-account data. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for proof of delivery. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 028

# Functional Specification — Delivery rerouting

**Project:** ParcelRoute  
**Feature:** rerouting  
**Status:** Active  

## Business purpose

ParcelRoute uses delivery rerouting to allow a recipient to request an eligible alternate delivery location. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated recipient opens a record and chooses to request an eligible alternate delivery location.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed recipient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The delivery rerouting action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for delivery rerouting. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 029

# Business Rules — Delivery rerouting

**Project:** ParcelRoute  
**Feature:** rerouting  
**Status:** Active  

## Approved feature policy

Delivered shipments are not eligible for rerouting requests.

## Eligible actors

Only authenticated recipient identities with permission on the relevant record may initiate delivery rerouting operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted delivery rerouting request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Delivery rerouting expire 10 minutes after issuance.

## Positive scenario

Given a recipient with record access, when the user requests to request an eligible alternate delivery location, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for delivery rerouting. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 030

# API Specification — Delivery rerouting

**Project:** ParcelRoute  
**Feature:** rerouting  
**Status:** Active  

## Operations

`POST /v1/delivery-reroutes` creates a delivery rerouting operation. `GET /v1/delivery-reroutes/{id}` retrieves the current state of a known operation. `GET /v1/delivery-reroutes?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/delivery-reroutes HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-5
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


---

## Document 031

# FAQ and Support — Delivery rerouting

**Project:** ParcelRoute  
**Feature:** rerouting  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible recipient to request an eligible alternate delivery location. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Failed reroute confirmations preserve the original active route. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Temporary authorization tokens for Delivery rerouting expire 30 minutes after issuance.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the rerouting feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 032

# ADR-005 — Asynchronous Reconciliation: Delivery rerouting

**Project:** ParcelRoute  
**Feature:** rerouting  
**Status:** Active  
**Decision status:** Accepted  

## Context

The delivery rerouting workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a recipient attempts to request an eligible alternate delivery location.

## Decision

Persist uncertain provider outcomes and reconcile them by reference instead of assuming success or failure.

## Alternatives

The team considered a simple synchronous design. It was rejected because: External providers can time out after accepting a request. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for delivery rerouting. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 033

# Functional Specification — Failed delivery handling

**Project:** ParcelRoute  
**Feature:** failed-delivery  
**Status:** Active  

## Business purpose

ParcelRoute uses failed delivery handling to allow a delivery agent to record an unsuccessful delivery attempt. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated delivery agent opens a record and chooses to record an unsuccessful delivery attempt.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed delivery agent receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The failed delivery handling action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for failed delivery handling. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 034

# Business Rules — Failed delivery handling

**Project:** ParcelRoute  
**Feature:** failed-delivery  
**Status:** Active  

## Approved feature policy

Every failed delivery attempt requires a standardized failure reason code.

## Eligible actors

Only authenticated delivery agent identities with permission on the relevant record may initiate failed delivery handling operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted failed delivery handling request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Failed delivery handling must be retained for 30 days after closure.

## Positive scenario

Given a delivery agent with record access, when the user requests to record an unsuccessful delivery attempt, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for failed delivery handling. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 035

# API Specification — Failed delivery handling

**Project:** ParcelRoute  
**Feature:** failed-delivery  
**Status:** Active  

## Operations

`POST /v1/failed-deliveries` creates a failed delivery handling operation. `GET /v1/failed-deliveries/{id}` retrieves the current state of a known operation. `GET /v1/failed-deliveries?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/failed-deliveries HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-6
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


---

## Document 036

# FAQ and Support — Failed delivery handling

**Project:** ParcelRoute  
**Feature:** failed-delivery  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible delivery agent to record an unsuccessful delivery attempt. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Duplicate failure events are deduplicated by attempt identifier. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Failed delivery handling must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the failed-delivery feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 037

# ADR-006 — Transactional Outbox: Failed delivery handling

**Project:** ParcelRoute  
**Feature:** failed-delivery  
**Status:** Active  
**Decision status:** Accepted  

## Context

The failed delivery handling workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a delivery agent attempts to record an unsuccessful delivery attempt.

## Decision

Record the domain mutation and an outbox entry in one transaction, then deliver external side effects asynchronously.

## Alternatives

The team considered a simple synchronous design. It was rejected because: A synchronous provider call inside the transaction risks long locks and partial failure ambiguity. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for failed delivery handling. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 038

# Functional Specification — Driver dispatch assignment

**Project:** ParcelRoute  
**Feature:** dispatch  
**Status:** Active  

## Business purpose

ParcelRoute uses driver dispatch assignment to allow a dispatcher to assign unallocated shipments to a delivery route. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated dispatcher opens a record and chooses to assign unallocated shipments to a delivery route.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed dispatcher receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The driver dispatch assignment action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for driver dispatch assignment. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 039

# Business Rules — Driver dispatch assignment

**Project:** ParcelRoute  
**Feature:** dispatch  
**Status:** Active  

## Approved feature policy

A shipment can have only one active route assignment at a time.

## Eligible actors

Only authenticated dispatcher identities with permission on the relevant record may initiate driver dispatch assignment operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted driver dispatch assignment request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Driver dispatch assignment remain valid for 12 hours after the first request.

## Positive scenario

Given a dispatcher with record access, when the user requests to assign unallocated shipments to a delivery route, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for driver dispatch assignment. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 040

# API Specification — Driver dispatch assignment

**Project:** ParcelRoute  
**Feature:** dispatch  
**Status:** Active  

## Operations

`POST /v1/dispatch-assignments` creates a driver dispatch assignment operation. `GET /v1/dispatch-assignments/{id}` retrieves the current state of a known operation. `GET /v1/dispatch-assignments?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/dispatch-assignments HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-7
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


---

## Document 041

# FAQ and Support — Driver dispatch assignment

**Project:** ParcelRoute  
**Feature:** dispatch  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible dispatcher to assign unallocated shipments to a delivery route. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Route publication is atomic and leaves the previous assignment unchanged on failure. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Deduplication keys for Driver dispatch assignment remain valid for 48 hours after the first request.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the dispatch feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 042

# ADR-007 — Idempotent Command Handler: Driver dispatch assignment

**Project:** ParcelRoute  
**Feature:** dispatch  
**Status:** Active  
**Decision status:** Accepted  

## Context

The driver dispatch assignment workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a dispatcher attempts to assign unallocated shipments to a delivery route.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for driver dispatch assignment. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 043

# Functional Specification — Shipment exception alerts

**Project:** ParcelRoute  
**Feature:** exception-alerts  
**Status:** Active  

## Business purpose

ParcelRoute uses shipment exception alerts to allow a sender to receive alerts when a shipment needs attention. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated sender opens a record and chooses to receive alerts when a shipment needs attention.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed sender receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The shipment exception alerts action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for shipment exception alerts. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 044

# Business Rules — Shipment exception alerts

**Project:** ParcelRoute  
**Feature:** exception-alerts  
**Status:** Active  

## Approved feature policy

Resolved shipment exceptions are excluded from newly generated alert batches.

## Eligible actors

Only authenticated sender identities with permission on the relevant record may initiate shipment exception alerts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted shipment exception alerts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Shipment exception alerts workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a sender with record access, when the user requests to receive alerts when a shipment needs attention, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for shipment exception alerts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 045

# API Specification — Shipment exception alerts

**Project:** ParcelRoute  
**Feature:** exception-alerts  
**Status:** Active  

## Operations

`POST /v1/exception-alerts` creates a shipment exception alerts operation. `GET /v1/exception-alerts/{id}` retrieves the current state of a known operation. `GET /v1/exception-alerts?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/exception-alerts HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-8
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


---

## Document 046

# FAQ and Support — Shipment exception alerts

**Project:** ParcelRoute  
**Feature:** exception-alerts  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible sender to receive alerts when a shipment needs attention. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Transient alert delivery failures may be retried without duplicating the exception record. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Shipment exception alerts workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the exception-alerts feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 047

# ADR-008 — Append-only Operation History: Shipment exception alerts

**Project:** ParcelRoute  
**Feature:** exception-alerts  
**Status:** Active  
**Decision status:** Accepted  

## Context

The shipment exception alerts workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a sender attempts to receive alerts when a shipment needs attention.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for shipment exception alerts. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 048

# Functional Specification — Parcel locker collection

**Project:** ParcelRoute  
**Feature:** locker-pickup  
**Status:** Active  

## Business purpose

ParcelRoute uses parcel locker collection to allow a recipient to collect a parcel from an assigned locker. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated recipient opens a record and chooses to collect a parcel from an assigned locker.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed recipient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The parcel locker collection action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for parcel locker collection. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 049

# Business Rules — Parcel locker collection

**Project:** ParcelRoute  
**Feature:** locker-pickup  
**Status:** Active  

## Approved feature policy

A locker pickup code is invalidated immediately after a successful collection.

## Eligible actors

Only authenticated recipient identities with permission on the relevant record may initiate parcel locker collection operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted parcel locker collection request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Parcel locker collection remain downloadable for 7 days.

## Positive scenario

Given a recipient with record access, when the user requests to collect a parcel from an assigned locker, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for parcel locker collection. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 050

# API Specification — Parcel locker collection

**Project:** ParcelRoute  
**Feature:** locker-pickup  
**Status:** Active  

## Operations

`POST /v1/locker-collections` creates a parcel locker collection operation. `GET /v1/locker-collections/{id}` retrieves the current state of a known operation. `GET /v1/locker-collections?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/locker-collections HTTP/1.1
Authorization: Bearer <token>
Idempotency-Key: example-9
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


---

## Document 051

# FAQ and Support — Parcel locker collection

**Project:** ParcelRoute  
**Feature:** locker-pickup  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible recipient to collect a parcel from an assigned locker. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: An unlock request is correlated to its code and acknowledged before completion is recorded. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational audit extracts for Parcel locker collection remain downloadable for 14 days.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the locker-pickup feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 052

# ADR-009 — Authorization at API Boundary: Parcel locker collection

**Project:** ParcelRoute  
**Feature:** locker-pickup  
**Status:** Active  
**Decision status:** Accepted  

## Context

The parcel locker collection workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a recipient attempts to collect a parcel from an assigned locker.

## Decision

Validate record ownership and tenant scope before dispatching any command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Client-side role checks alone are insufficient to protect cross-account data. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for parcel locker collection. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 053

# Functional Specification — Parcel damage claims

**Project:** ParcelRoute  
**Feature:** damage-claims  
**Status:** Active  

## Business purpose

ParcelRoute uses parcel damage claims to allow a sender to submit a claim for a damaged delivered parcel. The desired outcome is observable and bound to one record. The feature works within parcel delivery operations and shipment tracking. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated sender opens a record and chooses to submit a claim for a damaged delivered parcel.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed sender receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The parcel damage claims action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for parcel damage claims. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 054

# Business Rules — Parcel damage claims

**Project:** ParcelRoute  
**Feature:** damage-claims  
**Status:** Active  

## Approved feature policy

Damage claims require at least one photo attachment before they can be approved.

## Eligible actors

Only authenticated sender identities with permission on the relevant record may initiate parcel damage claims operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted parcel damage claims request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Parcel damage claims expire 10 minutes after issuance.

## Positive scenario

Given a sender with record access, when the user requests to submit a claim for a damaged delivered parcel, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for parcel damage claims. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 055

# API Specification — Parcel damage claims

**Project:** ParcelRoute  
**Feature:** damage-claims  
**Status:** Active  

## Operations

`POST /v1/damage-claims` creates a parcel damage claims operation. `GET /v1/damage-claims/{id}` retrieves the current state of a known operation. `GET /v1/damage-claims?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/damage-claims HTTP/1.1
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


---

## Document 056

# FAQ and Support — Parcel damage claims

**Project:** ParcelRoute  
**Feature:** damage-claims  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible sender to submit a claim for a damaged delivered parcel. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Failed attachments remain pending and do not count as accepted evidence. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Temporary authorization tokens for Parcel damage claims expire 30 minutes after issuance.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the damage-claims feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 057

# ADR-010 — Asynchronous Reconciliation: Parcel damage claims

**Project:** ParcelRoute  
**Feature:** damage-claims  
**Status:** Active  
**Decision status:** Accepted  

## Context

The parcel damage claims workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a sender attempts to submit a claim for a damaged delivered parcel.

## Decision

Persist uncertain provider outcomes and reconcile them by reference instead of assuming success or failure.

## Alternatives

The team considered a simple synchronous design. It was rejected because: External providers can time out after accepting a request. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for parcel damage claims. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.
