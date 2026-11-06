# Loan extensions — Workflow

Document ID: `TN-EXT-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

An extension modifies the due time of an existing loan. It must preserve the original reservation history and protect the next borrower from an overlapping use of the same physical unit.

## Requirements and guidance

### TN-EXT-WF-01

The extension screen shows the current due time and the requested new due time before submission.

### TN-EXT-WF-02

A failed extension preserves the current dueAt and shows the blocking reason without exposing another borrower's identity.

### TN-EXT-WF-03

The server rechecks availability inside the due-time update transaction.

### TN-EXT-WF-04

A separate research-loan extension exception has been requested, but its limits and authorized approvers remain undecided.
