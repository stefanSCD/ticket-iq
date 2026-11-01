# Business Rules — Vendor onboarding

**Project:** LedgerCloud  
**Feature:** vendor-onboarding  
**Status:** Active  

## Approved feature policy

A verified tax identifier cannot belong to two active vendor records in one legal entity.

## Eligible actors

Only authenticated vendor administrator identities with permission on the relevant record may initiate vendor onboarding operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted vendor onboarding request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Vendor onboarding must be retained for 30 days after closure.

## Positive scenario

Given a vendor administrator with record access, when the user requests to review and activate a new vendor record, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for vendor onboarding. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
