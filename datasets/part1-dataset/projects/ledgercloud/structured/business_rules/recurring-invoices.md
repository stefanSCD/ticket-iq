# Business Rules — Recurring invoicing

**Project:** LedgerCloud  
**Feature:** recurring-invoices  
**Status:** Active  

## Approved feature policy

Each recurring schedule produces at most one invoice for each billing cycle.

## Eligible actors

Only authenticated finance clerk identities with permission on the relevant record may initiate recurring invoicing operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted recurring invoicing request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Recurring invoicing workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a finance clerk with record access, when the user requests to schedule recurring invoice generation, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for recurring invoicing. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
