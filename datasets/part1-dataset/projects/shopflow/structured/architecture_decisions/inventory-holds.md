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
