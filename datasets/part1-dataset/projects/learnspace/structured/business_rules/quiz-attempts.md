# Business Rules — Quiz attempts

**Project:** LearnSpace  
**Feature:** quiz-attempts  
**Status:** Active  

## Approved feature policy

Each quiz attempt has one final submission; duplicate finalization requests are idempotent.

## Eligible actors

Only authenticated student identities with permission on the relevant record may initiate quiz attempts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted quiz attempts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Quiz attempts workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a student with record access, when the user requests to start and submit an online quiz attempt, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for quiz attempts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
