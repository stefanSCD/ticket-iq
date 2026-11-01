# Business Rules — Course file downloads

**Project:** LearnSpace  
**Feature:** downloads  
**Status:** Active  

## Approved feature policy

Course files require an active course enrollment before download access is granted.

## Eligible actors

Only authenticated student identities with permission on the relevant record may initiate course file downloads operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted course file downloads request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Course file downloads expire 10 minutes after issuance.

## Positive scenario

Given a student with record access, when the user requests to download materials from an enrolled course, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for course file downloads. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
