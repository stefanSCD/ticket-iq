# Business Rules — Delivery address validation

**Project:** ParcelRoute  
**Feature:** address-check  
**Status:** Active  

## Approved feature policy

An address that fails validation cannot be automatically marked as verified.

## Eligible actors

Only authenticated sender identities with permission on the relevant record may initiate delivery address validation operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted delivery address validation request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Delivery address validation remain valid for 12 hours after the first request.

## Positive scenario

Given a sender with record access, when the user requests to validate a delivery address before label purchase, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for delivery address validation. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
