# Returns and condition inspection — Business rules

Document ID: `TN-RET-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A return records physical receipt separately from condition inspection. Staff need to stop the loan clock when equipment arrives without prematurely making an uninspected unit available to the next borrower.

## Requirements and guidance

### TN-RET-BR-01

Recording receipt changes an Open loan to ReturnedPendingInspection and records receivedAt using server time.

### TN-RET-BR-02

A returned unit remains unavailable until staff finish its condition inspection.

### TN-RET-BR-03

Inspection must record a condition result for the unit and a present or missing result for every required accessory.

### TN-RET-BR-04

A clean inspection closes the loan and makes the unit available unless another reservation or maintenance block applies.

### TN-RET-BR-05

A return inspection is due within 4 staffed operating hours after receipt.
