# Business Rules — Shipment exception alerts

**Project:** ParcelRoute  
**Feature:** exception-alerts  
**Status:** Active  

## Approved feature policy

Resolved shipment exceptions are excluded from newly generated alert batches.

## Eligible actors

Only authenticated sender identities with permission on the relevant record may initiate shipment exception alerts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted shipment exception alerts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Shipment exception alerts workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a sender with record access, when the user requests to receive alerts when a shipment needs attention, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for shipment exception alerts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
