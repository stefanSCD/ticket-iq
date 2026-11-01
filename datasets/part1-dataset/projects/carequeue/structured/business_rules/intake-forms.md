# Business Rules — Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  

## Approved feature policy

Submitted administrative intake forms are immutable; corrections require a new revision.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate pre-visit intake forms operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted pre-visit intake forms request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Pre-visit intake forms remain downloadable for 7 days.

## Positive scenario

Given a patient with record access, when the user requests to complete administrative intake information before a visit, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for pre-visit intake forms. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
