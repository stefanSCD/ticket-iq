# Business Rules — Grade publication

**Project:** LearnSpace  
**Feature:** grade-release  
**Status:** Active  

## Approved feature policy

Assessment grades remain hidden from students until an instructor explicitly publishes them.

## Eligible actors

Only authenticated instructor identities with permission on the relevant record may initiate grade publication operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted grade publication request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Grade publication remain valid for 12 hours after the first request.

## Positive scenario

Given a instructor with record access, when the user requests to publish finalized assessment grades to students, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for grade publication. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
