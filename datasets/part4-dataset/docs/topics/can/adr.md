# Cancellations and booking edits — Architecture decision

Document ID: `TN-CAN-ADR`  
Owner: Matei Ionescu, Tech Lead  
Status: Active  
Applies to: ToolNest 1.1  
Published: 2026-08-28T08:00:00Z

## Context

Cancelling a booking is a reservation operation and is distinct from returning borrowed equipment. The system must release inventory promptly while retaining enough history to explain who cancelled the request and why.

## Requirements and guidance

### TN-CAN-ADR-01

Cancelled reservations are retained for history and are excluded from blocking interval queries.

### TN-CAN-ADR-02

Cancellation publication uses the transactional outbox so a committed cancellation can trigger wait-list processing.

### TN-CAN-ADR-03

A cancellation is not represented as deletion of the reservation row.
