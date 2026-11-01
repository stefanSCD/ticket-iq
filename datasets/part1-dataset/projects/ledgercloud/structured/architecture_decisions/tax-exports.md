# ADR-008 — Append-only Operation History: Tax export generation

**Project:** LedgerCloud  
**Feature:** tax-exports  
**Status:** Active  
**Decision status:** Accepted  

## Context

The tax export generation workflow can encounter duplicate client commands, delayed callbacks and temporary integration outages. The goal is to retain state consistency and a traceable record when a finance manager attempts to prepare an accounting tax export for a reporting period.

## Decision

Store immutable state-transition events and derive the visible current state from a checked projection.

## Alternatives

The team considered a simple synchronous design. It was rejected because: Overwriting historical states weakens troubleshooting and auditability. The approved design makes failure handling explicit and observable, rather than hiding uncertainty in a retry loop.

## Consequences

The implementation must preserve request identifiers, instrument retries and expose terminal versus pending state. Integration tests must exercise duplicated requests, transient failures and out-of-order acknowledgements. Support tools should not leak private record payloads.

## Scope of architectural decision

This ADR chooses an implementation mechanism and does not authorize a price, timing threshold, maximum attempt count or retention period for tax export generation. Such choices remain product policy and must be sourced separately.

## Verification

Exercise a normal operation, invalid authentication, a duplicate request, an external outage and delayed reconciliation. Confirm the result matches the functional workflow and approved business rules.
