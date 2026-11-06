# Loan extensions — Architecture decision

Document ID: `TN-EXT-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

An extension modifies the due time of an existing loan. It must preserve the original reservation history and protect the next borrower from an overlapping use of the same physical unit.

## Requirements and guidance

### TN-EXT-ADR-01

The availability constraint includes the occupied interval of an Open loan after its due time is extended.

### TN-EXT-ADR-02

The approved-extension counter belongs to the loan, not to the borrower's lifetime account.

### TN-EXT-ADR-03

Loan extension and reservation creation serialize their interval checks against the same unit.
