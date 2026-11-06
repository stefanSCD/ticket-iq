# Waiting lists and offers — Workflow

Document ID: `TN-WAI-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

The waiting list offers a newly freed interval to an eligible borrower. An offer is a temporary hold rather than an automatic reservation; the borrower still has to accept before its deadline.

## Requirements and guidance

### TN-WAI-WF-01

When cancellation frees an interval, the worker checks training and suspension before creating an offer.

### TN-WAI-WF-02

Accepting a still-valid offer creates a Confirmed reservation and closes the corresponding waiting-list entry.

### TN-WAI-WF-03

An expired offer releases the temporary hold and processing continues with the next eligible entry.

### TN-WAI-WF-04

Priority treatment for accessibility accommodations has been requested but neither the priority rule nor its authorizer is agreed.
