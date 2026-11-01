# Business Rules — Provider availability

**Project:** CareQueue  
**Feature:** provider-availability  
**Status:** Active  

## Approved feature policy

Published appointment slots for the same clinician must not overlap.

## Eligible actors

Only authenticated clinic receptionist identities with permission on the relevant record may initiate provider availability operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted provider availability request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational event records for Provider availability must be retained for 30 days after closure.

## Positive scenario

Given a clinic receptionist with record access, when the user requests to manage available appointment slots for a clinician, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for provider availability. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
