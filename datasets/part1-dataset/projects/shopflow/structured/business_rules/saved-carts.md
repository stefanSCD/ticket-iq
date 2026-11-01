# Business Rules — Saved shopping carts

**Project:** ShopFlow  
**Feature:** saved-carts  
**Status:** Active  

## Approved feature policy

Saving a cart does not lock prices; current prices are checked again at checkout.

## Eligible actors

Only authenticated shopper identities with permission on the relevant record may initiate saved shopping carts operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted saved shopping carts request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Saved shopping carts expire 10 minutes after issuance.

## Positive scenario

Given a shopper with record access, when the user requests to resume a previously saved shopping cart, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for saved shopping carts. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
