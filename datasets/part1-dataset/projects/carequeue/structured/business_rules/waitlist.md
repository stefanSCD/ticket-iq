# Business Rules — Waitlist offers

**Project:** CareQueue  
**Feature:** waitlist  
**Status:** Active  

## Approved feature policy

A waitlist slot can be confirmed by only one patient through an atomic acceptance operation.

## Eligible actors

Only authenticated patient identities with permission on the relevant record may initiate waitlist offers operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted waitlist offers request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Waitlist offers remain downloadable for 7 days.

## Positive scenario

Given a patient with record access, when the user requests to accept an earlier appointment from the waitlist, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for waitlist offers. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
