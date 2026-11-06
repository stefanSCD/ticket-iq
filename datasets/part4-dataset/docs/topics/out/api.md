# Pickup and checkout — API contract

Document ID: `TN-OUT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Physical handover creates a loan from a confirmed reservation. Staff scan a unit label and verify the borrower rather than treating possession of a reservation number as sufficient identity proof.

## Requirements and guidance

### TN-OUT-API-01

POST /v1/checkouts requires reservationId, scannedAssetId, identityVerified=true, and an Idempotency-Key.

### TN-OUT-API-02

A repeated checkout with the same actor, key, and payload returns the original loan; a changed payload returns 409 IDEMPOTENCY_MISMATCH.

### TN-OUT-API-03

An asset mismatch returns 409 WRONG_ASSET and an eligibility failure creates no loan.

### TN-OUT-API-04

The server uses actual server time for the checkout window; a client-provided timestamp cannot move that window.
