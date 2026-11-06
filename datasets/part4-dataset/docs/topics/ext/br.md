# Loan extensions — Business rules

Document ID: `TN-EXT-BR`  
Owner: Elena Varga, Product Owner  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

An extension modifies the due time of an existing loan. It must preserve the original reservation history and protect the next borrower from an overlapping use of the same physical unit.

## Requirements and guidance

### TN-EXT-BR-01

A borrower can request an extension only for their own Open loan before its current dueAt.

### TN-EXT-BR-02

An ordinary loan may receive at most one approved extension.

### TN-EXT-BR-03

An extension must not overlap a confirmed reservation, an awaiting-approval reservation, or an active maintenance block.

### TN-EXT-BR-04

Extension approval updates loan.dueAt and records the prior dueAt without rewriting the original reservation interval.

### TN-EXT-BR-05

An ordinary extension may add at most 24 hours to the current dueAt.
