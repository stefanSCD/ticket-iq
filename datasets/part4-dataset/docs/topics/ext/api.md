# Loan extensions — API contract

Document ID: `TN-EXT-API`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

An extension modifies the due time of an existing loan. It must preserve the original reservation history and protect the next borrower from an overlapping use of the same physical unit.

## Requirements and guidance

### TN-EXT-API-01

POST /v1/loans/{id}/extensions requires requestedDueAt and the current loan version.

### TN-EXT-API-02

A past-due extension request returns 409 LOAN_ALREADY_OVERDUE.

### TN-EXT-API-03

An overlapping extension returns 409 EXTENSION_CONFLICT without modifying the loan.

### TN-EXT-API-04

An extension event records oldDueAt, newDueAt, actorId, and loanId.
