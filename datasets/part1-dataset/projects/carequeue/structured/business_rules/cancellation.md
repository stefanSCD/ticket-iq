# Business Rules — Appointment cancellation

**Project:** CareQueue  
**Feature:** cancellation  
**Status:** Active  

## Approved feature policy

A canceled appointment releases its slot back to the availability pool.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate appointment cancellation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment cancellation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Appointment cancellation workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a patient with record access, when the user requests to cancel a scheduled visit, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment cancellation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
