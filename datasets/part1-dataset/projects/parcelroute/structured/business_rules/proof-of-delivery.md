# Business Rules — Proof of delivery

**Project:** ParcelRoute  
**Feature:** proof-of-delivery  
**Status:** Active  

## Approved feature policy

Final delivery requires at least one proof artifact: recipient signature or delivery photo.

## Eligible actors

Only authenticated delivery agent identities with permission on the relevant record may initiate proof of delivery operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted proof of delivery request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Operational audit extracts for Proof of delivery remain downloadable for 7 days.

## Positive scenario

Given a delivery agent with record access, when the user requests to record evidence that a shipment was delivered, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for proof of delivery. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
