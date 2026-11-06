# Returns and condition inspection — API contract

Document ID: `TN-RET-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A return records physical receipt separately from condition inspection. Staff need to stop the loan clock when equipment arrives without prematurely making an uninspected unit available to the next borrower.

## Requirements and guidance

### TN-RET-API-01

POST /v1/loans/{id}/receive returns the receipt ID and receivedAt without marking the unit Active or available.

### TN-RET-API-02

POST /v1/return-inspections requires receiptId, conditionResult, and one result for each required accessory.

### TN-RET-API-03

A second receive action for a loan already received returns the existing receipt and does not change receivedAt.

### TN-RET-API-04

An incomplete accessories checklist returns 422 INCOMPLETE_INSPECTION and leaves the inspection unfinished.
