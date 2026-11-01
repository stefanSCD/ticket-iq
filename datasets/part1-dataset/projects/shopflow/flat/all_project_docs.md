# ShopFlow — Combined Documentation

All documents below are byte-identical in content to their corresponding structured files. Do not index both representations together.

---

## Document 001

# ShopFlow — Project overview and glossary

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

## Scope

ShopFlow serves shoppers and merchants with checkout, post-purchase support, stock and shipping workflows. This project is fictional. It has 10 independent feature areas and a set of shared cross-cutting constraints.

## Terms

A request is a user-intended operation. An event records an observed transition. A policy is an approved product decision. A ticket describes work; it does not override a policy unless approved.

## Roles

shopper, merchant operator, support agent, platform administrator. Each role is limited to the records and tenants it is authorized to act upon.

## Interpretation

Product policy lives in business rules; functional specifications define user flows; API contracts define network semantics; ADRs explain engineering choices; FAQ is support-facing context. Similarity to a feature does not automatically answer a ticket question.


---

## Document 002

# ShopFlow — Security and privacy boundaries

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

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

# ShopFlow — Integration catalogue

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

## Dependencies

payment gateway, carrier adapter, tax service, email provider. Each provider may fail, delay, duplicate or time out. A timeout does not prove the provider failed to accept an operation.

## Reconciliation

A stable operation ID links local changes to provider acknowledgements. Failed side effects can be reconciled without silently overwriting authoritative data.

## Product choices

A provider offering an API does not make that option a default business requirement. The product owner must explicitly approve user-visible behavior.


---

## Document 004

# ShopFlow — Quality and observability

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

## Quality baseline

99.9% monthly availability for order-facing reads; mutations use request IDs and durable event logging.

## Observability

Services expose correlation IDs, stable error classes, retry queue health and pending-versus-terminal outcomes. Private payloads are redacted.

## Acceptance

Project-wide availability targets do not set feature-specific reminder deadlines, payment thresholds, retry ceilings or retention periods. QA must ask if a product-specific boundary remains undocumented.


---

## Document 005

# ShopFlow — Support and incident response

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

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

# ShopFlow — Requirements decision governance

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

## Source hierarchy

Approved business rules and functional specifications define intended product behavior. API specifications define interfaces, and ADRs define architecture. FAQ pages describe operational experience.

## Authority

Two active policy sources can genuinely contradict one another; authority or creation date alone must not be used as a guess for missing product approval.

## Ticket changes

The author or product owner approves clarification-derived acceptance criteria before the underlying Jira ticket is updated. Changes require source IDs and a rationale.


---

## Document 007

# ShopFlow — Acceptance testing patterns

**Status:** Active

## About

ShopFlow: Multi-merchant e-commerce platform. The page is authoritative only in the synthetic project context.

## Testable criteria

Express observable results as Given-When-Then conditions. Cover authorized success, rejected permissions, duplicate requests and external dependencies failing.

## Traceability

Added product constraints must reference an approved document excerpt or a confirmed stakeholder answer. An SLM must not convert an architectural preference into a business rule.

## Missing requirements

If timing, thresholds, payment rules or scope are unspecified, identify the smallest consequential decision and ask one focused question rather than inventing a default.


---

## Document 008

# Functional Specification — Order status alerts

**Project:** ShopFlow  
**Feature:** order-alerts  
**Status:** Active  

## Business purpose

ShopFlow uses order status alerts to allow a shopper to receive an alert when an order changes state. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to receive an alert when an order changes state.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The order status alerts action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for order status alerts. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 009

# Business Rules — Order status alerts

**Project:** ShopFlow  
**Feature:** order-alerts  
**Status:** Active  

## Approved feature policy

Order status alerts are sent by email to the verified address of the order owner.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate order status alerts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted order status alerts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Order status alerts must be retained for 30 days after closure.

## Positive scenario

Given a shopper with record access, when the user requests to receive an alert when an order changes state, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for order status alerts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 010

# API Specification — Order status alerts

**Project:** ShopFlow  
**Feature:** order-alerts  
**Status:** Active  

## Operations

`POST /v1/order-alerts` creates a order status alerts operation. `GET /v1/order-alerts/{id}` retrieves the current state of a known operation. `GET /v1/order-alerts?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/order-alerts HTTP/1.1
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

# FAQ and Support — Order status alerts

**Project:** ShopFlow  
**Feature:** order-alerts  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to receive an alert when an order changes state. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Temporary provider errors are eligible for an automatic retry. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Order status alerts must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the order-alerts feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 012

# ADR-001 — Transactional Outbox: Order status alerts

**Project:** ShopFlow  
**Feature:** order-alerts  
**Status:** Active  
**Decision status:** Accepted  

## Context

The order status alerts workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to receive an alert when an order changes state.

## Decision

Record the domain mutation and an outbox entry in one transaction, then deliver external side effects asynchronously.

## Alternatives

The team considered a simple synchronous design. It was rejected because: A synchronous provider call inside the transaction risks long locks and partial failure ambiguity. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for order status alerts. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 013

# Functional Specification — Coupon redemption

**Project:** ShopFlow  
**Feature:** coupon-redemption  
**Status:** Active  

## Business purpose

ShopFlow uses coupon redemption to allow a shopper to apply a discount code during checkout. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to apply a discount code during checkout.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The coupon redemption action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for coupon redemption. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 014

# Business Rules — Coupon redemption

**Project:** ShopFlow  
**Feature:** coupon-redemption  
**Status:** Active  

## Approved feature policy

Two percentage-based coupons cannot be stacked on a single checkout.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate coupon redemption operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted coupon redemption request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Coupon redemption remain valid for 12 hours after the first request.

## Positive scenario

Given a shopper with record access, when the user requests to apply a discount code during checkout, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for coupon redemption. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 015

# API Specification — Coupon redemption

**Project:** ShopFlow  
**Feature:** coupon-redemption  
**Status:** Active  

## Operations

`POST /v1/coupon-redemptions` creates a coupon redemption operation. `GET /v1/coupon-redemptions/{id}` retrieves the current state of a known operation. `GET /v1/coupon-redemptions?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/coupon-redemptions HTTP/1.1
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

# FAQ and Support — Coupon redemption

**Project:** ShopFlow  
**Feature:** coupon-redemption  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to apply a discount code during checkout. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Coupon service timeouts may be retried without changing the discount calculation. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Deduplication keys for Coupon redemption remain valid for 48 hours after the first request.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the coupon-redemption feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 017

# ADR-002 — Idempotent Command Handler: Coupon redemption

**Project:** ShopFlow  
**Feature:** coupon-redemption  
**Status:** Active  
**Decision status:** Accepted  

## Context

The coupon redemption workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to apply a discount code during checkout.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for coupon redemption. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 018

# Functional Specification — Return requests

**Project:** ShopFlow  
**Feature:** returns  
**Status:** Active  

## Business purpose

ShopFlow uses return requests to allow a shopper to request the return of an eligible delivered item. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to request the return of an eligible delivered item.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The return requests action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for return requests. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 019

# Business Rules — Return requests

**Project:** ShopFlow  
**Feature:** returns  
**Status:** Active  

## Approved feature policy

The standard return window begins when the carrier marks the item delivered.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate return requests operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted return requests request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Return requests workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a shopper with record access, when the user requests to request the return of an eligible delivered item, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for return requests. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 020

# API Specification — Return requests

**Project:** ShopFlow  
**Feature:** returns  
**Status:** Active  

## Operations

`POST /v1/return-requests` creates a return requests operation. `GET /v1/return-requests/{id}` retrieves the current state of a known operation. `GET /v1/return-requests?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/return-requests HTTP/1.1
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

# FAQ and Support — Return requests

**Project:** ShopFlow  
**Feature:** returns  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to request the return of an eligible delivered item. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Label creation may be retried after a transient carrier-adapter failure. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Return requests workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the returns feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 022

# ADR-003 — Append-only Operation History: Return requests

**Project:** ShopFlow  
**Feature:** returns  
**Status:** Active  
**Decision status:** Accepted  

## Context

The return requests workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to request the return of an eligible delivered item.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for return requests. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 023

# Functional Specification — Refund execution

**Project:** ShopFlow  
**Feature:** refunds  
**Status:** Active  

## Business purpose

ShopFlow uses refund execution to allow a support agent to approve and initiate an eligible refund. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated support agent opens a record and chooses to approve and initiate an eligible refund.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed support agent receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The refund execution action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for refund execution. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 024

# Business Rules — Refund execution

**Project:** ShopFlow  
**Feature:** refunds  
**Status:** Active  

## Approved feature policy

Refunds must use the original payment method; alternate destinations are not supported.

## Eligible actors

Only authenticated support agent identities with permission on the relevant record may initiate refund execution operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted refund execution request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Refund execution remain downloadable for 7 days.

## Positive scenario

Given a support agent with record access, when the user requests to approve and initiate an eligible refund, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for refund execution. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 025

# API Specification — Refund execution

**Project:** ShopFlow  
**Feature:** refunds  
**Status:** Active  

## Operations

`POST /v1/refunds` creates a refund execution operation. `GET /v1/refunds/{id}` retrieves the current state of a known operation. `GET /v1/refunds?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/refunds HTTP/1.1
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

# FAQ and Support — Refund execution

**Project:** ShopFlow  
**Feature:** refunds  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible support agent to approve and initiate an eligible refund. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Refund requests include a stable idempotency key when retried. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational audit extracts for Refund execution remain downloadable for 14 days.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the refunds feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 027

# ADR-004 — Authorization at API Boundary: Refund execution

**Project:** ShopFlow  
**Feature:** refunds  
**Status:** Active  
**Decision status:** Accepted  

## Context

The refund execution workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a support agent attempts to approve and initiate an eligible refund.

## Decision

Validate record ownership and tenant scope before dispatching any command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Client-side role checks alone are insufficient to protect cross-account data. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for refund execution. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 028

# Functional Specification — Saved shopping carts

**Project:** ShopFlow  
**Feature:** saved-carts  
**Status:** Active  

## Business purpose

ShopFlow uses saved shopping carts to allow a shopper to resume a previously saved shopping cart. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to resume a previously saved shopping cart.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The saved shopping carts action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for saved shopping carts. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 029

# Business Rules — Saved shopping carts

**Project:** ShopFlow  
**Feature:** saved-carts  
**Status:** Active  

## Approved feature policy

Saving a cart does not lock prices; current prices are checked again at checkout.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate saved shopping carts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted saved shopping carts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Saved shopping carts expire 10 minutes after issuance.

## Positive scenario

Given a shopper with record access, when the user requests to resume a previously saved shopping cart, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for saved shopping carts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 030

# API Specification — Saved shopping carts

**Project:** ShopFlow  
**Feature:** saved-carts  
**Status:** Active  

## Operations

`POST /v1/saved-carts` creates a saved shopping carts operation. `GET /v1/saved-carts/{id}` retrieves the current state of a known operation. `GET /v1/saved-carts?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/saved-carts HTTP/1.1
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

# FAQ and Support — Saved shopping carts

**Project:** ShopFlow  
**Feature:** saved-carts  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to resume a previously saved shopping cart. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Saved cart reads can be retried after transient storage failures. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Temporary authorization tokens for Saved shopping carts expire 30 minutes after issuance.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the saved-carts feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 032

# ADR-005 — Asynchronous Reconciliation: Saved shopping carts

**Project:** ShopFlow  
**Feature:** saved-carts  
**Status:** Active  
**Decision status:** Accepted  

## Context

The saved shopping carts workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to resume a previously saved shopping cart.

## Decision

Persist uncertain provider outcomes and reconcile them by reference instead of assuming success or failure.

## Alternatives

The team considered a simple synchronous design. It was rejected because: External providers can time out after accepting a request. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for saved shopping carts. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 033

# Functional Specification — Inventory reservations

**Project:** ShopFlow  
**Feature:** inventory-holds  
**Status:** Active  

## Business purpose

ShopFlow uses inventory reservations to allow a merchant operator to reserve stock for an active checkout. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated merchant operator opens a record and chooses to reserve stock for an active checkout.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed merchant operator receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The inventory reservations action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for inventory reservations. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 034

# Business Rules — Inventory reservations

**Project:** ShopFlow  
**Feature:** inventory-holds  
**Status:** Active  

## Approved feature policy

A checkout cannot reserve more units than the available sellable stock.

## Eligible actors

Only authenticated merchant operator identities with permission on the relevant record may initiate inventory reservations operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted inventory reservations request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Inventory reservations must be retained for 30 days after closure.

## Positive scenario

Given a merchant operator with record access, when the user requests to reserve stock for an active checkout, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for inventory reservations. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 035

# API Specification — Inventory reservations

**Project:** ShopFlow  
**Feature:** inventory-holds  
**Status:** Active  

## Operations

`POST /v1/inventory-reservations` creates a inventory reservations operation. `GET /v1/inventory-reservations/{id}` retrieves the current state of a known operation. `GET /v1/inventory-reservations?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/inventory-reservations HTTP/1.1
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

# FAQ and Support — Inventory reservations

**Project:** ShopFlow  
**Feature:** inventory-holds  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible merchant operator to reserve stock for an active checkout. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Reservation conflicts are returned to callers without silently overselling inventory. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational event records for Inventory reservations must be retained for 90 days after closure.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the inventory-holds feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 037

# ADR-006 — Transactional Outbox: Inventory reservations

**Project:** ShopFlow  
**Feature:** inventory-holds  
**Status:** Active  
**Decision status:** Accepted  

## Context

The inventory reservations workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a merchant operator attempts to reserve stock for an active checkout.

## Decision

Record the domain mutation and an outbox entry in one transaction, then deliver external side effects asynchronously.

## Alternatives

The team considered a simple synchronous design. It was rejected because: A synchronous provider call inside the transaction risks long locks and partial failure ambiguity. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for inventory reservations. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 038

# Functional Specification — Shipping estimates

**Project:** ShopFlow  
**Feature:** shipping-estimates  
**Status:** Active  

## Business purpose

ShopFlow uses shipping estimates to allow a shopper to view delivery estimates during checkout. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to view delivery estimates during checkout.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The shipping estimates action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for shipping estimates. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 039

# Business Rules — Shipping estimates

**Project:** ShopFlow  
**Feature:** shipping-estimates  
**Status:** Active  

## Approved feature policy

Shipping estimates include both merchant handling time and the carrier transit estimate.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate shipping estimates operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted shipping estimates request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Shipping estimates remain valid for 12 hours after the first request.

## Positive scenario

Given a shopper with record access, when the user requests to view delivery estimates during checkout, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for shipping estimates. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 040

# API Specification — Shipping estimates

**Project:** ShopFlow  
**Feature:** shipping-estimates  
**Status:** Active  

## Operations

`POST /v1/shipping-estimates` creates a shipping estimates operation. `GET /v1/shipping-estimates/{id}` retrieves the current state of a known operation. `GET /v1/shipping-estimates?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/shipping-estimates HTTP/1.1
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

# FAQ and Support — Shipping estimates

**Project:** ShopFlow  
**Feature:** shipping-estimates  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to view delivery estimates during checkout. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Transient carrier estimate errors can trigger a bounded retry. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Deduplication keys for Shipping estimates remain valid for 48 hours after the first request.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the shipping-estimates feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 042

# ADR-007 — Idempotent Command Handler: Shipping estimates

**Project:** ShopFlow  
**Feature:** shipping-estimates  
**Status:** Active  
**Decision status:** Accepted  

## Context

The shipping estimates workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to view delivery estimates during checkout.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for shipping estimates. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 043

# Functional Specification — Guest checkout

**Project:** ShopFlow  
**Feature:** guest-checkout  
**Status:** Active  

## Business purpose

ShopFlow uses guest checkout to allow a shopper to place an order without creating an account. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to place an order without creating an account.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The guest checkout action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for guest checkout. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 044

# Business Rules — Guest checkout

**Project:** ShopFlow  
**Feature:** guest-checkout  
**Status:** Active  

## Approved feature policy

Guest checkout does not require account creation, but a verified contact email is required.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate guest checkout operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted guest checkout request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Guest checkout workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a shopper with record access, when the user requests to place an order without creating an account, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for guest checkout. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 045

# API Specification — Guest checkout

**Project:** ShopFlow  
**Feature:** guest-checkout  
**Status:** Active  

## Operations

`POST /v1/guest-checkouts` creates a guest checkout operation. `GET /v1/guest-checkouts/{id}` retrieves the current state of a known operation. `GET /v1/guest-checkouts?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/guest-checkouts HTTP/1.1
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

# FAQ and Support — Guest checkout

**Project:** ShopFlow  
**Feature:** guest-checkout  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to place an order without creating an account. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Verification emails are rate-limited to reduce abuse. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

The Guest checkout workflow opens manual review after 5 consecutive processing failures.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the guest-checkout feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 047

# ADR-008 — Append-only Operation History: Guest checkout

**Project:** ShopFlow  
**Feature:** guest-checkout  
**Status:** Active  
**Decision status:** Accepted  

## Context

The guest checkout workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to place an order without creating an account.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for guest checkout. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 048

# Functional Specification — Order cancellation

**Project:** ShopFlow  
**Feature:** order-cancellation  
**Status:** Active  

## Business purpose

ShopFlow uses order cancellation to allow a shopper to cancel an order that has not been dispatched. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated shopper opens a record and chooses to cancel an order that has not been dispatched.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed shopper receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The order cancellation action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for order cancellation. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 049

# Business Rules — Order cancellation

**Project:** ShopFlow  
**Feature:** order-cancellation  
**Status:** Active  

## Approved feature policy

Shopper cancellation is allowed only before the carrier handoff event.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate order cancellation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted order cancellation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Order cancellation remain downloadable for 7 days.

## Positive scenario

Given a shopper with record access, when the user requests to cancel an order that has not been dispatched, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for order cancellation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 050

# API Specification — Order cancellation

**Project:** ShopFlow  
**Feature:** order-cancellation  
**Status:** Active  

## Operations

`POST /v1/order-cancellations` creates a order cancellation operation. `GET /v1/order-cancellations/{id}` retrieves the current state of a known operation. `GET /v1/order-cancellations?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/order-cancellations HTTP/1.1
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

# FAQ and Support — Order cancellation

**Project:** ShopFlow  
**Feature:** order-cancellation  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible shopper to cancel an order that has not been dispatched. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Concurrent cancellation and handoff requests are serialized by order version. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Operational audit extracts for Order cancellation remain downloadable for 14 days.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the order-cancellation feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 052

# ADR-009 — Authorization at API Boundary: Order cancellation

**Project:** ShopFlow  
**Feature:** order-cancellation  
**Status:** Active  
**Decision status:** Accepted  

## Context

The order cancellation workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a shopper attempts to cancel an order that has not been dispatched.

## Decision

Validate record ownership and tenant scope before dispatching any command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Client-side role checks alone are insufficient to protect cross-account data. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for order cancellation. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.


---

## Document 053

# Functional Specification — Merchant payouts

**Project:** ShopFlow  
**Feature:** merchant-payouts  
**Status:** Active  

## Business purpose

ShopFlow uses merchant payouts to allow a merchant operator to review and request payout of eligible earnings. The desired outcome is observable and bound to one record. The feature works within multi-merchant e-commerce platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated merchant operator opens a record and chooses to review and request payout of eligible earnings.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed merchant operator receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The merchant payouts action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for merchant payouts. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.


---

## Document 054

# Business Rules — Merchant payouts

**Project:** ShopFlow  
**Feature:** merchant-payouts  
**Status:** Active  

## Approved feature policy

Amounts linked to open payment disputes are excluded from the available payout balance.

## Eligible actors

Only authenticated merchant operator identities with permission on the relevant record may initiate merchant payouts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted merchant payouts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Merchant payouts expire 10 minutes after issuance.

## Positive scenario

Given a merchant operator with record access, when the user requests to review and request payout of eligible earnings, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for merchant payouts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.


---

## Document 055

# API Specification — Merchant payouts

**Project:** ShopFlow  
**Feature:** merchant-payouts  
**Status:** Active  

## Operations

`POST /v1/merchant-payouts` creates a merchant payouts operation. `GET /v1/merchant-payouts/{id}` retrieves the current state of a known operation. `GET /v1/merchant-payouts?limit=20&cursor=...` lists records visible to the authenticated actor.

## Security and idempotency

All endpoints require a bearer token and per-record authorization. Mutations require `Idempotency-Key` and `X-Correlation-ID`. The service never trusts client-provided role names as authority. Querying a foreign record must not leak details about the protected record.

## Request example

```http
POST /v1/merchant-payouts HTTP/1.1
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

# FAQ and Support — Merchant payouts

**Project:** ShopFlow  
**Feature:** merchant-payouts  
**Status:** Active  

## Purpose

**Q: What does this feature provide?**

A: It allows an eligible merchant operator to review and request payout of eligible earnings. It operates only on authorized records and records a correlation identifier for troubleshooting.

## Transient failure

**Q: What happens when an external dependency becomes temporarily unavailable?**

A: Transient payout provider errors are retried with the same payout reference. A user should not resubmit with a new request identity until the prior outcome has been checked.

## Retries and duplicates

**Q: Does pressing Retry create another business operation?**

A: An identical request using the same idempotency key is treated as the original operation. Support should inspect the operation history before recommending a new attempt.

## Operational lifecycle guidance

Temporary authorization tokens for Merchant payouts expire 30 minutes after issuance.

## Escalation

**Q: What if the active documentation disagrees?**

A: Record both literal statements and request a product-owner decision. Do not assume that the FAQ or business rules are always more recent or that a longer duration must be correct. Log the issue under the merchant-payouts feature key.

## Support checklist

Record the outcome, request ID, approximate UTC time and sanitized error category. Do not request passwords, bearer tokens or private attachments in tickets. Recheck the relevant policy before updating acceptance criteria. Support agents cannot authorize a new threshold by extrapolating an existing provider limit.


---

## Document 057

# ADR-010 — Asynchronous Reconciliation: Merchant payouts

**Project:** ShopFlow  
**Feature:** merchant-payouts  
**Status:** Active  
**Decision status:** Accepted  

## Context

The merchant payouts workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a merchant operator attempts to review and request payout of eligible earnings.

## Decision

Persist uncertain provider outcomes and reconcile them by reference instead of assuming success or failure.

## Alternatives

The team considered a simple synchronous design. It was rejected because: External providers can time out after accepting a request. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for merchant payouts. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.
