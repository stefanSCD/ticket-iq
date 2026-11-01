# Business Rules — Tax export generation

**Project:** LedgerCloud  
**Feature:** tax-exports  
**Status:** Active  

## Approved feature policy

Published tax exports contain only transactions posted within the selected reporting period.

## Eligible actors

Only authenticated finance manager identities with permission on the relevant record may initiate tax export generation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted tax export generation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Tax export generation workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a finance manager with record access, when the user requests to prepare an accounting tax export for a reporting period, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for tax export generation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
