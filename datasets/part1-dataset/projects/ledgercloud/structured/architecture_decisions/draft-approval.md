# ADR-002 — Idempotent Command Handler: Invoice draft approval

**Project:** LedgerCloud  
**Feature:** draft-approval  
**Status:** Active  
**Decision status:** Accepted  

## Context

The invoice draft approval workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a finance manager attempts to approve invoice drafts before they are issued.

## Decision

Persist a stable key and operation result before repeating a potentially side-effecting command.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Blind network retries can duplicate user-visible actions. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for invoice draft approval. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.
