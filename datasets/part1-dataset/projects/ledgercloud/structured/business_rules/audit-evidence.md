# Business Rules — Audit evidence bundles

**Project:** LedgerCloud  
**Feature:** audit-evidence  
**Status:** Active  

## Approved feature policy

Draft invoices must be labeled as drafts and cannot be represented as issued documents.

## Eligible actors

Only authenticated auditor identities with permission on the relevant record may initiate audit evidence bundles operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted audit evidence bundles request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Temporary authorization tokens for Audit evidence bundles expire 10 minutes after issuance.

## Positive scenario

Given a auditor with record access, when the user requests to assemble audit evidence for an invoice period, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for audit evidence bundles. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
