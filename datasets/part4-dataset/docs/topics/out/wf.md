# Pickup and checkout — Workflow

Document ID: `TN-OUT-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Physical handover creates a loan from a confirmed reservation. Staff scan a unit label and verify the borrower rather than treating possession of a reservation number as sufficient identity proof.

## Requirements and guidance

### TN-OUT-WF-01

The checkout screen shows the borrower name, assigned asset tag, accessories checklist, and current eligibility result.

### TN-OUT-WF-02

Staff confirm that every required accessory is present or record a pre-existing exception before handover.

### TN-OUT-WF-03

A failed identity verification leaves the reservation unchanged and creates no loan.

### TN-OUT-WF-04

Offline checkout has no approved synchronization or trust model; it is tracked as a future design decision.
