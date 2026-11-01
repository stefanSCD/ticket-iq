# Business Rules — Patient check-in

**Project:** CareQueue  
**Feature:** check-in  
**Status:** Active  

## Approved feature policy

An appointment may have one active check-in record; duplicate check-in requests are idempotent.

## Eligible actors

Only authenticated clinic receptionist identities with permission on the relevant record may initiate patient check-in operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted patient check-in request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Patient check-in remain valid for 12 hours after the first request.

## Positive scenario

Given a clinic receptionist with record access, when the user requests to mark patients as arrived at the clinic, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for patient check-in. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
