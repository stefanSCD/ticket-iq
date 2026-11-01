# CareQueue — Combined Documentation

All documents below are byte-identical in content to their corresponding structured files. Do not index both representations together.

---

## Document 001

# CareQueue — Project overview and glossary

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Scope

CareQueue handles non-clinical scheduling and administrative workflows for outpatient practices. This project is fictional. It has 10 independent feature areas and a set of shared cross-cutting constraints.

## Terms

A request is a user-intended operation. An event records an observed transition. A policy is an approved product decision. A ticket describes work; it does not override a policy unless approved.

## Roles

patient, clinic receptionist, clinician, clinic administrator. Each role is limited to the records and tenants it is authorized to act upon.

## Interpretation

Product policy lives in business rules; functional specifications define user flows; API contracts define network semantics; ADRs explain engineering choices; FAQ is support-facing context. Similarity to a feature does not automatically answer a ticket question.


---

## Document 002

# CareQueue — Security and privacy boundaries

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

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

# CareQueue — Integration catalogue

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Dependencies

calendar provider, email provider, SMS gateway, video meeting provider. Each provider may fail, delay, duplicate or time out. A timeout does not prove the provider failed to accept an operation.

## Reconciliation

A stable operation ID links local changes to provider acknowledgements. Failed side effects can be reconciled without silently overwriting authoritative data.

## Product choices

A provider offering an API does not make that option a default business requirement. The product owner must explicitly approve user-visible behavior.


---

## Document 004

# CareQueue — Quality and observability

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Quality baseline

Availability and privacy are prioritized; clinical notes and diagnostic recommendations are outside the dataset scope.

## Observability

Services expose correlation IDs, stable error classes, retry queue health and pending-versus-terminal outcomes. Private payloads are redacted.

## Acceptance

Project-wide availability targets do not set feature-specific reminder deadlines, payment thresholds, retry ceilings or retention periods. QA must ask if a product-specific boundary remains undocumented.


---

## Document 005

# CareQueue — Support and incident response

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

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

# CareQueue — Requirements decision governance

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Source hierarchy

Approved business rules and functional specifications define intended product behavior. API specifications define interfaces, and ADRs define architecture. FAQ pages describe operational experience.

## Authority

Two active policy sources can genuinely contradict one another; authority or creation date alone must not be used as a guess for missing product approval.

## Ticket changes

The author or product owner approves clarification-derived acceptance criteria before the underlying Jira ticket is updated. Changes require source IDs and a rationale.


---

## Document 007

# CareQueue — Acceptance testing patterns

**Status:** Active

## About

CareQueue: Outpatient appointment and administration platform. The page is authoritative only in the synthetic project context.

## Testable criteria

Express observable results as Given-When-Then conditions. Cover authorized success, rejected permissions, duplicate requests and external dependencies failing.

## Traceability

Added product constraints must reference an approved document excerpt or a confirmed stakeholder answer. An SLM must not convert an architectural preference into a business rule.

## Missing requirements

If timing, thresholds, payment rules or scope are unspecified, identify the smallest consequential decision and ask one focused question rather than inventing a default.


---

## Document 008

# Functional Specification — Appointment booking

**Project:** CareQueue  
**Feature:** appointment-booking  
**Status:** Active  

## Business purpose

CareQueue uses appointment booking to allow a patient to book a free consultation slot. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to book a free consultation slot.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The appointment booking action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for appointment booking. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 009

# Business Rules — Appointment booking

**Project:** CareQueue  
**Feature:** appointment-booking  
**Status:** Active  

## Approved feature policy

Only available, non-held slots may be confirmed as appointments.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate appointment booking operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment booking request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Appointment booking must be retained for 30 days after closure.

## Positive scenario

Given a patient with record access, when the user requests to book a free consultation slot, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment booking. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 010

# API Specification — Appointment booking

**Project:** CareQueue  
**Feature:** appointment-booking  
**Status:** Active  

## Operations

`POST /v1/appointments` creates a appointment booking operation. `GET /v1/appointments/{id}` retrieves the current state of a known operation. `GET /v1/appointments?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/appointments HTTP/1.1
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

# FAQ and Support — Appointment booking

**Project:** CareQueue  
**Feature:** appointment-booking  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to book a free consultation slot. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Calendar provider timeouts are eligible for a controlled retry. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Appointment booking must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the appointment-booking feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 012

# ADR-001 — Transactional Outbox: Appointment booking

**Project:** CareQueue  
**Feature:** appointment-booking  
**Status:** Active  
**Decision status:** Accepted  

## Context

The appointment booking workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to book a free consultation slot.

## Decision

Record the domain mutation and an outbox entry in one transaction, then deliver external side effects asynchronously.

## Alternatives

The team considered a simple synchronous design. It was rejected because: A synchronous provider call inside the transaction risks long locks and partial failure ambiguity. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for appointment booking. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 013

# Functional Specification — Appointment rescheduling

**Project:** CareQueue  
**Feature:** rescheduling  
**Status:** Active  

## Business purpose

CareQueue uses appointment rescheduling to allow a patient to move an existing appointment to another available slot. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to move an existing appointment to another available slot.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The appointment rescheduling action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for appointment rescheduling. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 014

# Business Rules — Appointment rescheduling

**Project:** CareQueue  
**Feature:** rescheduling  
**Status:** Active  

## Approved feature policy

Rescheduling preserves the appointment identifier and records the slot change in history.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate appointment rescheduling operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment rescheduling request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Appointment rescheduling remain valid for 12 hours after the first request.

## Positive scenario

Given a patient with record access, when the user requests to move an existing appointment to another available slot, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment rescheduling. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 015

# API Specification — Appointment rescheduling

**Project:** CareQueue  
**Feature:** rescheduling  
**Status:** Active  

## Operations

`POST /v1/appointment-reschedules` creates a appointment rescheduling operation. `GET /v1/appointment-reschedules/{id}` retrieves the current state of a known operation. `GET /v1/appointment-reschedules?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/appointment-reschedules HTTP/1.1
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

# FAQ and Support — Appointment rescheduling

**Project:** CareQueue  
**Feature:** rescheduling  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to move an existing appointment to another available slot. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Temporary slot reservation failures may be retried before asking the patient to choose again. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Deduplication keys for Appointment rescheduling remain valid for 48 hours after the first request.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the rescheduling feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 017

# ADR-002 — Idempotent Command Handler: Appointment rescheduling

**Project:** CareQueue  
**Feature:** rescheduling  
**Status:** Active  
**Decision status:** Accepted  

## Context

The appointment rescheduling workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to move an existing appointment to another available slot.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for appointment rescheduling. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 018

# Functional Specification — Appointment cancellation

**Project:** CareQueue  
**Feature:** cancellation  
**Status:** Active  

## Business purpose

CareQueue uses appointment cancellation to allow a patient to cancel a scheduled visit. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to cancel a scheduled visit.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The appointment cancellation action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for appointment cancellation. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 019

# Business Rules — Appointment cancellation

**Project:** CareQueue  
**Feature:** cancellation  
**Status:** Active  

## Approved feature policy

A canceled appointment releases its slot back to the availability pool.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate appointment cancellation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment cancellation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Appointment cancellation workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a patient with record access, when the user requests to cancel a scheduled visit, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment cancellation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 020

# API Specification — Appointment cancellation

**Project:** CareQueue  
**Feature:** cancellation  
**Status:** Active  

## Operations

`POST /v1/appointment-cancellations` creates a appointment cancellation operation. `GET /v1/appointment-cancellations/{id}` retrieves the current state of a known operation. `GET /v1/appointment-cancellations?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/appointment-cancellations HTTP/1.1
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

# FAQ and Support — Appointment cancellation

**Project:** CareQueue  
**Feature:** cancellation  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to cancel a scheduled visit. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Failed external calendar updates are queued for reconciliation. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Appointment cancellation workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the cancellation feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 022

# ADR-003 — Append-only Operation History: Appointment cancellation

**Project:** CareQueue  
**Feature:** cancellation  
**Status:** Active  
**Decision status:** Accepted  

## Context

The appointment cancellation workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to cancel a scheduled visit.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for appointment cancellation. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 023

# Functional Specification — Waitlist offers

**Project:** CareQueue  
**Feature:** waitlist  
**Status:** Active  

## Business purpose

CareQueue uses waitlist offers to allow a patient to accept an earlier appointment from the waitlist. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to accept an earlier appointment from the waitlist.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The waitlist offers action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for waitlist offers. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 024

# Business Rules — Waitlist offers

**Project:** CareQueue  
**Feature:** waitlist  
**Status:** Active  

## Approved feature policy

A waitlist slot can be confirmed by only one patient through an atomic acceptance operation.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate waitlist offers operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted waitlist offers request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Waitlist offers remain downloadable for 7 days.

## Positive scenario

Given a patient with record access, when the user requests to accept an earlier appointment from the waitlist, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for waitlist offers. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 025

# API Specification — Waitlist offers

**Project:** CareQueue  
**Feature:** waitlist  
**Status:** Active  

## Operations

`POST /v1/waitlist-offers` creates a waitlist offers operation. `GET /v1/waitlist-offers/{id}` retrieves the current state of a known operation. `GET /v1/waitlist-offers?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/waitlist-offers HTTP/1.1
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

# FAQ and Support — Waitlist offers

**Project:** CareQueue  
**Feature:** waitlist  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to accept an earlier appointment from the waitlist. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Failed waitlist notification deliveries are eligible for a retry. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational audit extracts for Waitlist offers remain downloadable for 14 days.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the waitlist feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 027

# ADR-004 — Authorization at API Boundary: Waitlist offers

**Project:** CareQueue  
**Feature:** waitlist  
**Status:** Active  
**Decision status:** Accepted  

## Context

The waitlist offers workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to accept an earlier appointment from the waitlist.

## Decision

Validate record ownership and tenant scope before dispatching any command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Client-side role checks alone are insufficient to protect cross-account data. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for waitlist offers. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 028

# Functional Specification — Appointment reminders

**Project:** CareQueue  
**Feature:** reminders  
**Status:** Active  

## Business purpose

CareQueue uses appointment reminders to allow a patient to receive reminders about upcoming appointments. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to receive reminders about upcoming appointments.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The appointment reminders action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for appointment reminders. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 029

# Business Rules — Appointment reminders

**Project:** CareQueue  
**Feature:** reminders  
**Status:** Active  

## Approved feature policy

Standard appointment reminders are delivered by email to a verified address.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate appointment reminders operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment reminders request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Appointment reminders expire 10 minutes after issuance.

## Positive scenario

Given a patient with record access, when the user requests to receive reminders about upcoming appointments, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment reminders. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 030

# API Specification — Appointment reminders

**Project:** CareQueue  
**Feature:** reminders  
**Status:** Active  

## Operations

`POST /v1/appointment-reminders` creates a appointment reminders operation. `GET /v1/appointment-reminders/{id}` retrieves the current state of a known operation. `GET /v1/appointment-reminders?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/appointment-reminders HTTP/1.1
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

# FAQ and Support — Appointment reminders

**Project:** CareQueue  
**Feature:** reminders  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to receive reminders about upcoming appointments. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Temporary reminder provider failures are retried through the notification queue. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Temporary authorization tokens for Appointment reminders expire 30 minutes after issuance.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the reminders feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 032

# ADR-005 — Asynchronous Reconciliation: Appointment reminders

**Project:** CareQueue  
**Feature:** reminders  
**Status:** Active  
**Decision status:** Accepted  

## Context

The appointment reminders workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to receive reminders about upcoming appointments.

## Decision

Persist uncertain provider outcomes and reconcile them by reference instead of assuming success or failure.

## Alternatives

The team considered a simple synchronous design. It was rejected because: External providers can time out after accepting a request. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for appointment reminders. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 033

# Functional Specification — Provider availability

**Project:** CareQueue  
**Feature:** provider-availability  
**Status:** Active  

## Business purpose

CareQueue uses provider availability to allow a clinic receptionist to manage available appointment slots for a clinician. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated clinic receptionist opens a record and chooses to manage available appointment slots for a clinician.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed clinic receptionist receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The provider availability action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for provider availability. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 034

# Business Rules — Provider availability

**Project:** CareQueue  
**Feature:** provider-availability  
**Status:** Active  

## Approved feature policy

Published appointment slots for the same clinician must not overlap.

## Eligible actors

Only authenticated clinic receptionist identities with permission on the relevant record may initiate provider availability operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted provider availability request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Provider availability must be retained for 30 days after closure.

## Positive scenario

Given a clinic receptionist with record access, when the user requests to manage available appointment slots for a clinician, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for provider availability. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 035

# API Specification — Provider availability

**Project:** CareQueue  
**Feature:** provider-availability  
**Status:** Active  

## Operations

`POST /v1/provider-availability` creates a provider availability operation. `GET /v1/provider-availability/{id}` retrieves the current state of a known operation. `GET /v1/provider-availability?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/provider-availability HTTP/1.1
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

# FAQ and Support — Provider availability

**Project:** CareQueue  
**Feature:** provider-availability  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible clinic receptionist to manage available appointment slots for a clinician. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Failed imports can be retried with the same import identifier. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Provider availability must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the provider-availability feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 037

# ADR-006 — Transactional Outbox: Provider availability

**Project:** CareQueue  
**Feature:** provider-availability  
**Status:** Active  
**Decision status:** Accepted  

## Context

The provider availability workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a clinic receptionist attempts to manage available appointment slots for a clinician.

## Decision

Record the domain mutation and an outbox entry in one transaction, then deliver external side effects asynchronously.

## Alternatives

The team considered a simple synchronous design. It was rejected because: A synchronous provider call inside the transaction risks long locks and partial failure ambiguity. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for provider availability. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 038

# Functional Specification — Patient check-in

**Project:** CareQueue  
**Feature:** check-in  
**Status:** Active  

## Business purpose

CareQueue uses patient check-in to allow a clinic receptionist to mark patients as arrived at the clinic. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated clinic receptionist opens a record and chooses to mark patients as arrived at the clinic.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed clinic receptionist receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The patient check-in action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for patient check-in. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 039

# Business Rules — Patient check-in

**Project:** CareQueue  
**Feature:** check-in  
**Status:** Active  

## Approved feature policy

An appointment may have one active check-in record; duplicate check-in requests are idempotent.

## Eligible actors

Only authenticated clinic receptionist identities with permission on the relevant record may initiate patient check-in operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted patient check-in request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Patient check-in remain valid for 12 hours after the first request.

## Positive scenario

Given a clinic receptionist with record access, when the user requests to mark patients as arrived at the clinic, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for patient check-in. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 040

# API Specification — Patient check-in

**Project:** CareQueue  
**Feature:** check-in  
**Status:** Active  

## Operations

`POST /v1/patient-checkins` creates a patient check-in operation. `GET /v1/patient-checkins/{id}` retrieves the current state of a known operation. `GET /v1/patient-checkins?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/patient-checkins HTTP/1.1
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

# FAQ and Support — Patient check-in

**Project:** CareQueue  
**Feature:** check-in  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible clinic receptionist to mark patients as arrived at the clinic. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: The local check-in record persists even when the display connection fails. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Deduplication keys for Patient check-in remain valid for 48 hours after the first request.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the check-in feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 042

# ADR-007 — Idempotent Command Handler: Patient check-in

**Project:** CareQueue  
**Feature:** check-in  
**Status:** Active  
**Decision status:** Accepted  

## Context

The patient check-in workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a clinic receptionist attempts to mark patients as arrived at the clinic.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for patient check-in. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 043

# Functional Specification — Televisit access links

**Project:** CareQueue  
**Feature:** televisit-links  
**Status:** Active  

## Business purpose

CareQueue uses televisit access links to allow a patient to join a remote appointment using a secure link. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to join a remote appointment using a secure link.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The televisit access links action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for televisit access links. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 044

# Business Rules — Televisit access links

**Project:** CareQueue  
**Feature:** televisit-links  
**Status:** Active  

## Approved feature policy

Televisit links are scoped to one appointment and cannot be reused across appointments.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate televisit access links operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted televisit access links request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Televisit access links workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a patient with record access, when the user requests to join a remote appointment using a secure link, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for televisit access links. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 045

# API Specification — Televisit access links

**Project:** CareQueue  
**Feature:** televisit-links  
**Status:** Active  

## Operations

`POST /v1/televisit-links` creates a televisit access links operation. `GET /v1/televisit-links/{id}` retrieves the current state of a known operation. `GET /v1/televisit-links?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/televisit-links HTTP/1.1
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

# FAQ and Support — Televisit access links

**Project:** CareQueue  
**Feature:** televisit-links  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to join a remote appointment using a secure link. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Meeting link provisioning may be retried using a stable appointment correlation ID. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Televisit access links workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the televisit-links feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 047

# ADR-008 — Append-only Operation History: Televisit access links

**Project:** CareQueue  
**Feature:** televisit-links  
**Status:** Active  
**Decision status:** Accepted  

## Context

The televisit access links workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to join a remote appointment using a secure link.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for televisit access links. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 048

# Functional Specification — Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  

## Business purpose

CareQueue uses pre-visit intake forms to allow a patient to complete administrative intake information before a visit. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to complete administrative intake information before a visit.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The pre-visit intake forms action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for pre-visit intake forms. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 049

# Business Rules — Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  

## Approved feature policy

Submitted administrative intake forms are immutable; corrections require a new revision.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate pre-visit intake forms operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted pre-visit intake forms request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Pre-visit intake forms remain downloadable for 7 days.

## Positive scenario

Given a patient with record access, when the user requests to complete administrative intake information before a visit, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for pre-visit intake forms. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 050

# API Specification — Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  

## Operations

`POST /v1/intake-forms` creates a pre-visit intake forms operation. `GET /v1/intake-forms/{id}` retrieves the current state of a known operation. `GET /v1/intake-forms?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/intake-forms HTTP/1.1
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

# FAQ and Support — Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible patient to complete administrative intake information before a visit. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Autosave errors are reported without marking unsaved fields as persisted. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational audit extracts for Pre-visit intake forms remain downloadable for 14 days.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the intake-forms feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 052

# ADR-009 — Authorization at API Boundary: Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  
**Decision status:** Accepted  

## Context

The pre-visit intake forms workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a patient attempts to complete administrative intake information before a visit.

## Decision

Validate record ownership and tenant scope before dispatching any command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Client-side role checks alone are insufficient to protect cross-account data. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for pre-visit intake forms. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 053

# Functional Specification — Appointment audit exports

**Project:** CareQueue  
**Feature:** audit-export  
**Status:** Active  

## Business purpose

CareQueue uses appointment audit exports to allow a clinic administrator to export scheduling changes for an authorized audit. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated clinic administrator opens a record and chooses to export scheduling changes for an authorized audit.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed clinic administrator receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The appointment audit exports action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for appointment audit exports. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 054

# Business Rules — Appointment audit exports

**Project:** CareQueue  
**Feature:** audit-export  
**Status:** Active  

## Approved feature policy

Appointment audit exports are restricted to the requesting clinic tenant.

## Eligible actors

Only authenticated clinic administrator identities with permission on the relevant record may initiate appointment audit exports operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment audit exports request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Appointment audit exports expire 10 minutes after issuance.

## Positive scenario

Given a clinic administrator with record access, when the user requests to export scheduling changes for an authorized audit, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment audit exports. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 055

# API Specification — Appointment audit exports

**Project:** CareQueue  
**Feature:** audit-export  
**Status:** Active  

## Operations

`POST /v1/appointment-audit-exports` creates a appointment audit exports operation. `GET /v1/appointment-audit-exports/{id}` retrieves the current state of a known operation. `GET /v1/appointment-audit-exports?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/appointment-audit-exports HTTP/1.1
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

# FAQ and Support — Appointment audit exports

**Project:** CareQueue  
**Feature:** audit-export  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible clinic administrator to export scheduling changes for an authorized audit. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Failed export uploads can be retried with an unchanged export job ID. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Temporary authorization tokens for Appointment audit exports expire 30 minutes after issuance.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the audit-export feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 057

# ADR-010 — Asynchronous Reconciliation: Appointment audit exports

**Project:** CareQueue  
**Feature:** audit-export  
**Status:** Active  
**Decision status:** Accepted  

## Context

The appointment audit exports workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a clinic administrator attempts to export scheduling changes for an authorized audit.

## Decision

Persist uncertain provider outcomes and reconcile them by reference instead of assuming success or failure.

## Alternatives

The team considered a simple synchronous design. It was rejected because: External providers can time out after accepting a request. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for appointment audit exports. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.
