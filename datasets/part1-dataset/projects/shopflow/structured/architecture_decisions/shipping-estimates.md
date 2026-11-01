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
