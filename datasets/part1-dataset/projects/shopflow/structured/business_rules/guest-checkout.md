# Business Rules — Guest checkout

**Project:** ShopFlow  
**Feature:** guest-checkout  
**Status:** Active  

## Approved feature policy

Guest checkout does not require account creation, but a verified contact email is required.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate guest checkout operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted guest checkout request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

The Guest checkout workflow opens manual review after 3 consecutive processing failures.

## Positive scenario

Given a shopper with record access, when the user requests to place an order without creating an account, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for guest checkout. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
