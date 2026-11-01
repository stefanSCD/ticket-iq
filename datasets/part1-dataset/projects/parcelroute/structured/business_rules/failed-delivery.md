# Business Rules — Failed delivery handling

**Project:** ParcelRoute  
**Feature:** failed-delivery  
**Status:** Active  

## Approved feature policy

Every failed delivery attempt requires a standardized failure reason code.

## Eligible actors

Only authenticated delivery agent identities with permission on the relevant record may initiate failed delivery handling operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted failed delivery handling request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Failed delivery handling must be retained for 30 days after closure.

## Positive scenario

Given a delivery agent with record access, when the user requests to record an unsuccessful delivery attempt, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for failed delivery handling. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
