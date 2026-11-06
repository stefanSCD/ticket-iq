# Returns and condition inspection — Architecture decision

Document ID: `TN-RET-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

A return records physical receipt separately from condition inspection. Staff need to stop the loan clock when equipment arrives without prematurely making an uninspected unit available to the next borrower.

## Requirements and guidance

### TN-RET-ADR-01

Receipt time is immutable; inspection completion time is a separate timestamp.

### TN-RET-ADR-02

The loan record keeps the checkout accessory list as a snapshot so later catalog edits do not change return obligations.

### TN-RET-ADR-03

A condition problem is routed through the incident workflow rather than overwriting the original checkout condition.
