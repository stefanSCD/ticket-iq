# LedgerCloud — Quality and observability

**Status:** Active

## About

LedgerCloud: Small-business invoicing and expense administration. The page is authoritative only in the synthetic project context.

## Quality baseline

Financial writes must be auditable and idempotent; published invoice amounts cannot be silently rewritten.

## Observability

Services expose correlation IDs, stable error classes, retry queue health and pending-versus-terminal outcomes. Private payloads are redacted.

## Acceptance

Project-wide availability targets do not set feature-specific reminder deadlines, payment thresholds, retry ceilings or retention periods. QA must ask if a product-specific boundary remains undocumented.
