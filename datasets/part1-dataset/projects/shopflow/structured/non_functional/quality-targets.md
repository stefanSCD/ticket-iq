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
