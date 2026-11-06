# Overdue loans and account restrictions — Workflow

Document ID: `TN-OVD-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

ToolNest v1.1 tracks late loans and borrowing restrictions without collecting money. Overdue state follows the physical receipt time; a delayed staff inspection must not make the borrower appear to keep equipment longer.

## Requirements and guidance

### TN-OVD-WF-01

The borrower dashboard lists the due time and overdue duration for each outstanding loan.

### TN-OVD-WF-02

The staff overdue queue is scoped to the labs for which the actor has a staff grant.

### TN-OVD-WF-03

ToolNest v1.1 records no monetary fines; a future charging policy requires a separate product decision.

### TN-OVD-WF-04

An overdue job rechecks receipt state before publishing a reminder intent.
