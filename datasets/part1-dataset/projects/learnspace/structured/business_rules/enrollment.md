# Business Rules — Course enrollment approval

**Project:** LearnSpace  
**Feature:** enrollment  
**Status:** Active  

## Approved feature policy

Restricted courses require an accepted enrollment request before access is granted.

## Eligible actors

Only authenticated course administrator identities with permission on the relevant record may initiate course enrollment approval operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted course enrollment approval request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Course enrollment approval remain downloadable for 7 days.

## Positive scenario

Given a course administrator with record access, when the user requests to approve enrollment requests for restricted courses, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for course enrollment approval. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
