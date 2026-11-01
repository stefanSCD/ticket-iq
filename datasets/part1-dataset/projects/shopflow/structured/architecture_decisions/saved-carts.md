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
