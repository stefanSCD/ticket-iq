# Business Rules — Invoice draft approval

**Project:** LedgerCloud  
**Feature:** draft-approval  
**Status:** Active  

## Approved feature policy

The author of an invoice draft cannot act as its final approver.

## Eligible actors

Only authenticated finance manager identities with permission on the relevant record may initiate invoice draft approval operations. Administrative access is logged and does not bypass record ownership checks.

## Consistency and state

Each accepted invoice draft approval request applies to exactly one authorized target. A rejected validation cannot advance state. Same-key identical retries must not apply the action twice. A missing or invalid identity cannot be treated as a request from a default actor.

## Operational lifecycle

Deduplication keys for Invoice draft approval remain valid for 12 hours after the first request.

## Positive scenario

Given a finance manager with record access, when the user requests to approve invoice drafts before they are issued, the service validates the request and produces a traceable operation. The normative feature policy above applies to the outcome. A successful command remains verifiable through its operation ID.

## Negative scenario

Given an unrelated identity, when a record from another account is referenced, the service denies mutation and does not disclose private values. Given a repeated request with a stable idempotency key, the service returns the same business outcome without replaying side effects.

## Ownership

A product owner must approve changes to the domain policy for invoice draft approval. Engineering and support staff may propose options but cannot infer an unrecorded time window, price, threshold or retry count from neighboring features.
