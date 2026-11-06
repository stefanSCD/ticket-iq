# Pickup and checkout — Business rules

Document ID: `TN-OUT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Physical handover creates a loan from a confirmed reservation. Staff scan a unit label and verify the borrower rather than treating possession of a reservation number as sufficient identity proof.

## Requirements and guidance

### TN-OUT-BR-01

Checkout requires a Confirmed reservation, its assigned asset, a present borrower, and a lab_technician or lab_manager grant for the pickup lab.

### TN-OUT-BR-02

The technician verifies the borrower using the university ID and records the result before committing checkout.

### TN-OUT-BR-03

A successful checkout atomically changes the reservation to Collected and creates one Open loan.

### TN-OUT-BR-04

The scanned asset must match the reservation's assigned unit; mismatch does not silently substitute another unit.

### TN-OUT-BR-05

Normal checkout can begin 15 minutes before the reservation start instant.
