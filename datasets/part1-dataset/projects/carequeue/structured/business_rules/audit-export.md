# Business Rules — Appointment audit exports

**Project:** CareQueue  
**Feature:** audit-export  
**Status:** Active  

## Approved feature policy

Appointment audit exports are restricted to the requesting clinic tenant.

## Eligible actors

Only authenticated clinic administrator identities with permission on the relevant record may initiate appointment audit exports operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted appointment audit exports request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Appointment audit exports expire 10 minutes after issuance.

## Positive scenario

Given a clinic administrator with record access, when the user requests to export scheduling changes for an authorized audit, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for appointment audit exports. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
