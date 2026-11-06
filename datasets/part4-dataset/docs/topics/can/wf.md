# Cancellations and booking edits — Workflow

Document ID: `TN-CAN-WF`  
Owner: Iris Popa, Operations Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Cancelling a booking is a reservation operation and is distinct from returning borrowed equipment. The system must release inventory promptly while retaining enough history to explain who cancelled the request and why.

## Requirements and guidance

### TN-CAN-WF-01

The confirmation dialog identifies the asset and interval that will be cancelled.

### TN-CAN-WF-02

When a staff cancellation commits, the borrower receives the reason in the in-app notification.

### TN-CAN-WF-03

The reservation history retains actorId, cancelledAt, and the cancellation reason.

### TN-CAN-WF-04

Automatic penalties for repeated cancellations are not defined; the product team has not chosen a threshold or sanction.
