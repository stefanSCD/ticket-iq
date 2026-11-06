# Pickup and checkout — Architecture decision

Document ID: `TN-OUT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Physical handover creates a loan from a confirmed reservation. Staff scan a unit label and verify the borrower rather than treating possession of a reservation number as sufficient identity proof.

## Requirements and guidance

### TN-OUT-ADR-01

QR labels encode opaque asset UUIDs rather than borrower identifiers or authorization tokens.

### TN-OUT-ADR-02

Checkout is one database transaction so a collected reservation cannot exist without its loan.

### TN-OUT-ADR-03

A university ID verification is recorded as an attestation; ToolNest stores no image of the identity document.
