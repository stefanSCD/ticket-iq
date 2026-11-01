# Functional Specification — Pre-visit intake forms

**Project:** CareQueue  
**Feature:** intake-forms  
**Status:** Active  

## Business purpose

CareQueue uses pre-visit intake forms to allow a patient to complete administrative intake information before a visit. The desired outcome is observable and bound to one record. The feature works within outpatient appointment and administration platform. A client interface does not create new business rules simply because a provider supports an option.

## Primary workflow

1. An authenticated patient opens a record and chooses to complete administrative intake information before a visit.
2. The client includes a target identifier, request ID and any required fields.
3. The service checks identity, scope, state and input validity.
4. A valid command records one transaction and an auditable operation ID.
5. The client shows the confirmed state returned by the service.
6. A transient integration failure can leave an operation pending; the client does not falsely report completion.

## Core acceptance paths

An allowed patient receives an operation reference and can look up the outcome. Invalid requests fail without mutation. Unauthorized record access returns a generic denial. Repeated commands with the same idempotency key have one business effect. A request racing with another change is checked against current record state before commit.

## User experience and accessibility

The pre-visit intake forms action requires a visible label, keyboard access, an explicit pending state, a confirmation on terminal success and a recoverable error on rejection. The client should preserve user input across retryable failures. Error messages should not expose private record details or access tokens.

## In scope / out of scope

In scope: the happy path, common validation errors, authorization, idempotent retries and event traceability for pre-visit intake forms. Out of scope: new commercial rules, undocumented time thresholds, policy changes for other features, and arbitrary product-owner decisions inferred from implementation choices.

## Related documents

The business-rules document defines normative policy, the API specification describes the transport contract, the FAQ captures troubleshooting behavior, and the ADR records implementation constraints. If active sources disagree, the product owner must resolve the contradiction.
