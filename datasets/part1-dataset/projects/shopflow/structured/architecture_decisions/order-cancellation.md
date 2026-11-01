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
