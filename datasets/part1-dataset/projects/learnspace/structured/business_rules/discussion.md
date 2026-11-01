# Business Rules — Discussion moderation

**Project:** LearnSpace  
**Feature:** discussion  
**Status:** Active  

## Approved feature policy

Removed discussion posts are hidden from student views but retained in the moderation audit trail.

## Eligible actors

Only authenticated teaching assistant identities with permission on the relevant record may initiate discussion moderation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted discussion moderation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Discussion moderation expire 10 minutes after issuance.

## Positive scenario

Given a teaching assistant with record access, when the user requests to moderate posts in course discussions, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for discussion moderation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
